#!/usr/bin/env python3

import argparse
import sys
import browser_history
from graphs import Graph


def add_options(parser):
    parser.add_argument("--chrome-sqlite-browser-history-path",
                        dest="chrome_sqlite_history_path",
                        type=str,
                        help="The file path to the chrome browser history sqlite3.")
    parser.add_argument("--html-file-path",
                        dest="html_filepath",
                        type=str,
                        help="The file path to output the graph to as html.")


def get_options():
    parser = argparse.ArgumentParser(usage="%(prog) --chrome-sqlite-browser-history-path '<FOO>'")
    add_options(parser)

    options, args = parser.parse_known_args(sys.argv)
    return options


def generate(options):
    chrome_sqlite_history_path = options.chrome_sqlite_history_path
    html_filepath = options.html_filepath

    browser_listing_history = browser_history.get_listing_history(chrome_sqlite_history_path)
    graph = Graph.fromBrowserHistory(browser_listing_history)
    graph.show_fig()
    graph.write_fig_to_html_filepath(html_filepath)

if __name__ == '__main__':
    options = get_options()
    generate(options)




