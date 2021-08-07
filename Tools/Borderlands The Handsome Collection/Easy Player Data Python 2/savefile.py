#! /usr/bin/env python

import binascii
from bisect import insort
from cStringIO import StringIO
import hashlib
import json
import math
import optparse
import random
import struct
import sys


class BL2Error(Exception): pass


class ReadBitstream(object):

    def __init__(self, s):
        self.s = s
        self.i = 0

    def read_bit(self):
        i = self.i
        self.i = i + 1
        byte = ord(self.s[i >> 3])
        bit = byte >> (7 - (i & 7))
        return bit & 1

    def read_bits(self, n):
        s = self.s
        i = self.i
        end = i + n
        chunk = s[i >> 3: (end + 7) >> 3]
        value = ord(chunk[0]) &~ (0xff00 >> (i & 7))
        for c in chunk[1: ]:
            value = (value << 8) | ord(c)
        if (end & 7) != 0:
            value = value >> (8 - (end & 7))
        self.i = end
        return value

    def read_byte(self):
        i = self.i
        self.i = i + 8
        byte = ord(self.s[i >> 3])
        if (i & 7) == 0:
            return byte
        byte = (byte << 8) | ord(self.s[(i >> 3) + 1])
        return (byte >> (8 - (i & 7))) & 0xff

class WriteBitstream(object):

    def __init__(self):
        self.s = ""
        self.byte = 0
        self.i = 7

    def write_bit(self, b):
        i = self.i
        byte = self.byte | (b << i)
        if i == 0:
            self.s += chr(byte)
            self.byte = 0
            self.i = 7
        else:
            self.byte = byte
            self.i = i - 1

    def write_bits(self, b, n):
        s = self.s
        byte = self.byte
        i = self.i
        while n >= (i + 1):
            shift = n - (i + 1)
            n = n - (i + 1)
            byte = byte | (b >> shift)
            b = b &~ (byte << shift)
            s = s + chr(byte)
            byte = 0
            i = 7
        if n > 0:
            byte = byte | (b << (i + 1 - n))
            i = i - n
        self.s = s
        self.byte = byte
        self.i = i

    def write_byte(self, b):
        i = self.i
        if i == 7:
            self.s += chr(b)
        else:
            self.s += chr(self.byte | (b >> (7 - i)))
            self.byte = (b << (i + 1)) & 0xff

    def getvalue(self):
        if self.i != 7:
            return self.s + chr(self.byte)
        else:
            return self.s


def read_huffman_tree(b):
    node_type = b.read_bit()
    if node_type == 0:
        return (None, (read_huffman_tree(b), read_huffman_tree(b)))
    else:
        return (None, b.read_byte())

def write_huffman_tree(node, b):
    if type(node[1]) is int:
        b.write_bit(1)
        b.write_byte(node[1])
    else:
        b.write_bit(0)
        write_huffman_tree(node[1][0], b)
        write_huffman_tree(node[1][1], b)

def make_huffman_tree(data):
    frequencies = [0] * 256
    for c in data:
        frequencies[ord(c)] += 1

    nodes = [[f, i] for (i, f) in enumerate(frequencies) if f != 0]
    nodes.sort()

    while len(nodes) > 1:
        l, r = nodes[: 2]
        nodes = nodes[2: ]
        insort(nodes, [l[0] + r[0], [l, r]])

    return nodes[0]

def invert_tree(node, code=0, bits=0):
    if type(node[1]) is int:
        return {chr(node[1]): (code, bits)}
    else:
        d = {}
        d.update(invert_tree(node[1][0], code << 1, bits + 1))
        d.update(invert_tree(node[1][1], (code << 1) | 1, bits + 1))
        return d

def huffman_decompress(tree, bitstream, size):
    output = ""
    while len(output) < size:
        node = tree
        while 1:
            b = bitstream.read_bit()
            node = node[1][b]
            if type(node[1]) is int:
                output += chr(node[1])
                break
    return output

def huffman_compress(encoding, data, bitstream):
    for c in data:
        code, nbits = encoding[c]
        bitstream.write_bits(code, nbits)


item_sizes = (
    (8, 17, 20, 11, 7, 7, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16),
    (8, 13, 20, 11, 7, 7, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17)
)

def pack_item_values(is_weapon, values):
    i = 0
    bytes = [0] * 32
    for value, size in zip(values, item_sizes[is_weapon]):
        if value is None:
            break
        j = i >> 3
        value = value << (i & 7)
        while value != 0:
            bytes[j] |= value & 0xff
            value = value >> 8
            j = j + 1
        i = i + size
    if (i & 7) != 0:
        value = 0xff << (i & 7)
        bytes[i >> 3] |= (value & 0xff)
    return "".join(map(chr, bytes[: (i + 7) >> 3]))

