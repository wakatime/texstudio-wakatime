# -*- coding: utf-8 -*-
"""
    WakaTime TeXstudio Macro Installer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Downloads and installs the WakaTime TeXstudio macro.
    :copyright: (c) 2016 Alan Hamlett.
    :license: BSD, see LICENSE for more details.
"""


import os
import json
import platform
import sys
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


PY2 = (sys.version_info[0] == 2)
ROOT_URL = 'https://raw.githubusercontent.com/wakatime/texstudio-wakatime/master/src/'
SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
if platform.system() == 'Windows':
    CONFIG_DIR = os.path.join(os.getenv('APPDATA'), 'texstudio', 'macro')
else:
    CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.config', 'texstudio', 'macro')
FILES = [
    'utils.js',
    'main.js',
]


if PY2:
    import codecs
    open = codecs.open
    input = raw_input


def main():
    macro = build_macro()
    path = find_macro_file()
    save_macro_file(macro, path)
    print('Installed. You may now run TeXstudio.')
    if platform.system() == 'Windows':
        input('Press [Enter] to exit...')


def build_macro():
    """Build the WakaTime macro object from source JavaScript files."""

    script = {
        "abbrev": '',
        "description": 'TeXstudio macro for automatic time tracking and metrics generated from your TeXstudio usage.',
        "formatVersion": 1,
        "menu": '',
        "name": 'WakaTime',
        "shortcut": '',
        "trigger": '?txs-start|?save-file'
    }

    script['tag'] = []
    script['tag'].append('%SCRIPT')
    for filename in FILES:
        contents = get_file_contents(filename)
        if not contents:
            continue
        for line in contents.splitlines():
            script['tag'].append(line.rstrip())
    return script


def get_file_contents(filename):
    """Get file contents from local clone or GitHub repo."""

    if os.path.exists(os.path.join(SRC_DIR, filename)):
        with open(os.path.join(SRC_DIR, filename)) as fh:
            return fh.read()
    else:
        url = ROOT_URL + filename
        resp = urlopen(url)
        return resp.read() if PY2 else resp.read().decode('utf-8')


def find_macro_file():
    """Returns path of existing installed macro or an unused macro number file."""

    number = 0
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    while True:
        filename = 'Macro_{}.txsMacro'.format(number)
        macroFile = os.path.join(CONFIG_DIR, filename)
        if not os.path.exists(macroFile):
            print('Installing WakaTime macro {}.'.format(macroFile))
            return macroFile
        with open(macroFile, 'r', encoding='utf-8') as fh:
            macro = json.load(fh)
        if macro.get('name') == 'WakaTime':
            print('Found existing WakaTime macro {}.'.format(macroFile))
            return macroFile
        number += 1


def save_macro_file(macro, path):
    """Writes macro contents to txsMacro path."""

    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(macro, fh, sort_keys=True, indent=2)


if __name__ == '__main__':
    main()
