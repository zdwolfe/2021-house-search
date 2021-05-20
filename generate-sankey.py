#!/usr/bin/env python3

import argparse
import sys
import browser_history
import graphs

def add_options(parser):
    parser.add_argument("--chrome-sqlite-browser-history-path",
                        dest="chrome_sqlite_history_path",
                        type=str,
                        help="The file path to the chrome browser history sqlite3.")


def get_options():
    parser = argparse.ArgumentParser(usage="%(prog) --chrome-sqlite-browser-history-path '<FOO>'")
    add_options(parser)

    options, args = parser.parse_known_args(sys.argv)
    return options


def generate(chrome_sqlite_history_path):
    browser_listing_history = browser_history.get_listing_history(chrome_sqlite_history_path)
    graphs.generate_graph(browser_listing_history)


if __name__ == '__main__':
    options = get_options()
    chrome_sqlite_history_path = options.chrome_sqlite_history_path
    generate(chrome_sqlite_history_path)