def unpack_item_values(is_weapon, data):
    i = 8
    data = " " + data
    values = []
    end = len(data) * 8
    for size in item_sizes[is_weapon]:
        j = i + size
        if j > end:
            values.append(None)
            continue
        value = 0
        for b in data[j >> 3: (i >> 3) - 1: -1]:
            value = (value << 8) | ord(b)
        values.append((value >> (i & 7)) &~ (0xff << size))
        i = j
    return values

def rotate_data_right(data, steps):
    steps = steps % len(data)
    return data[-steps: ] + data[: -steps]

def rotate_data_left(data, steps):
    steps = steps % len(data)
    return data[steps: ] + data[: steps]

def xor_data(data, key):
    key = key & 0xffffffff
    output = ""
    for c in data:
        key = (key * 279470273) % 4294967291
        output += chr((ord(c) ^ key) & 0xff)
    return output

def wrap_item(is_weapon, values, key):
    item = pack_item_values(is_weapon, values)
    header = struct.pack(">Bi", (is_weapon << 7) | 7, key)
    padding = "\xff" * (33 - len(item))
    h = binascii.crc32(header + "\xff\xff" + item + padding) & 0xffffffff
    checksum = struct.pack(">H", ((h >> 16) ^ h) & 0xffff)
    body = xor_data(rotate_data_left(checksum + item, key & 31), key >> 5)
    return header + body

def unwrap_item(data):
    version_type, key = struct.unpack(">Bi", data[: 5])
    is_weapon = version_type >> 7
    raw = rotate_data_right(xor_data(data[5: ], key >> 5), key & 31)
    return is_weapon, unpack_item_values(is_weapon, raw[2: ]), key

def replace_raw_item_key(data, key):
    old_key = struct.unpack(">i", data[1: 5])[0]
    item = rotate_data_right(xor_data(data[5: ], old_key >> 5), old_key & 31)[2: ]
    header = data[0] + struct.pack(">i", key)
    padding = "\xff" * (33 - len(item))
    h = binascii.crc32(header + "\xff\xff" + item + padding) & 0xffffffff
    checksum = struct.pack(">H", ((h >> 16) ^ h) & 0xffff)
    body = xor_data(rotate_data_left(checksum + item, key & 31), key >> 5)
    return header + body


def read_varint(f):
    value = 0
    offset = 0
    while 1:
        b = ord(f.read(1))
        value |= (b & 0x7f) << offset
        if (b & 0x80) == 0:
            break
        offset = offset + 7
    return value

def write_varint(f, i):
    while i > 0x7f:
        f.write(chr(0x80 | (i & 0x7f)))
        i = i >> 7
    f.write(chr(i))

def read_protobuf(data):
    fields = {}
    end_position = len(data)
    bytestream = StringIO(data)
    while bytestream.tell() < end_position:
        key = read_varint(bytestream)
        field_number = key >> 3
        wire_type = key & 7
        value = read_protobuf_value(bytestream, wire_type)
        fields.setdefault(field_number, []).append([wire_type, value])
    return fields

def read_protobuf_value(b, wire_type):
    if wire_type == 0:
        value = read_varint(b)
    elif wire_type == 1:
        value = struct.unpack("<Q", b.read(8))[0]
    elif wire_type == 2:
        length = read_varint(b)
        value = b.read(length)
    elif wire_type == 5:
        value = struct.unpack("<I", b.read(4))[0]
    else:
        raise BL2Error("Unsupported wire type " + str(wire_type))
    return value

def read_repeated_protobuf_value(data, wire_type):
    b = StringIO(data)
    values = []
    while b.tell() < len(data):
        values.append(read_protobuf_value(b, wire_type))
    return values

def write_protobuf(data):
    b = StringIO()
    # If the data came from a JSON file the keys will all be strings
    data = dict([(int(k), v) for (k, v) in data.items()])
    for key, entries in sorted(data.items()):
        for wire_type, value in entries:
            if type(value) is dict:
                value = write_protobuf(value)
                wire_type = 2
            elif type(value) in (list, tuple) and wire_type != 2:
                sub_b = StringIO()
                for v in value:
                    write_protobuf_value(sub_b, wire_type, v)
                value = sub_b.getvalue()
                wire_type = 2
            write_varint(b, (key << 3) | wire_type)
            write_protobuf_value(b, wire_type, value)
    return b.getvalue()

