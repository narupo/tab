#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

def padrow(row, maxlen, pad=' '):
    """Set padding to cols"""
    for i in range(0, len(row)):
        row[i] = row[i].ljust(maxlen, pad)

def parserow(row):
    """Get result"""
    res = '| '
    rowlen = len(row)
    for i in range(0, rowlen-1):
        res += '{0} | '.format(row[i])
    if rowlen:
        res += '{0}'.format(row[rowlen-1])

    res += ' |\n'

    return res

def getmaxlens(rows):
    """Get most length in rows and cols"""
    maxrowlen = 0
    maxcollen = 0
    for r in rows:
        maxrowlen = max(maxrowlen, len(r))
        for c in r:
            maxcollen = max(maxcollen, len(c))
    return maxrowlen, maxcollen

def padrows(rows, maxrowlen, pad=''):
    """Padding rows"""
    for i in range(0, len(rows)):
        if len(rows[i]) < maxrowlen:
            for _ in range(0, maxrowlen-len(rows[i])):
                rows[i].append(pad)

def makeseparator(maxrowlen, maxcollen):
    s = ''
    for i in range(0, maxrowlen):
        s += '+'
        s += '-' * (maxcollen + 2)
    s += '+\n'
    return s

def parserows(rows):
    maxrowlen, maxcollen = getmaxlens(rows)
    padrows(rows, maxrowlen)

    """Parse row"""
    res = makeseparator(maxrowlen, maxcollen)
    for r in rows:
        padrow(r, maxcollen, ' ')
        res += parserow(r)
        res += makeseparator(maxrowlen, maxcollen)

    return res

def parse(txt, sep=','):
    rows = []
    lines = txt.split('\n')

    for line in lines:
        rows.append(line.split(sep))

    return parserows(rows)

def main(args):
    try:
        fin = sys.stdin
        res = parse(fin.read())
        print(res, end='')
        sys.stderr.flush()
        sys.stdout.flush()
    except BaseException as e:
        print(str(e), file=sys.stderr)
        raise e

if __name__ == '__main__':
    main(sys.argv)
