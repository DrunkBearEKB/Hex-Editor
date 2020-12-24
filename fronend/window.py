import ast
import os
import struct
import urllib.error
import urllib.request
import webbrowser

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, qApp, QFrame, \
    QLabel, QLineEdit, QDesktopWidget, QPushButton, QApplication, QMessageBox

from backend.board import Board
from backend.file_changing_handler import FileChangingHandler
from watchdog.observers import Observer
from backend.log.commands import Command
from backend.log.log import Log
from backend.log.log_line import LogLine


class Window(QMainWindow):
    def __init__(self, mode_edit=True):
        super().__init__()

        # ===========================================================
        # Main definitions
        self._amount_width = 16
        self._amount_height = 16

        self._win_width = 1107
        self._win_height = 662  # 609 - without bottom frame
        self._encoding = 'ascii'
        self._log = Log()
        self._log_temp = Log()
        self._board = Board(self._amount_width, self._amount_height, 13)
        self._mode_edit = mode_edit

        self._font_name = 'Consolas'  # Calibri Terminus Consolas

        # ===========================================================
        # Widgets definitions
        self._frame_top = None
        self._frame_btn_open = None
        self._flag_frame_btn_open = False

        self._frame_left = None
        self._labels_frame_left = dict()

        self._list_frames_center = list()
        self._list_entries_center = list()
        self._dict_entries_center = dict()
        self._list_texts_center = list()

        self._list_frame_right = None
        self._list_entries_right = list()
        self._dict_entries_right = dict()
        self._list_texts_right = list()

        self._frame_bottom = None

        # ===========================================================
        # File definitions
        self._file = (None, None, None)
        self._text_abstract = b''
        self._cursor = 0
        self._cursor_max = 0
        self._selected = list()
        self._selected_values = list()
        self._label_file = None
        self._label_file_max_len = 83
        self._flag_changed = False
        self._file_changing_handler = None
        self._observer = None
        self.position = None

        # ===========================================================
        # Color definitions
        self._color_bg_menu = 'rgb(64, 64, 64)'
        self._color_bg_menu_temp = 'rgb(48, 48, 48)'
        self._color_bg_text = 'rgb(32, 32, 32)'
        self._color_bg_text_selected = 'rgb(52, 52, 52)'
        self._color_font_text = 'rgb(172, 172, 172)'  # 'white'
        self._color_labels_text = 'grey'
        self._color_entering_widget = '#acacac'

        self.__initui()

    def __initui(self):
        screen_size = QDesktopWidget().screenGeometry()
        self.setGeometry((screen_size.width() - self._win_width) // 2,
                         (screen_size.height() - self._win_height) // 2,
                         self._win_width, self._win_height)
        self.setWindowTitle('Hex Editor')
        self.setWindowIcon(QIcon('resources/icon.png'))
        self.installEventFilter(self)

        QtWidgets.QToolTip.setFont(
            QFont(self._font_name, 2, QFont.StyleItalic))

        self.setFixedSize(self._win_width, self._win_height)
        self.setAcceptDrops(True)

        self.__init_style_sheets()

        self.__create_frame_top()
        self.__create_frame_bottom()

        self.__create_frame_left()
        self.__create_frame_center()
        self.__create_frame_right()

        self.__create_short_cuts()
        self.__create_finish()

    def __init_style_sheets(self):
        self.style_sheet_button_top = \
            f'image: url(menu.png);\n' \
            f'color: {self._color_font_text};\n' \
            f'background-color: {self._color_bg_menu};\n' \
            f'font: bold 16pt "{self._font_name}";\n' \
            f'border: none;'

        self.style_sheet_label_file = \
            f'background-color: {self._color_bg_menu};\n' \
            f'color: {self._color_font_text};\n' \
            f'font: 12pt "{self._font_name}";'

        self.style_sheet_label_left = \
            f'background-color: {self._color_bg_text};\n' \
            f'color: {self._color_font_text};\n' \
            f'font: 12pt "{self._font_name}";'

        self.style_sheet_line_edit = \
            f'background-color: {self._color_bg_text};\n' \
            f'color: {self._color_font_text};\n' \
            f'font: 12pt "{self._font_name}";\n' \
            f'border: none;'

        self.style_sheet_line_edit_selected = \
            f'background-color: {self._color_bg_text_selected};\n' \
            f'color: {self._color_font_text};\n' \
            f'font: 12pt "{self._font_name}";\n' \
            f'border: none;'

        self.style_sheet_button_temp = \
            f'color: {self._color_font_text};\n' \
            f'background-color: {self._color_bg_menu_temp};\n' \
            f'font: bold 12pt "{self._font_name}";\n' \
            f'border: none;'

    def __create_frame_top(self):
        _height = 52

        self._frame_top = QFrame(self)
        self._frame_top.acceptDrops()
        self._frame_top.setGeometry(0, 0, self._win_width, _height)
        self._frame_top.setStyleSheet(
            f'background-color: {self._color_bg_menu};')

        _dx = 10
        _size = _height - 2 * _dx

        self.btn_open = QPushButton(self._frame_top)
        self.btn_open.setGeometry(_dx, _dx, _size, _size)
        self.btn_open.setIcon(QtGui.QIcon('resources/menu.png'))
        self.btn_open.setStyleSheet(self.style_sheet_button_top)
        self.btn_open.installEventFilter(self)

        font = self.btn_open.font()
        font.setBold(True)

        self.btn_back = QPushButton("⮌", self._frame_top)
        self.btn_back.setGeometry(self._win_width - 3 * (_size + _dx), _dx - 3,
                                  _size, _size)
        self.btn_back.setStyleSheet(self.style_sheet_button_top)
        self.btn_back.installEventFilter(self)

        self.btn_save = QPushButton("☭", self._frame_top)
        self.btn_save.setGeometry(self._win_width - 2 * (_size + _dx), _dx,
                                  _size, _size)
        self.btn_save.setStyleSheet(self.style_sheet_button_top)
        self.btn_save.installEventFilter(self)

        self.btn_info = QPushButton("ⓘ", self._frame_top)
        self.btn_info.setGeometry(self._win_width - _size - _dx, _dx, _size,
                                  _size)
        self.btn_info.setStyleSheet(self.style_sheet_button_top)
        self.btn_info.installEventFilter(self)

        self._label_file = QLabel('', self._frame_top)
        self._label_file.setGeometry(2 * _dx + self.btn_open.width(), _dx,
                                     self._win_width - 6 * _dx - 4 * _size,
                                     _size)
        self._label_file.setStyleSheet(self.style_sheet_label_file)

    def __create_frame_left(self):
        width = 162
        _dy_top = self._frame_top.height() + 2
        _dy_bottom = _dy_bottom = self._frame_bottom.height() + 2

        self._frame_left = QFrame(self)
        self._frame_left.setGeometry(0, _dy_top, width,
                                     self._win_height - _dy_top - _dy_bottom)
        self._frame_left.setStyleSheet(
            f'background-color: {self._color_bg_text};')

        _dx = 9
        _height = 25
        _dy = 9
        for i in range(self._amount_height):
            self._labels_frame_left[i] = QLabel('', self._frame_left)
            self._labels_frame_left[i].setGeometry(
                _dx, _dy + (_height + _dy) * i, self._frame_left.width() -
                2 * _dx, _height)
            self._labels_frame_left[i].setAlignment(
                Qt.AlignRight | Qt.AlignTop)
            self._labels_frame_left[i].setStyleSheet(
                self.style_sheet_label_left)

    def __create_frame_center(self):
        width = 141
        _dx = self._frame_left.width() + 2
        _dy_top = self._frame_top.height() + 2
        _dy_bottom = self._frame_bottom.height() + 2

        for index in range(4):
            self._list_frames_center.append(QFrame(self))
            self._list_frames_center[-1].setGeometry(
                _dx + (width + 1) * index, _dy_top, width,
                self._win_height - _dy_top - _dy_bottom)
            self._list_frames_center[-1].setStyleSheet(
                f'background-color: {self._color_bg_text};')

            self._list_entries_center.append(list())
            self._list_texts_center.append(list())

            _dx_t = 9
            _size = 25
            _dy_t = 9
            for i in range(self._amount_height):
                self._list_entries_center[index].append(list())
                self._list_texts_center[index].append(list())
                for j in range(4):
                    obj = QLineEdit('', self._list_frames_center[index])

                    self._list_entries_center[index][i].append(obj)
                    self._dict_entries_center[obj] = (i, 4 * index + j)
                    self._list_texts_center[index][i].append('')

                    obj.setGeometry(_dx_t + (_size + _dx_t) * j,
                                    _dy_t + (_size + _dy_t) * i, _size, _size)
                    obj.setAlignment(Qt.AlignCenter)
                    obj.setReadOnly(True)
                    obj.setMaxLength(2)
                    obj.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
                    obj.installEventFilter(self)
                    obj.setStyleSheet(self.style_sheet_line_edit)

    def __create_frame_right(self):
        width = self._win_width - 7 - self._frame_left.width() - \
                4 * self._list_frames_center[0].width()
        _dy_top = self._frame_top.height() + 2
        _dy_bottom = self._frame_bottom.height() + 2

        self._list_frame_right = QFrame(self)
        self._list_frame_right.setGeometry(self._win_width - width, _dy_top,
                                           width, self._win_height - _dy_top -
                                           _dy_bottom)
        self._list_frame_right.setStyleSheet(
            f'background-color: {self._color_bg_text};')

        _dx_t = 3
        _width_size = 20
        _height_size = 25
        _dy_t = 9
        for i in range(self._amount_height):
            self._list_entries_right.append(list())
            self._list_texts_right.append(list())
            for j in range(self._amount_width):
                obj = QLineEdit('', self._list_frame_right)
                self._list_entries_right[i].append(obj)
                obj.setGeometry(2 + _dx_t + (_width_size + _dx_t) * j,
                                _dy_t + (_height_size + _dy_t) * i,
                                _width_size, _height_size)
                obj.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
                obj.setMaxLength(1)
                obj.setReadOnly(True)
                obj.installEventFilter(self)
                obj.setStyleSheet(self.style_sheet_line_edit)

                self._dict_entries_right[obj] = (i, j)
                self._list_texts_right[i].append('')

    def __create_frame_bottom(self):
        _height = 52

        self._frame_bottom = QFrame(self)
        self._frame_bottom.setGeometry(0, self._win_height - _height,
                                       self._win_width, _height)
        self._frame_bottom.setStyleSheet(
            f'background-color: {self._color_bg_menu};')

        _dx = 10
        _size_height = _height - 2 * _dx
        _size_width_1 = 290
        _size_width_2 = 400

        self.label_int = QLabel("Int: -", self._frame_bottom)
        self.label_int.setGeometry(_dx, _dx, _size_width_1, _size_height)
        self.label_int.setStyleSheet(self.style_sheet_label_file)

        self.label_float = QLabel("Float: -", self._frame_bottom)
        self.label_float.setGeometry(2 * _dx + self.label_int.width(), _dx,
                                     _size_width_2, _size_height)
        self.label_float.setStyleSheet(self.style_sheet_label_file)

    def __create_short_cuts(self):
        self.short_cut_open = QtWidgets.QShortcut(
            QtGui.QKeySequence(Qt.CTRL + Qt.Key_O), self)
        self.short_cut_open.activated.connect(self.__open_files_browser)

        self.short_cut_save = QtWidgets.QShortcut(
            QtGui.QKeySequence(Qt.CTRL + Qt.Key_S), self)
        self.short_cut_save.activated.connect(
            lambda: self.__save_file(self._file[1]))

        self.short_cut_undo = QtWidgets.QShortcut(
            QtGui.QKeySequence(Qt.CTRL + Qt.Key_Z), self)
        self.short_cut_undo.activated.connect(self.__make_action_back)

        self.short_cut_quit = QtWidgets.QShortcut(
            QtGui.QKeySequence(Qt.CTRL + Qt.Key_Q), self)
        self.short_cut_quit.activated.connect(self.__exit)

    def __create_finish(self):
        _width_btn = 180
        _height_btn = 30
        _dx = 3
        self._frame_btn_open = QFrame(self)
        self._frame_btn_open.setGeometry(
            self.btn_open.x() + self.btn_open.width(),
            self.btn_open.y() + self.btn_open.height(),
            _width_btn + 2 * _dx, _height_btn * 2 + 3 * _dx)
        self._frame_btn_open.setStyleSheet(
            f'background-color: {self._color_bg_menu_temp}; \n'
            f'border: 2;')

        self.btn_open_temp = QPushButton("Open the file...",
                                         self._frame_btn_open)
        self.btn_open_temp.setGeometry(_dx, _dx, _width_btn, _height_btn)
        self.btn_open_temp.setStyleSheet(self.style_sheet_button_temp)
        self.btn_open_temp.installEventFilter(self)

        self.btn_create_temp = QPushButton("Create new file",
                                           self._frame_btn_open)
        self.btn_create_temp.setGeometry(_dx, 2 * _dx + _height_btn,
                                         _width_btn, _height_btn)
        self.btn_create_temp.setStyleSheet(self.style_sheet_button_temp)
        self.btn_create_temp.installEventFilter(self)

        self._frame_btn_open.hide()

    def start(self):
        self.show()

    # ===========================================================
    # Event Handlers
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.position = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event):
        pass

    def wheelEvent(self, event):
        if self._file[1] is None:
            return

        delta = self._amount_width
        # if event.key() == Qt.Key_Control:
        #     delta *= 10

        if event.angleDelta().y() > 0:
            self._cursor -= delta
            direction = -1
            if self._cursor < 0:
                self._cursor = 0
                return
        else:
            self._cursor += delta
            direction = 1
            if self._cursor > self._cursor_max:
                self._cursor_max = self._cursor

        self.update_all(direction=direction)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self._cursor = 0
            self.update_all()
        elif event.key() == Qt.Key_PageDown:
            self._cursor = self._cursor_max
            self.update_all()

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        try:
            mime_data = event.mimeData().text()
            if 'file:///' in mime_data:
                file_name = mime_data.replace('file:///', '')
                if '\n' in file_name:
                    file_name = file_name[:file_name.index('\n')]
                if os.path.exists(file_name):
                    self._file = ('file', file_name,
                                  self.__extract_file_name(file_name))

                    self.__open_file()
            else:
                try:
                    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ' \
                                 'en-US; rv:1.9.0.7) Gecko/2009021910 ' \
                                 'Firefox/3.0.7'
                    headers = {'User-Agent': user_agent, }

                    request = urllib.request.Request(mime_data, None, headers)
                    response = urllib.request.urlopen(request)
                    content = response.read()

                    file = open('url_content.txt', mode='tw')
                    file.write(str(content[2:]))
                    file.close()

                    self._file = ('url', mime_data, mime_data)
                    self.__open_file()
                except urllib.error.URLError:
                    return

        except FileNotFoundError:
            return

    def closeEvent(self, event):
        if self._flag_changed:
            res = QMessageBox.question(
                self, 'Do you want to save and exit?',
                'Do you want to save and exit?',
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Cancel)

            if res == QMessageBox.Yes:
                if self._file[0] == 'abstract_file':
                    self.__save_file_browser()
                else:
                    self.__save_file(self._file[1])
            elif res == QMessageBox.Cancel:
                return

    def eventFilter(self, obj, event=None):
        if type(obj) == QLineEdit and event.type() == QEvent.KeyPress and \
                event.key() == Qt.Key_Z:
            modifiers = QApplication.keyboardModifiers()
            if modifiers == Qt.ControlModifier:
                self._flag_changed = True
                self.__make_action_back()
        elif type(obj) == QLineEdit and event.type() == QEvent.KeyPress and \
                event.key() == Qt.Key_Return:
            modifiers = QApplication.keyboardModifiers()
            if modifiers == Qt.ControlModifier:
                i, j = 0, 0
                try:
                    if obj in self._dict_entries_center.keys():
                        i, j = self._dict_entries_center[obj]
                    else:
                        i, j = self._dict_entries_right[obj]
                except ValueError:
                    pass

                log_line = \
                    LogLine(Command.INSERT,
                            self._cursor + i * self._amount_width + j,
                            '00', '.')
            else:
                i, j = 0, 0
                try:
                    if obj in self._dict_entries_center.keys():
                        i, j = self._dict_entries_center[obj]
                        _text = self._list_entries_center[j // 4][i][
                            j % 4].text()

                        if _text == '':
                            _char = ''
                        else:
                            value = int(_text, 16)
                            if not (32 <= value <= 127):
                                _char = '.'
                            else:
                                _char = chr(value)
                    else:
                        i, j = self._dict_entries_right[obj]
                        _char = self._list_entries_right[i][j].text()

                        if _char == '':
                            _text = ''
                        else:
                            value = ord(_char)
                            if not (32 <= value <= 127):
                                raise ValueError()
                            _text = '{:02X} '.format(value)[:2]
                except ValueError:
                    _text = '00'
                    _char = '.'

                if _text != '':
                    log_line = \
                        LogLine(Command.REFACTOR,
                                self._cursor + i * self._amount_width + j,
                                self._list_texts_center[j // 4][i][j % 4],
                                self._list_texts_right[i][j],
                                _text,
                                _char)
                else:
                    log_line = \
                        LogLine(Command.DELETE,
                                self._cursor + i * self._amount_width + j,
                                self._list_texts_center[j // 4][i][j % 4],
                                self._list_texts_right[i][j])

            self._log.append(log_line)
            self._flag_changed = True

            self.update_all()

        elif event.type() == QEvent.MouseButtonPress:
            if obj == self.btn_open:
                if event.button() == Qt.LeftButton:
                    if self._flag_frame_btn_open:
                        self._frame_btn_open.hide()
                    self.__open_files_browser()
                elif event.button() == Qt.RightButton:
                    if not self._flag_frame_btn_open:
                        self._frame_btn_open.show()
                    else:
                        self._frame_btn_open.hide()
                    self._flag_frame_btn_open = not self._flag_frame_btn_open

            elif obj == self.btn_back:
                if event.button() == Qt.LeftButton:
                    self.__make_action_back()
                elif event.button() == Qt.RightButton:
                    pass

            elif obj == self.btn_save:
                if event.button() == Qt.LeftButton:
                    if self._file[0] != 'abstract_file':
                        self.__save_file(self._file[1])
                    else:
                        self.__save_file_browser()
                elif event.button() == Qt.RightButton:
                    self.__save_file_browser()

            elif obj == self.btn_info:
                if event.button() == Qt.LeftButton:
                    url = 'https://docs.google.com/document/d/1VeNzG6mLl1ht_' \
                          'Mv-mn-SBShQZD-5-zq6CHfY3_iueN8/edit'
                    webbrowser.open(url, new=0, autoraise=True)
                elif event.button() == Qt.RightButton:
                    pass

            elif obj == self.btn_open_temp:
                if event.button() == Qt.LeftButton:
                    self._frame_btn_open.hide()
                    self.__open_files_browser()

            elif obj == self.btn_create_temp:
                if event.button() == Qt.LeftButton:
                    self._frame_btn_open.hide()
                    self.__create_file()

            elif type(obj) == QLineEdit and self._file[0] is not None and \
                    event.button() == Qt.LeftButton:

                if self._flag_frame_btn_open:
                    self._frame_btn_open.hide()
                    self._flag_frame_btn_open = not self._flag_frame_btn_open

                if obj in self._dict_entries_center.keys():
                    coordinates = self._dict_entries_center[obj]
                else:
                    coordinates = self._dict_entries_right[obj]
                y, x = coordinates

                if self._cursor + y * self._amount_width + x not in \
                        self._selected:
                    modifiers = QApplication.keyboardModifiers()
                    if modifiers != Qt.ControlModifier:
                        self._selected.clear()
                        self._selected_values.clear()

                    self._selected.append(
                        self._cursor + y * self._amount_width + x)
                    self._selected_values.append(
                        self._list_entries_center[x // 4][y][
                                    x % 4].text())
                else:  # selected
                    modifiers = QApplication.keyboardModifiers()
                    if modifiers != Qt.ControlModifier:  # not with Ctrl
                        self._selected.clear()
                        self._selected_values.clear()

                        if len(self._selected) != 0:
                            self._selected.append(
                                self._cursor + y * self._amount_width + x)
                            self._selected_values.append(
                                self._list_entries_center[x // 4][y][
                                    x % 4].text())
                    else:  # with Ctrl
                        if obj in self._dict_entries_center.keys():
                            coordinates = self._dict_entries_center[obj]
                        else:
                            coordinates = self._dict_entries_right[obj]

                        y, x = coordinates
                        ind = self._selected.index(
                            self._cursor + y * self._amount_width + x)
                        self._selected.pop(ind)
                        self._selected_values.pop(ind)

                self._selected.sort()
                self.update_all()

            else:
                if event.button() == Qt.LeftButton and \
                        self._flag_frame_btn_open:
                    self._frame_btn_open.hide()
                    self._flag_frame_btn_open = False

        return super().eventFilter(obj, event)

    def __open_files_browser(self):
        try:
            file_name = QtWidgets.QFileDialog.getOpenFileName(
                None, 'Open file')[0]
            if file_name == '':
                return

            if self._flag_changed:
                res = QMessageBox.question(
                    self, 'Do you want to save', 'Do you want to save?',
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                    QMessageBox.Cancel)

                if res == QMessageBox.Yes:
                    self.__save_file(self._file[1])
                elif res == QMessageBox.Cancel:
                    return

            self._file = ('file', file_name,
                          self.__extract_file_name(file_name))
            self.__open_file()
        except TypeError:
            return

    def __open_file(self):
        for i in range(self._amount_height):
            for j in range(self._amount_width):
                self._list_entries_center[j // 4][i][j % 4]\
                    .setReadOnly(not self._mode_edit)
                self._list_entries_right[i][j]\
                    .setReadOnly(not self._mode_edit)

        self._cursor = 0
        self._cursor_max = 0
        self._selected.clear()
        self._selected_values.clear()

        self._file_changing_handler = FileChangingHandler(self, self._file[1])
        self._observer = Observer()
        self._observer.schedule(
            self._file_changing_handler,
            path=f'{self._file[1][:self._file[1].rindex("/")]}',
            recursive=False)
        self._observer.start()

        self.update_all()

    def __create_file(self):
        try:
            self._file = ('abstract_file', 'Untitled file', 'Untitled file')
            self.__open_file()
        except TypeError:
            return

    def __make_action_back(self):
        if len(self._log) > 0:
            self._log.pop_last()
            self.update_all()
        elif len(self._log_temp) > 0:
            self._log.append(self._log_temp.pop_last(), change=False)
            self.update_all()

    def __save_file_browser(self):
        try:
            if self._file[1] is None:
                return

            file_name = QtWidgets.QFileDialog.getSaveFileName(
                None, 'Save file', 'c:\\')[0]
            if file_name == '':
                return

            self.__save_file(file_name)
        except TypeError:
            return

    def __save_file(self, file_name):
        if self._file[0] is None:
            return

        if self._file[0] == 'file':
            result = self._board.get_content_from_file(self._file[1],
                                                       self._log, 0, -1)
            with open(file_name, mode='wb') as file_write:
                file_write.write(result)

            self._log_temp = self._log.inverse()
            self._log.clear()
            self._flag_changed = False
        elif self._file[0] == 'abstract_file':
            _len = 0
            for log_line in self._log:
                if log_line.index > _len:
                    _len = log_line.index
            result = self._board.get_content(self._log, 0, _len + 2)

            with open(file_name, mode='wb') as file_write:
                file_write.write(result)

            self._text_abstract = b''
            self._file = ('file', file_name,
                          self.__extract_file_name(file_name))
            self._flag_changed = False
        else:
            QMessageBox.critical(self, 'Exception',
                                 'File of url can\'t be saved!',
                                 QMessageBox.Ok)
            return

        self.update_all()

    # ===========================================================
    # Other
    def update_all(self, direction=0):
        self._label_file.setText(self._file[2])

        if direction == 0:
            for i in range(self._amount_height):
                for j in range(self._amount_width):
                    self._list_entries_center[j // 4][i][j % 4]\
                        .setStyleSheet(
                            self.style_sheet_line_edit)
                    self._list_entries_right[i][j].setStyleSheet(
                        self.style_sheet_line_edit)
        else:
            for cursor in self._selected:
                i = (cursor - self._cursor) // self._amount_width
                j = (cursor - self._cursor) % self._amount_width

                if 0 <= i + direction < self._amount_height:
                    self._list_entries_center[j // 4][i + direction][j % 4] \
                        .setStyleSheet(
                            self.style_sheet_line_edit)
                    self._list_entries_right[i + direction][j].setStyleSheet(
                        self.style_sheet_line_edit)

        for cursor in self._selected:
            if self._cursor <= cursor < self._cursor + \
                    self._amount_width * self._amount_height:
                i = (cursor - self._cursor) // self._amount_width
                j = (cursor - self._cursor) % self._amount_width

                self._list_entries_center[j // 4][i][j % 4].setStyleSheet(
                    self.style_sheet_line_edit_selected)
                self._list_entries_right[i][j].setStyleSheet(
                    self.style_sheet_line_edit_selected)

        if self._file[0] == 'file':
            self._board.update(self._file[1], self._encoding,
                               self._cursor, self._log)
        elif self._file[0] == 'abstract_file':
            _len = self._board.update(
                self._text_abstract, self._encoding, self._cursor, self._log,
                not_file=True)
            self._text_abstract = b'\x00' * _len
        elif self._file[0] == 'url':
            self._board.update('url_content.txt', self._encoding,
                               self._cursor, self._log)

        indexes = self._board.indexes
        _bytes = self._board.bytes
        chars = self._board.chars

        for i in range(self._amount_height):
            self._labels_frame_left[i].setText(indexes[i])

            for k in range(4):
                for j in range(self._amount_width // 4):
                    self._list_entries_center[k][i][j] \
                        .setText(_bytes[i][4 * k + j])
                    self._list_texts_center[k][i][j] = _bytes[i][4 * k + j]

            for j in range(self._amount_width):
                self._list_entries_right[i][j] \
                    .setText(chars[i][j])
                self._list_texts_right[i][j] = chars[i][j]

        text = "b'" + '\\x00' * (4 - len(self._selected_values))
        for value in self._selected_values:
            text += f'\\x{value}'
        text += "'"

        value_int = int.from_bytes(ast.literal_eval(text),
                                   byteorder='big', signed=True)
        if not (-2 ** 63 <= value_int < 2 ** 63):
            value_int = '-'
        self.label_int.setText(f'Int64: {value_int}')

        if len(self._selected_values) <= 4:
            text = "b'" + '\\x00' * (4 - len(self._selected_values))
            for value in self._selected_values:
                text += f'\\x{value}'
            text += "'"

            _bytes = ast.literal_eval(text)
            value_float = struct.unpack('f', _bytes)[0]
            self.label_float.setText(
                f'Float: {value_float}')
        else:
            self.label_float.setText(
                f'Float: -')

    def __exit(self):
        if self._flag_changed:
            res = QMessageBox.question(
                self, 'Do you want to save and exit?',
                'Do you want to save and exit?',
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Cancel)

            if res == QMessageBox.Yes:
                if self._file[0] == 'Abstract_file':
                    self.__save_file_browser()
                else:
                    self.__save_file(self._file[1])
            elif res == QMessageBox.Cancel:
                return

        qApp.quit()

    def __extract_file_name(self, file_name):
        path_parsed = file_name.split('/')
        path = [path_parsed.pop(0), path_parsed.pop(-1)]
        left, right = 1, 1

        while len(path_parsed) != 0 and sum([len(i) for i in path]) + \
                len(path) + 2 <= self._label_file_max_len:
            if left >= right:
                if sum([len(i) for i in path]) + len(path_parsed[-1]) + \
                        len(path) + 3 <= self._label_file_max_len:
                    path.insert(-right, path_parsed.pop(-1))
                    right += 1
                elif sum([len(i) for i in path]) + len(path_parsed[0]) + \
                        len(path) + 3 <= self._label_file_max_len:
                    path.insert(left, path_parsed.pop(0))
                    left += 1
                else:
                    if sum([len(i) for i in path]) + \
                            len(path) + 3 <= self._label_file_max_len:
                        path.insert(left, '...')
                    else:
                        path[left] = '...'
                    break

            elif left < right:
                if sum([len(i) for i in path]) + len(path_parsed[0]) + \
                        len(path) + 3 <= self._label_file_max_len:
                    path.insert(left, path_parsed.pop(0))
                    left += 1
                elif sum([len(i) for i in path]) + len(path_parsed[-1]) + \
                        len(path) + 3 <= self._label_file_max_len:
                    path.insert(-right, path_parsed.pop(-1))
                    right += 1
                else:
                    if sum([len(i) for i in path]) + \
                            len(path) + 3 <= self._label_file_max_len:
                        path.insert(left, '...')
                    else:
                        path[left] = '...'
                    break

        return '\\'.join(str(j) for j in path)