def write_protobuf_value(b, wire_type, value):
    if wire_type == 0:
        write_varint(b, value)
    elif wire_type == 1:
        b.write(struct.pack("<Q", value))
    elif wire_type == 2:
        if type(value) is unicode:
            value = value.encode("latin1")
        elif type(value) is list:
            value = "".join(map(chr, value))
        write_varint(b, len(value))
        b.write(value)
    elif wire_type == 5:
        b.write(struct.pack("<I", value))
    else:
        raise BL2Error("Unsupported wire type " + str(wire_type))

def write_repeated_protobuf_value(data, wire_type):
    b = StringIO()
    for value in data:
        write_protobuf_value(b, wire_type, value)
    return b.getvalue()

def parse_zigzag(i):
    if i & 1:
        return -1 ^ (i >> 1)
    else:
        return i >> 1


def apply_structure(pbdata, s):
    fields = {}
    raw = {}
    for k, data in pbdata.items():
        mapping = s.get(k)
        if mapping is None:
            raw[k] = data
            continue
        elif type(mapping) is str:
            fields[mapping] = data[0][1]
            continue
        key, repeated, child_s = mapping
        if child_s is None:
            values = [d[1] for d in data]
            fields[key] = values if repeated else values[0]
        elif type(child_s) is int:
            if repeated:
                fields[key] = read_repeated_protobuf_value(data[0][1], child_s)
            else:
                fields[key] = data[0][1]
        elif type(child_s) is tuple:
            values = [child_s[0](d[1]) for d in data]
            fields[key] = values if repeated else values[0]
        elif type(child_s) is dict:
            values = [apply_structure(read_protobuf(d[1]), child_s) for d in data]
            fields[key] = values if repeated else values[0]
        else:
            raise Exception("Invalid mapping %r for %r: %r" % (mapping, k, data))
    if len(raw) != 0:
        fields["_raw"] = {}
        for k, values in raw.items():
            safe_values = []
            for (wire_type, v) in values:
                if wire_type == 2:
                    v = [ord(c) for c in v]
                safe_values.append([wire_type, v])
            fields["_raw"][k] = safe_values
    return fields

def remove_structure(data, inv):
    pbdata = {}
    pbdata.update(data.get("_raw", {}))
    for k, value in data.items():
        if k == "_raw":
            continue
        mapping = inv.get(k)
        if mapping is None:
            raise BL2Error("Unknown key %r in data" % (k, ))
        elif type(mapping) is int:
            pbdata[mapping] = [[guess_wire_type(value), value]]
            continue
        key, repeated, child_inv = mapping
        if child_inv is None:
            value = [value] if not repeated else value
            pbdata[key] = [[guess_wire_type(v), v] for v in value]
        elif type(child_inv) is int:
            if repeated:
                b = StringIO()
                for v in value:
                    write_protobuf_value(b, child_inv, v)
                pbdata[key] = [[2, b.getvalue()]]
            else:
                pbdata[key] = [[child_inv, value]]
        elif type(child_inv) is tuple:
            value = [value] if not repeated else value
            values = []
            for v in map(child_inv[1], value):
                if type(v) is list:
                    values.append(v)
                else:
                    values.append([guess_wire_type(v), v])
            pbdata[key] = values
        elif type(child_inv) is dict:
            value = [value] if not repeated else value
            values = []
            for d in [remove_structure(v, child_inv) for v in value]:
                values.append([2, write_protobuf(d)])
            pbdata[key] = values
        else:
            raise Exception("Invalid mapping %r for %r: %r" % (mapping, k, value))
    return pbdata

def guess_wire_type(value):
    return 2 if isinstance(value, basestring) else 0

def invert_structure(structure):
    inv = {}
    for k, v in structure.items():
        if type(v) is tuple:
            if type(v[2]) is dict:
                inv[v[0]] = (k, v[1], invert_structure(v[2]))
            else:
                inv[v[0]] = (k, ) + v[1: ]
        else:
            inv[v] = k
    return inv

def unwrap_bytes(value):
    return [ord(d) for d in value]

def wrap_bytes(value):
    return "".join(map(chr, value))

def unwrap_float(v):
    return struct.unpack("<f", struct.pack("<I", v))[0]

def wrap_float(v):
    return [5, struct.unpack("<I", struct.pack("<f", v))[0]]

black_market_keys = (
    "rifle", "pistol", "launcher", "shotgun", "smg",
    "sniper", "grenade", "backpack", "bank"
)

