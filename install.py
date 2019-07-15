# -*- coding: utf-8 -*-
"""
    WakaTime TeXstudio Macro Installer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Downloads and installs the WakaTime TeXstudio macro.
    :copyright: (c) 2016 Alan Hamlett.
    :license: BSD, see LICENSE for more details.
"""


import os
import glob
import json
import platform
import sys
try:
    import ConfigParser as configparser
except ImportError:
    import configparser
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
    save_macro_file(macro)
    print('Installed. You may now run TeXstudio.')
    if platform.system() == 'Windows':
        input('Press [Enter] to exit...')


def build_macro():
    """Build the contents that adds wakatime.txsMacro file."""

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
        path = get_file_path(filename)
        with open(path) as f:
            line = f.readline()
            while line:
                line = line.replace('\n', '').strip()
                script['tag'].append(line)
                line = f.readline()
    return script


def get_file_path(filename):
    """Get file contents from local clone or GitHub repo."""

    if os.path.exists(os.path.join(SRC_DIR, filename)):
        return os.path.join(SRC_DIR, filename)
    else:
        return ROOT_URL + filename


def save_macro_file(macro):
    """Writes wakatime.txsMacro file."""

    os.chdir(CONFIG_DIR)
    total_files = len(glob.glob1(CONFIG_DIR, 'Macro_*.txsMacro'))
    print('Found {} file(s) from macro folder.'.format(total_files))

    macroFile = os.path.join(CONFIG_DIR, 'Macro_{}.txsMacro'.format(total_files))

    with open(macroFile, 'w', encoding='utf-8') as fh:
        json.dump(macro, fh)


if __name__ == '__main__':
    main()
