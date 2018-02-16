#!/usr/bin/python

import os
import sys
import json
import jsonschema

##
def main(args=None):
  if args is None:
    args = sys.argv[1:]
  #
  if (len(args) > -1):
    home = os.path.dirname(os.path.realpath(__file__))
    print(json.dumps({"detected" : 0}))
  else:
    print('Invalid input parameters')
    sys.exit(1)

if __name__ == "__main__":
    main()