def unwrap_black_market(value):
    sdus = read_repeated_protobuf_value(value, 0)
    return dict(zip(black_market_keys, sdus))

def wrap_black_market(value):
    sdus = [value[k] for k in black_market_keys[: len(value)]]
    return write_repeated_protobuf_value(sdus, 0)

item_header_sizes = (
    (("type", 8), ("balance", 10), ("manufacturer", 7)),
    (("type", 6), ("balance", 10), ("manufacturer", 7))
)

def unwrap_item_info(value):
    is_weapon, item, key = unwrap_item(value)
    data = {
        "is_weapon": is_weapon,
        "key": key,
        "set": item[0],
        "level": [item[4], item[5]]
    }
    for i, (k, bits) in enumerate(item_header_sizes[is_weapon]):
        lib = item[1 + i] >> bits
        asset = item[1 + i] &~ (lib << bits)
        data[k] = {"lib": lib, "asset": asset}
    bits = 10 + is_weapon
    parts = []
    for value in item[6: ]:
        if value is None:
            parts.append(None)
        else:
            lib = value >> bits
            asset = value &~ (lib << bits)
            parts.append({"lib": lib, "asset": asset})
    data["parts"] = parts
    return data

def wrap_item_info(value):
    item = [value["set"]]
    for key, bits in item_header_sizes[value["is_weapon"]]:
        v = value[key]
        item.append((v["lib"] << bits) | v["asset"])
    item.extend(value["level"])
    bits = 10 + value["is_weapon"]
    for v in value["parts"]:
        if v is None:
            item.append(None)
        else:
            item.append((v["lib"] << bits) | v["asset"])
    return wrap_item(value["is_weapon"], item, value["key"])

save_structure = {
    1: "class",
    2: "level",
    3: "experience",
    4: "skill_points",
    6: ("currency", True, 0),
    7: "playthroughs_completed",
    8: ("skills", True, {
            1: "name",
            2: "level",
            3: "unknown3",
            4: "unknown4"
        }),
    11: ("resources", True, {
            1: "resource",
            2: "pool",
            3: ("amount", False, (unwrap_float, wrap_float)),
            4: "level"
        }),
    13: ("sizes", False, {
            1: "inventory",
            2: "weapon_slots",
            3: "weapon_slots_shown"
        }),
    15: ("stats", False, (unwrap_bytes, wrap_bytes)),
    16: ("active_fast_travel", True, None),
    17: "last_fast_travel",
    18: ("missions", True, {
            1: "playthrough",
            2: "active",
            3: ("data", True, {
                1: "name",
                2: "status",
                3: "is_from_dlc",
                4: "dlc_id",
                5: ("unknown5", False, (unwrap_bytes, wrap_bytes)),
                6: "unknown6",
                7: ("unknown7", False, (unwrap_bytes, wrap_bytes)),
                8: "unknown8",
                9: "unknown9",
                10: "unknown10",
                11: "level",
            }),
        }),
    19: ("appearance", False, {
            1: "name",
            2: ("color1", False, {1: "a", 2: "r", 3: "g", 4: "b"}),
            3: ("color2", False, {1: "a", 2: "r", 3: "g", 4: "b"}),
            4: ("color3", False, {1: "a", 2: "r", 3: "g", 4: "b"}),
        }),
    20: "save_game_id",
    21: "mission_number",
    23: ("unlocks", False, (unwrap_bytes, wrap_bytes)),
    24: ("unlock_notifications", False, (unwrap_bytes, wrap_bytes)),
    25: "time_played",
    26: "save_timestamp",
    29: ("game_stages", True, {
            1: "name",
            2: "level",
            3: "is_from_dlc",
            4: "dlc_id",
            5: "playthrough",
        }),
    30: ("areas", True, {
            1: "name",
            2: "unknown2"
        }),
    34: ("id", False, {
            1: ("a", False, 5),
            2: ("b", False, 5),
            3: ("c", False, 5),
            4: ("d", False, 5),
        }),
    35: ("wearing", True, None),
    36: ("black_market", False, (unwrap_black_market, wrap_black_market)),
    37: "active_mission",
    38: ("challenges", True, {
            1: "name",
            2: "is_from_dlc",
            3: "dlc_id"
        }),
    41: ("bank", True, {
            1: ("data", False, (unwrap_item_info, wrap_item_info)),
        }),
    43: ("lockouts", True, {
            1: "name",
            2: "time",
            3: "is_from_dlc",
            4: "dlc_id"
        }),
    46: ("explored_areas", True, None),
    49: "active_playthrough",
    53: ("items", True, {
            1: ("data", False, (unwrap_item_info, wrap_item_info)),
            2: "unknown2",
            3: "is_equipped",
            4: "star"
        }),
    54: ("weapons", True, {
            1: ("data", False, (unwrap_item_info, wrap_item_info)),
            2: "slot",
            3: "star",
            4: "unknown4",
        }),
    55: "stats_bonuses_disabled",
    56: "bank_size",
}


