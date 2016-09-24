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
    CONFIG_DIR = os.path.join(os.getenv('APPDATA'), 'texstudio')
else:
    CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.config', 'texstudio')
FILES = [
    'utils.js',
    'main.js',
]


if PY2:
    import codecs
    open = codecs.open
    input = raw_input


def main():
    configs = parse_ini_file()
    macro = build_macro()
    configs = add_macro(configs, macro)
    save_ini_file(configs)
    print('Installed. You may now run TeXstudio.')
    if platform.system() == 'Windows':
        input('Press [Enter] to exit...')


def build_macro():
    """Build the contents that gets added to your texstudio.ini file."""

    script = '%SCRIPT'
    for filename in FILES:
        contents = get_file_contents(filename)
        if not contents:
            return
        script += '\n' + contents
    script = json.dumps(script)
    macro = 'WakaTime, {script}, , ?txs-start|?save-file'.format(
        script=script,
    )
    return macro


def get_file_contents(filename):
    """Get file contents from local clone or GitHub repo."""

    if os.path.exists(os.path.join(SRC_DIR, filename)):
        with open(os.path.join(SRC_DIR, filename)) as fh:
            return fh.read()
    else:
        url = ROOT_URL + filename
        resp = urlopen(url)
        return resp.read()


def parse_ini_file():
    """Parses your texstudio.ini config file and returns a ConfigParser obj."""

    iniFile = os.path.join(CONFIG_DIR, 'texstudio.ini')

    configs = configparser.RawConfigParser()
    configs.optionxform = str  # preserve case in key names
    with open(iniFile, 'r', encoding='utf-8') as fh:
        configs.readfp(fh)
    return configs


def add_macro(configs, macro):
    """Adds the given macro to a ConfigParser texstudio.ini file."""

    section = 'texmaker'
    key = 'Macros\\{0}'

    # find next available macro index
    index = 0
    while configs.has_option(section, key.format(index)):
        val = configs.get(section, key.format(index))
        if val.split(',')[0].strip() == 'WakaTime':
            break
        index += 1

    # add macro to config at given index
    configs.set(section, key.format(index), macro)

    return configs


def save_ini_file(configs):
    """Writes a ConfigParser obj to your texstudio.ini config file."""

    iniFile = os.path.join(CONFIG_DIR, 'texstudio.ini')

    with open(iniFile, 'w', encoding='utf-8') as fh:
        configs.write(fh)


if __name__ == '__main__':
    main()
