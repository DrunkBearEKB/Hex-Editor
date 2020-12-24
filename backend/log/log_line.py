#!/usr/bin/env python3

from backend.log.commands import Command


class LogLine:
    def __init__(self, command: Command, index: int,
                 value_hex_1=None, value_chr_1=None,
                 value_hex_2=None, value_chr_2=None):
        self._command = command
        self._index = index
        self._value_hex_1 = value_hex_1
        self._value_chr_1 = value_chr_1
        self._value_hex_2 = value_hex_2
        self._value_chr_2 = value_chr_2

    def copy(self, index=None):
        result = LogLine(self._command,
                         self._index if index is None else index,
                         self._value_hex_1,
                         self._value_chr_1,
                         self._value_hex_2,
                         self._value_chr_2)

        return result

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, value):
        if type(value) != Command:
            raise ValueError()
        self._command = value

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        if type(value) != int:
            raise ValueError()
        self._index = value

    @property
    def value_hex_1(self):
        return self._value_hex_1

    @value_hex_1.setter
    def value_hex_1(self, value):
        if type(value) != str:
            raise ValueError()
        self.value_hex_1 = value

    @property
    def value_chr_1(self):
        return self._value_chr_1

    @value_chr_1.setter
    def value_chr_1(self, value):
        if type(value) != str:
            raise ValueError()
        self.value_chr_1 = value

    @property
    def value_hex_2(self):
        return self._value_hex_2

    @value_hex_2.setter
    def value_hex_2(self, value):
        if type(value) != str:
            raise ValueError()
        self.value_hex_2 = value

    @property
    def value_chr_2(self):
        return self._value_chr_2

    @value_chr_2.setter
    def value_chr_2(self, value):
        if type(value) != str:
            raise ValueError()
        self.value_chr_2 = value

    def __lt__(self, other):
        return self._index < other.index

    def __le__(self, other):
        return self._index <= other.index

    def __gt__(self, other):
        return self._index > other.index

    def __ge__(self, other):
        return self._index >= other.index

    def __str__(self):
        return f'(command="{self._command}", ' \
               f'index={self.index}, ' \
               f'value_hex_1="{self._value_hex_1}", ' \
               f'value_chr_1="{self._value_chr_1}", ' \
               f'value_hex_2="{self._value_hex_2}", ' \
               f'value_chr_2="{self._value_chr_2}")'