def unwrap_player_data(data):
    if data[: 4] == "CON ":
        raise BL2Error("You need to use a program like Horizon or Modio to extract the SaveGame.sav file first")

    if data[: 20] != hashlib.sha1(data[20: ]).digest():
        raise BL2Error("Invalid save file")

    data = lzo1x_decompress("\xf0" + data[20: ])
    size, wsg, version = struct.unpack(">I3sI", data[: 11])
    if version != 2 and version != 0x02000000:
        raise BL2Error("Unknown save version " + str(version))

    if version == 2:
        crc, size = struct.unpack(">II", data[11: 19])
    else:
        crc, size = struct.unpack("<II", data[11: 19])

    bitstream = ReadBitstream(data[19: ])
    tree = read_huffman_tree(bitstream)
    player = huffman_decompress(tree, bitstream, size)

    if (binascii.crc32(player) & 0xffffffff) != crc:
        raise BL2Error("CRC check failed")

    return player

def wrap_player_data(player, endian=1):
    crc = binascii.crc32(player) & 0xffffffff

    bitstream = WriteBitstream()
    tree = make_huffman_tree(player)
    write_huffman_tree(tree, bitstream)
    huffman_compress(invert_tree(tree), player, bitstream)
    data = bitstream.getvalue() + "\x00\x00\x00\x00"

    header = struct.pack(">I3s", len(data) + 15, "WSG")
    if endian == 1:
        header = header + struct.pack(">III", 2, crc, len(player))
    else:
        header = header + struct.pack("<III", 2, crc, len(player))

    data = lzo1x_1_compress(header + data)[1: ]

    return hashlib.sha1(data).digest() + data


def expand_zeroes(src, ip, extra):
    start = ip
    while src[ip] == 0:
        ip = ip + 1
    v = ((ip - start) * 255) + src[ip]
    return v + extra, ip + 1

def copy_earlier(b, offset, n):
    i = len(b) - offset
    end = i + n
    while i < end:
        chunk = b[i: i + n]
        i = i + len(chunk)
        n = n - len(chunk)
        b.extend(chunk)

def lzo1x_decompress(s):
    dst = bytearray()
    src = bytearray(s)
    ip = 5

    t = src[ip]; ip += 1
    if t > 17:
        t = t - 17
        dst.extend(src[ip: ip + t]); ip += t
        t = src[ip]; ip += 1
    elif t < 16:
        if t == 0:
            t, ip = expand_zeroes(src, ip, 15)
        dst.extend(src[ip: ip + t + 3]); ip += t + 3
        t = src[ip]; ip += 1

    while 1:
        while 1:
            if t >= 64:
                copy_earlier(dst, 1 + ((t >> 2) & 7) + (src[ip] << 3), (t >> 5) + 1); ip += 1
            elif t >= 32:
                count = t & 31
                if count == 0:
                    count, ip = expand_zeroes(src, ip, 31)
                t = src[ip]
                copy_earlier(dst, 1 + ((t | (src[ip + 1] << 8)) >> 2), count + 2); ip += 2
            elif t >= 16:
                offset = (t & 8) << 11
                count = t & 7
                if count == 0:
                    count, ip = expand_zeroes(src, ip, 7)
                t = src[ip]
                offset += (t | (src[ip + 1] << 8)) >> 2; ip += 2
                if offset == 0:
                    return str(dst)
                copy_earlier(dst, offset + 0x4000, count + 2)
            else:
                copy_earlier(dst, 1 + (t >> 2) + (src[ip] << 2), 2); ip += 1

            t = t & 3
            if t == 0:
                break
            dst.extend(src[ip: ip + t]); ip += t
            t = src[ip]; ip += 1

        while 1:
            t = src[ip]; ip += 1
            if t < 16:
                if t == 0:
                    t, ip = expand_zeroes(src, ip, 15)
                dst.extend(src[ip: ip + t + 3]); ip += t + 3
                t = src[ip]; ip += 1
            if t < 16:
                copy_earlier(dst, 1 + 0x0800 + (t >> 2) + (src[ip] << 2), 3); ip += 1
                t = t & 3
                if t == 0:
                    continue
                dst.extend(src[ip: ip + t]); ip += t
                t = src[ip]; ip += 1
            break


