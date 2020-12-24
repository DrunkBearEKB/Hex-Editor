import curses
import sys
from tkinter import Tk, filedialog
from watchdog.observers import Observer
from backend.board import Board
from backend.file_changing_handler import FileChangingHandler


class Console:
    def __init__(self, height=16):
        self._amount_width = 16
        self._amount_height = height

        self._board = Board(self._amount_width, self._amount_height)
        self._encoding = 'ascii'
        self._separator = ' | '

        self._file = None
        self._cursor = 0
        self._file_changing_handler = None
        self._observer = None

        self._std_src = curses.initscr()
        curses.curs_set(False)
        curses.noecho()
        curses.raw()

        self._std_src.nodelay(False)

    def start(self):
        curses.resize_term(self._amount_height + 4, 109)  # 108

        while True:
            try:
                key = self._std_src.getkey().encode('ascii')

                if key == b'\x11':
                    curses.endwin()
                    curses.curs_set(True)
                    curses.echo()
                    sys.exit(0)
                elif key == b'\x0f':
                    Tk().withdraw()
                    try:
                        self._file = filedialog.askopenfilename()
                        self._cursor = 0
                        self.__start_observer()
                    except FileNotFoundError:
                        continue
                    self.update_all()
                elif key == b'w':
                    if self._cursor != 0:
                        self._cursor -= self._amount_width
                        self.update_all()
                elif key == b'\x17':
                    if self._cursor != 0:
                        self._cursor -= self._amount_width * \
                                        self._amount_height
                        if self._cursor < 0:
                            self._cursor = 0
                        self.update_all()
                elif key == b's':
                    self._cursor += self._amount_width
                    self.update_all()
                elif key == b'\x13':
                    self._cursor += self._amount_width * self._amount_height
                    self.update_all()

            except Exception:
                continue

    def update_all(self, *args, **kwargs):
        self._board.update(self._file, self._encoding, self._cursor)

        self._std_src.addstr(0, 0, '+' + '—' * 106 + '+')
        self._std_src.addstr(1, 0, '| ' +
                             self._file + ' ' * (105 - len(self._file)) + '|')
        self._std_src.addstr(2, 0, '+' + '—' * 16 + '+' + '—' * 13 + '+' +
                             '—' * 13 + '+' + '—' * 13 + '+' + '—' * 13 + '+' +
                             '—' * 33 + '+')

        for i in range(self._amount_height):
            _str = '| ' + self._board.indexes[i] + self._separator + \
                  ' '.join(str(j) for j in self._board.bytes[i][:4]) + \
                  self._separator + \
                  ' '.join(str(j) for j in self._board.bytes[i][4:8]) + \
                  self._separator + \
                  ' '.join(str(j) for j in self._board.bytes[i][8:12]) + \
                  self._separator + \
                  ' '.join(str(j) for j in self._board.bytes[i][12:16]) + \
                  self._separator + \
                  ' '.join(str(j) for j in self._board.chars[i]) + ' |'
            self._std_src.addstr(i + 3, 0, _str)
        self._std_src.addstr(2 + self._amount_height + 1, 0,
                             '+' + '—' * 16 +
                             '+' + '—' * 13 + '+' + '—' * 13 + '+' +
                             '—' * 13 + '+' + '—' * 13 + '+' + '—' * 33 + '+')
        self._std_src.refresh()

    def __start_observer(self):
        self._file_changing_handler = FileChangingHandler(self, self._file)
        self._observer = Observer()
        self._observer.schedule(
            self._file_changing_handler,
            path=f'{self._file[:self._file.rindex("/")]}',
            recursive=False)
        self._observer.start()
