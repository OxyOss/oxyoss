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

'Check a guess against the hashed entries in a `known_hosts` file.'

import base64
import hashlib
import hmac
import itertools
import os.path
import sys


VERBOSE = 0


def parse_line(line):
    """
    >>> line = '|1|0YP15ycxoYMonCwcTo+zg9HMR3s=|GapoIyXQk7XJ+j3Kcg6yGC16Y/Y= ssh-rsa ...'
    >>> info = parse_line(line)
    >>> info['hashed']
    '|1|0YP15ycxoYMonCwcTo+zg9HMR3s=|GapoIyXQk7XJ+j3Kcg6yGC16Y/Y='
    >>> info['?']
    1
    >>> base64.b64encode(info['key'])
    '0YP15ycxoYMonCwcTo+zg9HMR3s='
    >>> base64.b64encode(info['name'])
    'GapoIyXQk7XJ+j3Kcg6yGC16Y/Y='
    """
    if not line.startswith('|'):
        raise ValueError(line)
    host = line.split()[0]
    fields = host.split('|')
    assert len(fields) == 4, '%d fields in %s' % (len(fields), host)
    assert fields[0] == '', host
    assert fields[1] == '1', host
    q = int(fields[1])
    key = base64.b64decode(fields[2])
    name = base64.b64decode(fields[3])
    return {'?': q, 'key': key, 'name': name, 'hashed': host}

def read_known_hosts(stream=None):
    """
    >>> import StringIO
    >>> stream = StringIO.StringIO(
    ...     '|1|0YP15ycxoYMonCwcTo+zg9HMR3s=|GapoIyXQk7XJ+j3Kcg6yGC16Y/Y= ssh-rsa ...\\n')
    >>> entries = read_known_hosts(stream)
    >>> for key in entries.keys():
    ...     print base64.b64encode(key)
    0YP15ycxoYMonCwcTo+zg9HMR3s=
    >>> info = entries[base64.b64decode('0YP15ycxoYMonCwcTo+zg9HMR3s=')]
    >>> info['hashed']
    '|1|0YP15ycxoYMonCwcTo+zg9HMR3s=|GapoIyXQk7XJ+j3Kcg6yGC16Y/Y='
    """
    if not stream:
        path = os.path.expanduser(os.path.join('~', '.ssh', 'known_hosts'))
        stream = open(path, 'r')
    entries = {}
    for i,line in enumerate(stream):
        try:
            info = parse_line(line)
        except ValueError:
            continue
        info['line'] = i
        entries[info['key']] = info
    return entries

def match_guess(name, entries):
    """
    >>> line = '|1|0YP15ycxoYMonCwcTo+zg9HMR3s=|GapoIyXQk7XJ+j3Kcg6yGC16Y/Y= ssh-rsa ...'
    >>> info = parse_line(line)
    >>> entries = {info['key']: info}
    >>> match_guess('wrong', entries)
    >>> match = match_guess('einstein', entries)
    >>> match == info
    True
    """
    for key,info in entries.items():
        h = hmac.new(info['key'], name, hashlib.sha1)
        if h.digest() == info['name']:
            return info

def ip_glob_entries(ip_glob):
    """
    >>> list(ip_glob_entries('192.168.0.*'))  # doctest: +ELLIPSIS
    ['192.168.0.0', '192.168.0.1', ..., '192.168.0.255']
    >>> list(ip_glob_entries('192.168.*.*'))  # doctest: +ELLIPSIS
    ['192.168.0.0', '192.168.0.1', ..., '192.168.255.255']
    """
    values = []
    for field in ip_glob.split('.'):
        if field == '*':
            value = [str(x) for x in range(256)]
        else:
            value = [field]
        values.append(value)
    for selection in selections(values):
        yield '.'.join(selection)

def alphanum_entries(min_length=1, max_length=8, chars=None):
    """
    >>> list(alphanum_entries(max_length=3, chars=['a', 'b']))
    ... # doctest: +ELLIPSIS
    ['a', 'b', 'aa', 'ab', 'ba', 'bb', 'aaa', 'aab', ..., 'bbb']
    >>> list(alphanum_entries(min_length=3, max_length=3))
    ... # doctest: +ELLIPSIS
    ['aaa', 'aab', 'aac', ..., '999', '...']
    """
    if chars == None:
        chars = [chr(x) for x in range(ord('a'), ord('z')+1)]
        chars.extend([chr(x) for x in range(ord('0'), ord('9')+1)])
        chars.extend(['.'])
    for length in range(min_length, max_length+1):
        if VERBOSE >= 1:
            sys.stderr.write('generate alpha-nums of length %d (max %d)\n' %
                             (length, max_length))
            sys.stderr.flush()
        for selection in selections([chars for i in range(length)]):
            yield ''.join(selection)

def selections(values):
    """
    >>> list(selections(values=[[0,1,2], [3], [4,5]]))
    [[0, 3, 4], [0, 3, 5], [1, 3, 4], [1, 3, 5], [2, 3, 4], [2, 3, 5]]
    """
    index = [0]*len(values)
    while True:
        yield [values[i][j] for i,j in enumerate(index)]
        index[-1] += 1
        for i in range(len(values), 0, -1):  # carry, if necessary
            i -= 1  # convert to [len(values)-1, ..., 0]
            j = index[i]
            if j >= len(values[i]):
                if i == 0:
                    return
                elif i == 1 and VERBOSE >= 2:
                    sys.stderr.write('selection completed %d of %d\n' %
                                     (index[0], len(values[0])))
                    sys.stderr.flush()
                index[i] = 0
                index[i-1] += 1


if __name__ == '__main__':
    from argparse import ArgumentParser, Action

    class CountAction (Action):
        def __call__(self, parser, namespace, values, option_string=None):
            value = getattr(namespace, self.dest)
            if value is None:
                value = 0
            setattr(namespace, self.dest, value + 1)

    p = ArgumentParser(description=__doc__)
    p.add_argument('names', metavar='NAME', type=unicode, nargs='*',
                   help='a guessed host name or IP')
    p.add_argument('--known-hosts', dest='known_hosts', type=unicode,
                   help='alternate path to known_hosts file')
    p.add_argument('--ip', metavar='GLOB', dest='ip_glob', type=unicode,
                   help="IP glob (e.g. '192.168.*.*')")
    p.add_argument('--alphanum', metavar='LENGTH', dest='max_an_len', type=int,
                   help='scan all alpha-numeric names up to this max length')
    p.add_argument('-v', '--verbose', dest='verbose', type=int, nargs=0,
                   action=CountAction, help='increment verbosity')

    args = p.parse_args()

    VERBOSE = args.verbose or 0

    stream = None
    if args.known_hosts:
        stream = open(args.known_hosts, 'r')

    entries = read_known_hosts(stream)

    if args.known_hosts:
        stream.close()

    names = args.names

    if args.ip_glob:
        names = itertools.chain(names, ip_glob_entries(args.ip_glob))

    if args.max_an_len:
        names = itertools.chain(names, alphanum_entries(
                max_length=args.max_an_len))

    for name in names:
        if VERBOSE >= 3:
            sys.stderr.write('check %s\n' % name)
            sys.stderr.flush()
        match = match_guess(name, entries)
        if match:
            print '%s %s (line %d)' % (name, match['hashed'], match['line']+1)