def read_xor32(src, p1, p2):
    v1 = src[p1] | (src[p1 + 1] << 8) | (src[p1 + 2] << 16) | (src[p1 + 3] << 24)
    v2 = src[p2] | (src[p2 + 1] << 8) | (src[p2 + 2] << 16) | (src[p2 + 3] << 24)
    return v1 ^ v2

clz_table = (
    32, 0, 1, 26, 2, 23, 27, 0, 3, 16, 24, 30, 28, 11, 0, 13, 4,
    7, 17, 0, 25, 22, 31, 15, 29, 10, 12, 6, 0, 21, 14, 9, 5,
    20, 8, 19, 18
)

def lzo1x_1_compress_core(src, dst, ti, ip_start, ip_len):
    dict_entries = [0] * 16384

    in_end = ip_start + ip_len
    ip_end = ip_start + ip_len - 20

    ip = ip_start
    ii = ip_start

    ip += (4 - ti) if ti < 4 else 0
    ip += 1 + ((ip - ii) >> 5)
    while 1:
        while 1:
            if ip >= ip_end:
                return in_end - (ii - ti)
            dv = src[ip: ip + 4]
            dindex = dv[0] | (dv[1] << 8) | (dv[2] << 16) | (dv[3] << 24)
            dindex = ((0x1824429d * dindex) >> 18) & 0x3fff
            m_pos = ip_start + dict_entries[dindex]
            dict_entries[dindex] = (ip - ip_start) & 0xffff
            if dv == src[m_pos: m_pos + 4]:
                break
            ip += 1 + ((ip - ii) >> 5)

        ii -= ti; ti = 0
        t = ip - ii
        if t != 0:
            if t <= 3:
                dst[-2] |= t
                dst.extend(src[ii: ii + t])
            elif t <= 16:
                dst.append(t - 3)
                dst.extend(src[ii: ii + t])
            else:
                if t <= 18:
                    dst.append(t - 3)
                else:
                    tt = t - 18
                    dst.append(0)
                    n, tt = divmod(tt, 255)
                    dst.extend("\x00" * n)
                    dst.append(tt)
                dst.extend(src[ii: ii + t])
                ii += t

        m_len = 4
        v = read_xor32(src, ip + m_len, m_pos + m_len)
        if v == 0:
            while 1:
                m_len += 4
                v = read_xor32(src, ip + m_len, m_pos + m_len)
                if ip + m_len >= ip_end:
                    break
                elif v != 0:
                    m_len += clz_table[(v & -v) % 37] >> 3
                    break
        else:
            m_len += clz_table[(v & -v) % 37] >> 3

        m_off = ip - m_pos
        ip += m_len
        ii = ip
        if m_len <= 8 and m_off <= 0x0800:
            m_off -= 1
            dst.append(((m_len - 1) << 5) | ((m_off & 7) << 2))
            dst.append(m_off >> 3)
        elif m_off <= 0x4000:
            m_off -= 1
            if m_len <= 33:
                dst.append(32 | (m_len - 2))
            else:
                m_len -= 33
                dst.append(32)
                n, m_len = divmod(m_len, 255)
                dst.extend("\x00" * n)
                dst.append(m_len)
            dst.append((m_off << 2) & 0xff)
            dst.append((m_off >> 6) & 0xff)
        else:
            m_off -= 0x4000
            if m_len <= 9:
                dst.append(0xff & (16 | ((m_off >> 11) & 8) | (m_len - 2)))
            else:
                m_len -= 9
                dst.append(0xff & (16 | ((m_off >> 11) & 8)))
                n, m_len = divmod(m_len, 255)
                dst.extend("\x00" * n)
                dst.append(m_len)
            dst.append((m_off << 2) & 0xff)
            dst.append((m_off >> 6) & 0xff)

def lzo1x_1_compress(s):
    src = bytearray(s)
    dst = bytearray()

    ip = 0
    l = len(s)
    t = 0

    dst.append(240)
    dst.append((l >> 24) & 0xff)
    dst.append((l >> 16) & 0xff)
    dst.append((l >>  8) & 0xff)
    dst.append( l        & 0xff)

    while l > 20 and t + l > 31:
        ll = min(49152, l)
        t = lzo1x_1_compress_core(src, dst, t, ip, ll)
        ip += ll
        l -= ll
    t += l

    if t > 0:
        ii = len(s) - t

        if len(dst) == 5 and t <= 238:
            dst.append(17 + t)
        elif t <= 3:
            dst[-2] |= t
        elif t <= 18:
            dst.append(t - 3)
        else:
            tt = t - 18
            dst.append(0)
            n, tt = divmod(tt, 255)
            dst.extend("\x00" * n)
            dst.append(tt)
        dst.extend(src[ii: ii + t])

    dst.append(16 | 1)
    dst.append(0)
    dst.append(0)

    return str(dst)


