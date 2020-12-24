#!/usr/bin/env python3

import sys
import argparse
from PyQt5.QtWidgets import QApplication

from fronend.window import Window
from fronend.console import Console


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--edit', action='store_true',
                        help='toggles `edit` mode')
    parser.add_argument('-v', '--view', action='store_true',
                        help='toggles `view` mode')
    parser.add_argument('-c', '--console', action='store_true',
                        help='starts app in current console/terminal with '
                             '`view` mode')
    args = parser.parse_args()

    if args.console:
        if args.edit:
            print('[WARNING] Program can\'t be started in console with mode '
                  '`edit`!')

        console = Console()
        console.start()
    else:
        if args.edit and args.view:
            print('[WARNING] Program can\'t be started in both modes! It will '
                  'be started in `edit` mode!')
        app = QApplication(sys.argv)
        window = Window(
            mode_edit=args.edit or (not args.edit and not args.view))
        window.start()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
