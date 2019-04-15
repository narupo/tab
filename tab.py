#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys
import io


class Row:
    def __init__(self):
        self.cols = []
        self.type = ''

    def append(self, col):
        self.cols.append(col)

    def clear(self):
        self.cols = []

    def copy(self):
        r = Row()
        r.cols = self.cols[:]
        return r

    def conv(self):
        if self.type == 'end':
            return ''
        else:
            buf = ''
            total = 0
            for c in self.cols:
                clen = len(c.conv())
                if c.type == 'end':
                    buf += ('-'*(clen))
                elif c.type == 'begin':
                    buf += ('-'*(clen-2)) + '+'
                else:
                    buf += ('-'*(clen-1)) + '+'
            buf += '\n'
            return buf


class Col:
    def __init__(self):
        self.text = ''
        self.type = ''
        self.maxlen = 0

    def append(self, c):
        self.text += c

    def clear(self):
        self.text = ''

    def copy(self):
        c = Col()
        c.text = self.text
        return c

    def strip(self):
        self.text = self.text.strip()

    def len(self):
        return len(self.text)

    def conv(self):
        if self.type == 'begin':
            return self.text.center(self.maxlen) + ' | '
        elif self.type == 'end':
            return self.text.center(self.maxlen) + '\n'
        else:
            return self.text.center(self.maxlen) + ' | '


class Table:
    def __init__(self):
        self.rows = []
        self.print_rows = []
        self.maxlen = 0

    def append(self, row):
        self.rows.append(row)

    def parse(self):
        self.maxlen = 0
        for r in self.rows:
            for c in r.cols:
                self.maxlen = max(c.len(), self.maxlen)

        self.print_rows = self.rows[:]
        self.print_rows[0].type = 'begin'
        self.print_rows[-1].type = 'end'
        i = 0
        while i < len(self.print_rows):
            self.print_rows[i].cols[0].type = 'begin'
            self.print_rows[i].cols[-1].type = 'end'
            j = 0
            while j < len(self.print_rows[i].cols):
                self.print_rows[i].cols[j].maxlen = self.maxlen
                j += 1
            i += 1

    def print(self):
        for r in self.print_rows:
            for c in r.cols:
                text = c.conv()
                print(text, end='')
            text = r.conv()
            print(text, end='')


class Parser:
    def parse(self, src):
        t = Table()
        r = Row()
        c = Col()
        for el in src:
            if el == '|':
                c.strip()
                r.append(c.copy())
                c.clear()
            elif el == '\n':
                c.strip()
                r.append(c.copy())
                c.clear()
                t.append(r.copy())
                r.clear()
            else:
                c.append(el)
        return t


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

    src = sys.stdin.read()
    table = Parser().parse(src)
    table.parse()
    table.print()

    sys.exit(0)


if __name__ == '__main__':
    main()