def modify_save(data, changes, endian=1):
    player = read_protobuf(unwrap_player_data(data))

    if changes.has_key("level"):
        level = int(changes["level"])
        lower = int(60 * (level ** 2.8) - 59.2)
        upper = int(60 * ((level + 1) ** 2.8) - 59.2)
        if player[3][0][1] not in range(lower, upper):
            player[3][0][1] = lower
        player[2] = [[0, int(changes["level"])]]

    if changes.has_key("skillpoints"):
        player[4] = [[0, int(changes["skillpoints"])]]

    if any(map(changes.has_key, ("money", "eridium", "seraph", "tokens"))):
        raw = player[6][0][1]
        b = StringIO(raw)
        values = []
        while b.tell() < len(raw):
            values.append(read_protobuf_value(b, 0))
        if changes.has_key("money"):
            values[0] = int(changes["money"])
        if changes.has_key("eridium"):
            values[1] = int(changes["eridium"])
        if changes.has_key("seraph"):
            values[2] = int(changes["seraph"])
        if changes.has_key("tokens"):
            values[4] = int(changes["tokens"])
        player[6][0] = [0, values]

    if changes.has_key("itemlevels"):
        if changes["itemlevels"]:
            level = int(changes["itemlevels"])
        else:
            level = player[2][0][1]
        for field_number in (53, 54):
            for field in player[field_number]:
                field_data = read_protobuf(field[1])
                is_weapon, item, key = unwrap_item(field_data[1][0][1])
                if item[4] > 1:
                    item = item[: 4] + [level, level] + item[6: ]
                    field_data[1][0][1] = wrap_item(is_weapon, item, key)
                    field[1] = write_protobuf(field_data)

    if changes.has_key("backpack"):
        size = int(changes["backpack"])
        sdus = int(math.ceil((size - 12) / 3.0))
        size = 12 + (sdus * 3)
        slots = read_protobuf(player[13][0][1])
        slots[1][0][1] = size
        player[13][0][1] = write_protobuf(slots)
        s = read_repeated_protobuf_value(player[36][0][1], 0)
        player[36][0][1] = write_repeated_protobuf_value(s[: 7] + [sdus] + s[8: ], 0)

    if changes.has_key("bank"):
        size = int(changes["bank"])
        sdus = int(min(255, math.ceil((size - 6) / 2.0)))
        size = 6 + (sdus * 2)
        if player.has_key(56):
            player[56][0][1] = size
        else:
            player[56] = [[0, size]]
        s = read_repeated_protobuf_value(player[36][0][1], 0)
        if len(s) < 9:
            s = s + (9 - len(s)) * [0]
        player[36][0][1] = write_repeated_protobuf_value(s[: 8] + [sdus] + s[9: ], 0)

    if changes.get("gunslots", "0") in "234":
        n = int(changes["gunslots"])
        slots = read_protobuf(player[13][0][1])
        slots[2][0][1] = n
        if slots[3][0][1] > n - 2:
            slots[3][0][1] = n - 2
        player[13][0][1] = write_protobuf(slots)

    if changes.has_key("unlocks"):
        unlocked, notifications = [], []
        if player.has_key(23):
            unlocked = map(ord, player[23][0][1])
        if player.has_key(24):
            notifications = map(ord, player[24][0][1])
        unlocks = changes["unlocks"].split(":")
        if "slaughterdome" in unlocks:
            if 1 not in unlocked:
                unlocked.append(1)
            if 1 not in notifications:
                notifications.append(1)
        if unlocked:
            player[23] = [[2, "".join(map(chr, unlocked))]]
        if notifications:
            player[24] = [[2, "".join(map(chr, notifications))]]
        if "truevaulthunter" in unlocks:
            if player[7][0][1] < 1:
                player[7][0][1] = 1

    return wrap_player_data(write_protobuf(player), endian)

