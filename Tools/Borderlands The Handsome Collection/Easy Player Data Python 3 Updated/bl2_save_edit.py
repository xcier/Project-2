#!/usr/bin/env python3

import sys
import traceback
from borderlands.bl2 import AppBL2

if __name__ == "__main__":
    try:
        app = AppBL2(sys.argv[1:])
        app.run()
    except Exception as e:
        print('Something went wrong, but please ensure you have the latest', file=sys.stderr)
        print('version from https://github.com/apocalyptech/borderlands2 before', file=sys.stderr)
        print('reporting a bug.  Information useful for a report follows:', file=sys.stderr)
        print('', file=sys.stderr)
        print(repr(sys.argv), file=sys.stderr)
        print('', file=sys.stderr)
        traceback.print_exc(None, sys.stderr)
        sys.exit(1)
