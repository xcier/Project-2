#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

import os
import sys
import subprocess

if True:
    print('This was just a utility I used when porting to Python 3, to compare')
    print('the outputs to the Python 2 version (to ensure that nothing was')
    print('subtly broken.  Really some unit tests would have been the long-term')
    print('better way to go, but whatever.  Anyway, not really for general use,')
    print('though I figured I would commit it anyway, in case I think of')
    print('something else that needs checking.')
    sys.exit(0)

class Test(object):

    games = ['bl2', 'tps']
    executables = {
        'bl2': {
            'two': '/home/pez/git/borderlands2-py2/bl2_save_edit.py',
            'three': '/home/pez/git/borderlands2/bl2_save_edit.py',
            },
        'tps': {
            'two': '/home/pez/git/borderlands2-py2/bltps_save_edit.py',
            'three': '/home/pez/git/borderlands2/bltps_save_edit.py',
            },
        }
    output_dir = 'output'
    suffix = {
            'two': '.2',
            'three': '.3',
        }

    def __init__(self, desc, input_file, args, text_output=False, restrict_game=False):
        self.desc = desc
        self.input_file = input_file
        self.args = args
        self.text_output = text_output
        self.restrict_game = restrict_game

    def run(self):
        for game in self.games:
            if self.restrict_game and game != self.restrict_game:
                print('{} {}: skipping'.format(game, self.desc))
                continue
            output_files = []
            output_data = []
            for version in ['two', 'three']:
                executable = self.executables[game][version]
                suffix = self.suffix[version]
                full_output = os.path.join(
                        self.output_dir,
                        '{}-{}{}'.format(game, self.desc, suffix),
                        )
                output_files.append(full_output)
                commandline = [executable]
                commandline.extend(self.args)
                commandline.append('{}-{}'.format(game, self.input_file))
                commandline.append(full_output)
                subprocess.run(commandline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                try:
                    if self.text_output:
                        with open(full_output, 'r') as df:
                            output_lines = []
                            for line in df.readlines():
                                output_lines.append(line.strip())
                            output_data.append(''.join(output_lines))
                    else:
                        with open(full_output, 'rb') as df:
                            output_data.append(df.read())
                except FileNotFoundError as e:
                    output_data.append('{} {} result does not exist'.format(game, executable))
            if output_data[0] != output_data[1]:
                print('{} {}: files {} and {} do not match'.format(
                    game,
                    self.desc,
                    output_files[0],
                    output_files[1]))
            else:
                print('{} {}: good!'.format(game, self.desc))
                os.unlink(output_files[0])
                os.unlink(output_files[1])

# First clear out our output directory
print('Cleaning output directory')
for filename in os.listdir(Test.output_dir):
    os.unlink(os.path.join(Test.output_dir, filename))

tests = [
        Test('noargs', 'toptier.sav', []),
        Test('copy', 'toptier.sav', ['-o', 'savegame']),
        Test('decoded', 'toptier.sav', ['-o', 'decoded']),
        Test('decodedjson', 'toptier.sav', ['-o', 'decodedjson'], text_output=True),
        Test('json', 'toptier.sav', ['-o', 'json'], text_output=True),
        Test('items', 'toptier.sav', ['-o', 'items'], text_output=True),
        Test('jsoninput', 'toptier.json', ['-j']),
        Test('decodedjsoninput', 'toptier_decoded.json', ['-j']),
        # Can't actually test this one, item IDs are randomly generated on insert.
        # Manually made sure this works by hardcoding IDs, though.
        #Test('itemimport', 'early.sav', ['-i', 'items.txt']),
        Test('charname', 'early.sav', ['--name', 'Fred']),
        Test('saveid', 'early.sav', ['--save-game-id', '42']),
        Test('level', 'early.sav', ['--level', '42']),
        Test('money', 'early.sav', ['--money', '42000']),
        Test('eridium', 'early.sav', ['--eridium', '42'], restrict_game='bl2'),
        Test('moonstone', 'early.sav', ['--moonstone', '42'], restrict_game='tps'),
        Test('seraph', 'early.sav', ['--seraph', '42'], restrict_game='bl2'),
        Test('torgue', 'early.sav', ['--torgue', '42'], restrict_game='bl2'),
        Test('itemlevels', 'toptier.sav', ['--itemlevels', '2']),
        Test('backpack', 'early.sav', ['--backpack', '30']),
        Test('bank', 'early.sav', ['--bank', '20']),
        Test('gunslots', 'early.sav', ['--gunslots', '4']),
        Test('slaughter', 'early_noslaughterdome.sav', ['--unlock', 'slaughterdome'], restrict_game='bl2'),
        Test('tvhm', 'early.sav', ['--unlock', 'tvhm']),
        # This test can't be manually tested without adding in the same Challenge
        # sorting on the py2 version which we now do in py3.  (Not committing that
        # on the py2 branch for Reasons.)
        #Test('challenges', 'early.sav', ['--unlock', 'challenges']),
        Test('ammo', 'early.sav', ['--unlock', 'ammo']),
        Test('zerochallenge', 'early.sav', ['--challenges', 'zero']),
        Test('maxchallenge', 'early.sav', ['--challenges', 'max']),
        Test('bonuschallenge', 'early.sav', ['--challenges', 'bonus']),
        Test('maxammo', 'early.sav', ['--maxammo']),
        ]

for test in tests:
    test.run()
