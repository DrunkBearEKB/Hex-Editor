import unittest

from backend.board import Board
from backend.log.log import Log
from backend.log.log_line import LogLine
from backend.log.commands import Command


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.width = 16
        self.height = 4
        self.board = Board(self.width, self.height)
        self.log = Log()

    def test_board_empty_file_indexes_1(self):
        self.board.update('tests/temp_1.txt', 'ascii', 0)
        correct_answer = ['00000000000000', '00000000000001',
                          '00000000000002', '00000000000003']
        self.assertEqual(correct_answer,
                         self.board.indexes)

    def test_board_not_empty_file_indexes_2(self):
        self.board.update('tests/temp_2.txt', 'ascii', 0)
        correct_answer = ['00000000000000', '00000000000001',
                          '00000000000002', '00000000000003']
        self.assertEqual(correct_answer,
                         self.board.indexes)

    def test_board_not_empty_file_indexes_3(self):
        self.board.update('tests/temp_2.txt', 'ascii', self.width)
        correct_answer = ['00000000000001', '00000000000002',
                          '00000000000003', '00000000000004']
        self.assertEqual(correct_answer,
                         self.board.indexes)

    def test_board_not_empty_file_indexes_4(self):
        self.board.update('tests/temp_2.txt', 'ascii', 2 * self.width)
        correct_answer = ['00000000000002', '00000000000003',
                          '00000000000004', '00000000000005']
        self.assertEqual(correct_answer,
                         self.board.indexes)

    def test_board_empty_file_bytes_1(self):
        self.board.update('tests/temp_1.txt', 'ascii', 0)
        correct_answer = [['00' for _ in range(self.width)]
                          for __ in range(self.height)]
        self.assertEqual(correct_answer,
                         self.board.bytes)

    def test_board_not_empty_file_bytes_2(self):
        self.board.update('tests/temp_2.txt', 'ascii', 0)
        correct_answer = [
            ['62', '6A', '64', '66', '62', '73', '68', '6A', '64', '61', '64',
             '66', '6A', '68', '20', '62'],
            ['64', '76', '73', '6C', '3B', '6A', '67', '66', '6B', '6C', '62',
             '66', '67', '6C', '73', '64'],
            ['6B', '66', '6A', '68', '6B', '20', '6A', '64', '73', '6B', '61',
             '66', '6B', '6A', '68', '6C'],
            ['64', '66', '6B', '6C', '2F', '73', '76', '5B', '64', '67', '70',
             '68', '6F', '69', '66', '77']]
        self.assertEqual(correct_answer,
                         self.board.bytes)

    def test_board_not_empty_file_bytes_3(self):
        self.board.update('tests/temp_2.txt', 'ascii', self.width)
        correct_answer = [
            ['64', '76', '73', '6C', '3B', '6A', '67', '66', '6B', '6C', '62',
             '66', '67', '6C', '73', '64'],
            ['6B', '66', '6A', '68', '6B', '20', '6A', '64', '73', '6B', '61',
             '66', '6B', '6A', '68', '6C'],
            ['64', '66', '6B', '6C', '2F', '73', '76', '5B', '64', '67', '70',
             '68', '6F', '69', '66', '77'],
            ['75', '32', '33', '35', '38', '34', '39', '36', '6F', '6A', '68',
             '74', '72', '2E', '2E', '62']]
        self.assertEqual(correct_answer,
                         self.board.bytes)

    def test_board_not_empty_file_bytes_4(self):
        self.board.update('tests/temp_2.txt', 'ascii', 2 * self.width)
        correct_answer = [
            ['6B', '66', '6A', '68', '6B', '20', '6A', '64', '73', '6B', '61',
             '66', '6B', '6A', '68', '6C'],
            ['64', '66', '6B', '6C', '2F', '73', '76', '5B', '64', '67', '70',
             '68', '6F', '69', '66', '77'],
            ['75', '32', '33', '35', '38', '34', '39', '36', '6F', '6A', '68',
             '74', '72', '2E', '2E', '62'],
            ['76', '64', '6A', '63', '71', '66', '77', '74', '33', '20', '79',
             '32', '35', '34', '70', '75']]
        self.assertEqual(correct_answer,
                         self.board.bytes)

    def test_board_empty_file_chars_1(self):
        self.board.update('tests/temp_1.txt', 'ascii', 0)
        correct_answer = [['.' for _ in range(self.width)]
                          for __ in range(self.height)]
        self.assertEqual(correct_answer,
                         self.board.chars)

    def test_board_not_empty_file_chars_2(self):
        self.board.update('tests/temp_2.txt', 'ascii', 0)
        correct_answer = [
            ['b', 'j', 'd', 'f', 'b', 's', 'h', 'j', 'd', 'a', 'd', 'f', 'j',
             'h', ' ', 'b'],
            ['d', 'v', 's', 'l', ';', 'j', 'g', 'f', 'k', 'l', 'b', 'f', 'g',
             'l', 's', 'd'],
            ['k', 'f', 'j', 'h', 'k', ' ', 'j', 'd', 's', 'k', 'a', 'f', 'k',
             'j', 'h', 'l'],
            ['d', 'f', 'k', 'l', '/', 's', 'v', '[', 'd', 'g', 'p', 'h', 'o',
             'i', 'f', 'w']]
        self.assertEqual(correct_answer,
                         self.board.chars)

    def test_board_not_empty_file_chars_3(self):
        self.board.update('tests/temp_2.txt', 'ascii', self.width)
        correct_answer = [
            ['d', 'v', 's', 'l', ';', 'j', 'g', 'f', 'k', 'l', 'b', 'f', 'g',
             'l', 's', 'd'],
            ['k', 'f', 'j', 'h', 'k', ' ', 'j', 'd', 's', 'k', 'a', 'f', 'k',
             'j', 'h', 'l'],
            ['d', 'f', 'k', 'l', '/', 's', 'v', '[', 'd', 'g', 'p', 'h', 'o',
             'i', 'f', 'w'],
            ['u', '2', '3', '5', '8', '4', '9', '6', 'o', 'j', 'h', 't', 'r',
             '.', '.', 'b']]
        self.assertEqual(correct_answer,
                         self.board.chars)

    def test_board_not_empty_file_chars_4(self):
        self.board.update('tests/temp_2.txt', 'ascii', 2 * self.width)
        correct_answer = [
            ['k', 'f', 'j', 'h', 'k', ' ', 'j', 'd', 's', 'k', 'a', 'f', 'k',
             'j', 'h', 'l'],
            ['d', 'f', 'k', 'l', '/', 's', 'v', '[', 'd', 'g', 'p', 'h', 'o',
             'i', 'f', 'w'],
            ['u', '2', '3', '5', '8', '4', '9', '6', 'o', 'j', 'h', 't', 'r',
             '.', '.', 'b'],
            ['v', 'd', 'j', 'c', 'q', 'f', 'w', 't', '3', ' ', 'y', '2', '5',
             '4', 'p', 'u']]
        self.assertEqual(correct_answer,
                         self.board.chars)

    def test_log_append_1(self):
        log_line = LogLine(Command.INSERT, 0)
        self.log.append(log_line)
        self.assertTrue(log_line in self.log.list)

    def test_log_append_2(self):
        log_line = LogLine(Command.REFACTOR, 0)
        self.log.append(log_line)
        self.assertTrue(log_line in self.log.list)

    def test_log_append_3(self):
        log_line = LogLine(Command.DELETE, 0)
        self.log.append(log_line)
        self.assertTrue(log_line in self.log.list)

    def test_log_append_4(self):
        log_line1 = LogLine(Command.INSERT, 5)
        log_line2 = LogLine(Command.REFACTOR, 15)
        self.log.append(log_line1)
        self.log.append(log_line2)

        self.assertTrue(self.log.pop_first() == log_line1)

    def test_log_append_5(self):
        log_line1 = LogLine(Command.INSERT, 5)
        log_line2 = LogLine(Command.REFACTOR, 15)
        self.log.append(log_line1)
        self.log.append(log_line2)

        self.assertTrue(self.log.pop_last() == log_line2)

    def test_log_append_6(self):
        log_line1 = LogLine(Command.INSERT, 5)
        log_line2 = LogLine(Command.REFACTOR, 15)
        self.log.append(log_line1)
        self.log.append(log_line2)

        self.assertEqual(2, len(self.log))

    def test_log_line_1(self):
        self.assertRaises(ValueError, self.log.append)

    def test_log_line_2(self):
        try:
            LogLine(1, 0)
        except ValueError:
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)

    def test_log_line_3(self):
        try:
            LogLine(Command.REFACTOR, 'asdf')
        except ValueError:
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
