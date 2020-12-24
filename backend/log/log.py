from backend.log.commands import Command
from backend.log.log_line import LogLine


class Log:
    def __init__(self):
        self._log = list()

    def append(self, *args, change=True):
        if len(args) == 1 and type(args[0]) == LogLine:
            self._log.append(args[0])

            if not change:
                return

            if self._log[-1].command == Command.INSERT:
                _index = self._log[-1].index
                for index, value in enumerate(self._log):
                    if value.index > _index:
                        self._log[index].index += 1
            elif self._log[-1].command == Command.DELETE:
                _index = self._log[-1].index
                for index, value in enumerate(self._log):
                    if value.index < _index:
                        self._log[index].index -= 1
            else:
                pass

        elif len(args) == 6:
            log_line = LogLine(args[0], args[1], args[2],
                               args[3], args[4], args[5])

            if not change:
                return

            if self._log[-1].command == Command.INSERT:
                _index = self._log[-1].index
                for index, value in enumerate(self._log):
                    if value.index >= _index:
                        self._log[index].index += 1
            elif self._log[-1].command == Command.DELETE:
                _index = self._log[-1].index
                for index, value in enumerate(self._log):
                    if value.index < _index:
                        self._log[index].index -= 1

            self._log.append(log_line)

        else:
            raise ValueError()

    def pop_first(self):
        log_line = self._log.pop(0)

        if log_line.command == Command.INSERT:
            _index = log_line.index
            for index, value in enumerate(self._log):
                if value.index > _index:
                    self._log[index].index -= 1
        elif log_line.command == Command.DELETE:
            _index = log_line.index
            for index, value in enumerate(self._log):
                if value.index < _index:
                    self._log[index].index += 1

        return log_line

    def pop_last(self):
        log_line = self._log.pop(-1)

        if log_line.command == Command.INSERT:
            _index = log_line.index
            for index, value in enumerate(self._log):
                if value.index > _index:
                    self._log[index].index -= 1
        elif log_line.command == Command.DELETE:
            _index = log_line.index
            for index, value in enumerate(self._log):
                if value.index < _index:
                    self._log[index].index += 1

        return log_line

    def inverse(self):
        result = Log()

        for log_line in self._log:
            if log_line.command == Command.INSERT:
                command = Command.DELETE
            elif log_line.command == Command.DELETE:
                command = Command.INSERT
            else:
                command = Command.REFACTOR

            if log_line.command == Command.INSERT or \
                    log_line.command == Command.DELETE:
                log_line_new = LogLine(command, log_line.index,
                                       log_line.value_hex_1,
                                       log_line.value_chr_1)
            else:
                log_line_new = LogLine(command, log_line.index,
                                       log_line.value_hex_2,
                                       log_line.value_chr_2,
                                       log_line.value_hex_1,
                                       log_line.value_chr_1)

            result.append(log_line_new, change=False)

        return result

    def clear(self):
        self._log.clear()

    def get_sorted(self, key: callable = lambda x: x):
        return sorted(self._log, key=key)

    @property
    def list(self):
        return self._log

    def get_log_between_indexes(self, index_start, index_end):
        result = Log()

        for log_line in self._log:
            if index_start <= log_line.index <= index_end:
                result.append(
                    log_line.copy(index=log_line.index - index_start),
                    change=False)

        return result

    def __iter__(self):
        for value in self._log:
            yield value

    def __getitem__(self, index: int):
        return self._log[index]

    def __len__(self):
        return len(self._log)

    def __str__(self):
        return '\n'.join(str(j) for j in self._log)
