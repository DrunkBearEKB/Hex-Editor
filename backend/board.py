#!/usr/bin/env python3

from backend.log.commands import Command
from backend.log.log import Log


class Board:
    def __init__(self, width, height, len_index=14):
        self._list_indexes = None
        self._list_bytes = None
        self._list_chars = None
        self._width = width
        self._height = height
        self._len_index = len_index

    def update(self, file_name_or_content, encoding, index_start, log=Log(),
               not_file=False):
        self._list_indexes = list()
        self._list_bytes = list()
        self._list_chars = list()

        if not_file:
            content = self.get_content(log, index_start)
        else:
            content = self.get_content_from_file(file_name_or_content, log,
                                                 index_start)

        counter_lines = 0
        point = index_start // 16
        for index in range(0, len(content), self._width):
            _index = str(hex(point % 65536))[2:]
            _index = '0' * (self._len_index - len(_index)) + _index
            self._list_indexes.append(_index)
            point += 1

            line = content[index:index + self._width]
            self._list_bytes.append(list())
            self._list_chars.append(list())

            counter_chars = 0
            for symbol in line:
                self._list_bytes[-1].append('{:02X} '.format(symbol)[:2])

                if 32 <= symbol < 127:
                    self._list_chars[-1].append(
                        str(chr(symbol).encode(encoding=encoding))[2])
                else:
                    self._list_chars[-1].append('.')
                counter_chars += 1

            if counter_chars != self._width:
                for i in range(self._width - counter_chars):
                    self._list_bytes[-1].append('00')
                    self._list_chars[-1].append('.')

            counter_lines += 1

        if counter_lines != self._height:
            for index in range(counter_lines, self._height):
                _index = hex(index_start // self._width + index)[2:]
                _index = '0' * (self._len_index - len(_index)) + _index
                self._list_indexes.append(_index)

                self._list_bytes.append(list())
                self._list_chars.append(list())
                for i in range(self._width):
                    self._list_bytes[-1].append('00')
                    self._list_chars[-1].append('.')

        if not_file:
            return len(content)

    @property
    def indexes(self):
        return self._list_indexes

    @property
    def bytes(self):
        return self._list_bytes

    @property
    def chars(self):
        return self._list_chars

    def get_content_from_file(self, file_name, log, index_start, amount=None):
        if amount is None:
            log = log.get_log_between_indexes(
                index_start, index_start + self._width * self._height - 1)
        else:
            if amount != -1:
                log = log.get_log_between_indexes(
                    index_start, index_start + amount - 1)

        with open(file_name, mode='rb') as file:
            if amount is None:
                _amount = self._width * self._height
            elif amount != -1:
                _amount = amount
            else:
                _amount = None

            file.seek(index_start)

            if _amount is None:
                result = file.read()
            else:
                result = file.read(_amount)

            _len = len(log)
            for i in range(_len):
                log_line = log.pop_first()
                log.append(log_line, change=False)

                if log_line.command == Command.INSERT:
                    if len(result[:log_line.index]) == log_line.index:
                        result = result[:log_line.index] + \
                                 bytes([int(log_line.value_hex_1, 16)]) + \
                                 result[log_line.index:]
                    else:
                        result = \
                            result[:log_line.index] + \
                            (log_line.index -
                             len(result[:log_line.index])) * b'\x00' + \
                            bytes([int(log_line.value_hex_1, 16)])

                elif log_line.command == Command.REFACTOR:
                    if len(result[:log_line.index]) == log_line.index:
                        result = result[:log_line.index] + \
                                 bytes([int(log_line.value_hex_2, 16)]) + \
                                 result[log_line.index + 1:]
                    else:
                        result = \
                            result[:log_line.index] + \
                            (log_line.index -
                             len(result[:log_line.index])) * b'\x00' + \
                            bytes([int(log_line.value_hex_2, 16)])
                elif log_line.command == Command.DELETE:
                    if len(result[:log_line.index]) == log_line.index:
                        result = result[:log_line.index] + \
                                 result[log_line.index + 1:]
                    else:
                        result = result[:log_line.index] + \
                                 (log_line.index -
                                  len(result[:log_line.index])) * b'\x00'

            if _amount is not None:
                if len(result) < _amount:
                    result += file.read(_amount - len(result))
                elif len(result) > _amount:
                    result = result[:_amount - len(result)]

        return result

    def get_content(self, log, index_start, amount=None):
        amount = self._width * self._height if amount is None else amount
        content = b'\x00' * amount

        log = log.get_log_between_indexes(
            index_start, index_start + amount - 1)

        _len = len(log)
        for i in range(_len):
            log_line = log.pop_first()
            _ind = log_line.index
            log.append(log_line, change=False)

            if log_line.command == Command.INSERT:
                if len(content[:_ind]) == _ind:
                    content = content[:_ind] + \
                              bytes([int(log_line.value_hex_1, 16)]) + \
                              content[_ind:]
                else:
                    content = content[:_ind] + \
                              (_ind - len(content[:_ind])) * b'\x00' + \
                              bytes([int(log_line.value_hex_1, 16)])

            elif log_line.command == Command.REFACTOR:
                if len(content[:_ind]) == _ind:
                    content = content[:_ind] + \
                              bytes([int(log_line.value_hex_2, 16)]) + \
                              content[_ind + 1:]
                else:
                    content = content[:_ind] + \
                              (_ind - len(content[:_ind])) * b'\x00' + \
                              bytes([int(log_line.value_hex_2, 16)])
            elif log_line.command == Command.DELETE:
                if len(content[:_ind]) == _ind:
                    content = content[:_ind] + \
                             content[_ind + 1:]
                else:
                    content = content[:_ind] + \
                              (_ind - len(content[:_ind])) * b'\x00'

        if len(content) < amount:
            result = content + (amount - len(content)) * b'\x00'
        elif len(content) > amount:
            result = content[:amount - len(content)]
        else:
            result = content

        return result