def export_items(data, output):
    player = read_protobuf(unwrap_player_data(data))
    for i, name in ((41, "Bank"), (53, "Items"), (54, "Weapons")):
        content = player.get(i)
        if content is None:
            continue
        print >>output, "; " + name
        for field in content:
            raw = read_protobuf(field[1])[1][0][1]
            raw = replace_raw_item_key(raw, 0)
            code = "BL2(" + raw.encode("base64").strip() + ")"
            print >>output, code

def import_items(data, codelist, endian=1):
    player = read_protobuf(unwrap_player_data(data))

    to_bank = False
    for line in codelist.splitlines():
        line = line.strip()
        if line.startswith(";"):
            name = line[1: ].strip().lower()
            if name == "bank":
                to_bank = True
            elif name in ("items", "weapons"):
                to_bank = False
            continue
        elif line[: 4] + line[-1: ] != "BL2()":
            continue

        code = line[4: -1]
        try:
            raw = code.decode("base64")
        except binascii.Error:
            continue

        key = random.randrange(0x100000000) - 0x80000000
        raw = replace_raw_item_key(raw, key)
        if to_bank:
            field = 41
            entry = {1: [[2, raw]]}
        elif (ord(raw[0]) & 0x80) == 0:
            field = 53
            entry = {1: [[2, raw]], 2: [[0, 1]], 3: [[0, 0]], 4: [[0, 1]]}
        else:
            field = 53
            entry = {1: [[2, raw]], 2: [[0, 0]], 3: [[0, 1]]}

        player.setdefault(field, []).append([2, write_protobuf(entry)])

    return wrap_player_data(write_protobuf(player), endian)


def parse_args():
    usage = "usage: %prog [options] [source file] [destination file]"
    p = optparse.OptionParser()
    p.add_option(
        "-d", "--decode",
        action="store_true",
        help="read from a save game, rather than creating one"
    )
    p.add_option(
        "-e", "--export-items", metavar="FILENAME",
        help="save out codes for all bank and inventory items"
    )
    p.add_option(
        "-i", "--import-items", metavar="FILENAME",
        help="read in codes for items and add them to the bank and inventory"
    )
    p.add_option(
        "-j", "--json",
        action="store_true",
        help="read or write save game data in JSON format, rather than raw protobufs"
    )
    p.add_option(
        "-l", "--little-endian",
        action="store_true",
        help="change the output format to little endian, to write PC-compatible save files"
    )
    p.add_option(
        "-m", "--modify", metavar="MODIFICATIONS",
        help="comma separated list of modifications to make, eg money=99999999,eridium=99"
    )
    p.add_option(
        "-p", "--parse",
        action="store_true",
        help="parse the protocol buffer data further and generate more readable JSON"
    )
    return p.parse_args()

def main(options, args):
    if len(args) >= 2 and args[0] != "-" and args[0] == args[1]:
        print >>sys.stderr, "Cannot overwrite the save file, please use a different filename for the new save"
        return

    if len(args) < 1 or args[0] == "-":
        input = sys.stdin
    else:
        input = open(args[0], "rb")

    if len(args) < 2 or args[1] == "-":
        output = sys.stdout
    else:
        output = open(args[1], "wb")

    if options.little_endian:
        endian = 0
    else:
        endian = 1

    if options.modify is not None:
        changes = {}
        if options.modify:
            for m in options.modify.split(","):
                k, v = (m.split("=", 1) + [None])[: 2]
                changes[k] = v
        output.write(modify_save(input.read(), changes, endian))
    elif options.export_items:
        output = open(options.export_items, "w")
        export_items(input.read(), output)
    elif options.import_items:
        itemlist = open(options.import_items, "r")
        output.write(import_items(input.read(), itemlist.read(), endian))
    elif options.decode:
        savegame = input.read()
        player = unwrap_player_data(savegame)
        if options.json:
            data = read_protobuf(player)
            if options.parse:
                data = apply_structure(data, save_structure)
            player = json.dumps(data, encoding="latin1", sort_keys=True, indent=4)
        output.write(player)
    else:
        player = input.read()
        if options.json:
            data = json.loads(player, encoding="latin1")
            if not data.has_key("1"):
                data = remove_structure(data, invert_structure(save_structure))
            player = write_protobuf(data)
        savegame = wrap_player_data(player, endian)
        output.write(savegame)

if __name__ == "__main__":
    options, args = parse_args()
    try:
        main(options, args)
    except:
        print >>sys.stderr, (
            "Something went wrong, but please ensure you have the latest "
            "version from https://github.com/pclifford/borderlands2 before "
            "reporting a bug.  Information useful for a report follows:"
        )
        print >>sys.stderr, repr(sys.argv)
        raise
