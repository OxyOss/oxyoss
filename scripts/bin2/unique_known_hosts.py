#!/usr/bin/env python
#
# Copyright (C) 2011 W. Trevor King <wking@drexel.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

"""Sort a `known_hosts` file by public key.

This makes it easier to associate entries in your `known_hosts` file,
which may have separate, hashed entries for `server`,
`server.example.net`, and `123.456.789.123`.

usage: unique_known_hosts.py path/to/known_hosts
"""

import os.path
import sys


known_hosts = os.path.expanduser(os.path.join('~', '.ssh', 'known_hosts'))
if len(sys.argv) > 1:
    known_hosts = sys.argv[1]

keys = {}

for line in open(known_hosts, 'r'):
    name,key = line.split(' ', 1)
    if key in keys:
        keys[key].append(name)
    else:
        keys[key] = [name]

for key,names in keys.items():
    print '%s  %s' % (key, '\n  '.join(names))
