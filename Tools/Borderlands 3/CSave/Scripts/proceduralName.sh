#!/bin/sh

for f in $1; do
	echo $f;
	SaveToProto $f
	SaveGenerate $f.proto $f.proto.edited << =EOF=
set name
$f
exit
=EOF=
	ProtoToSave $f.proto.edited $f
	rm $f.proto $f.proto.edited
done
