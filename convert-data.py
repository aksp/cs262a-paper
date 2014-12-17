#!/usr/bin/env python

import re
import sys
from math import log10

current_is_read = None
current_type = None

for line in sys.stdin:
  match = re.search(r'^(read|write) /(.*)$', line)
  if match:
    current_is_read = match.group(1) == 'read'
    current_type = match.group(2)
    continue

  match = re.search(r'^/benchmark/jsons/(number|size)_(\d+).json ([0-9.]+)(?: ([0-9.]+))?$', line)
  if match:
    x = float(match.group(2))
    if match.group(1) == 'size':
      x = log10(x)
    if match.group(4):
      assert not current_is_read
      with open('%s-%s-write.txt' % (current_type, match.group(1)), 'a') as f:
        f.write('%d %f\n' % (x, float(match.group(3))))
      with open('%s-%s-converge.txt' % (current_type, match.group(1)), 'a') as f:
        f.write('%d %f\n' % (x, float(match.group(4))))
    else:
      with open('%s-%s-%s.txt' % (current_type, match.group(1), 'read' if current_is_read else 'write'), 'a') as f:
        f.write('%d %f\n' % (x, float(match.group(3))))
    continue

  raise Exception("Invalid line: %s" % line)
