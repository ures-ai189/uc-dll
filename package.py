#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2018 The ungoogled-chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
ungoogled-chromium packaging script for Microsoft Windows
"""

import sys
if sys.version_info.major < 3:
    raise RuntimeError('Python 3 is required for this script.')

import argparse
import os
import platform
from pathlib import Path
import shutil

sys.path.insert(0, str(Path(__file__).resolve().parent / 'ungoogled-chromium' / 'utils'))
import filescfg
from _common import ENCODING, get_chromium_version
sys.path.pop(0)

def _get_release_revision():
    revision_path = Path(__file__).resolve().parent / 'ungoogled-chromium' / 'revision.txt'
    return revision_path.read_text(encoding=ENCODING).strip()

def _get_packaging_revision():
    revision_path = Path(__file__).resolve().parent / 'revision.txt'
    return revision_path.read_text(encoding=ENCODING).strip()

_cached_target_cpu = None

def _get_target_cpu(build_outputs):
    global _cached_target_cpu
    if not _cached_target_cpu:
        with open(build_outputs / 'args.gn', 'r') as f:
            args_gn_text = f.read()
            for cpu in ('x64', 'x86', 'arm64'):
                if f'target_cpu="{cpu}"' in args_gn_text:
                    _cached_target_cpu = cpu
                    break
    assert _cached_target_cpu
    return _cached_target_cpu

def main():
    """Entrypoint"""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--cpu-arch',
        metavar='ARCH',
        default=platform.architecture()[0],
        choices=('64bit', '32bit', 'arm'),
        help=('Filter build outputs by a target CPU. '
              'This is the same as the "arch" key in FILES.cfg. '
              'Default (from platform.architecture()): %(default)s'))
    args = parser.parse_args()

    build_outputs = Path('build/src/out/Default')

    # 不再复制 mini_installer.exe，只打包 ZIP

    timestamp = None
    try:
        with open('build/src/build/util/LASTCHANGE.committime', 'r') as ct:
            timestamp = int(ct.read())
    except FileNotFoundError:
        pass

    output = Path('build/ungoogled-chromium_{}-{}.{}_windows_{}.zip'.format(
        get_chromium_version(), _get_release_revision(),
        _get_packaging_revision(), _get_target_cpu(build_outputs)))

    # 仅打包 chrome.dll 和 chrome.dll.pdb
    import zipfile
    files_to_zip = [
        build_outputs / 'chrome.dll',
        build_outputs / 'chrome.dll.pdb',
    ]

    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in files_to_zip:
            if file_path.exists():
                # 将文件存入 ZIP 根目录，使用文件名作为归档名
                zf.write(file_path, arcname=file_path.name)
            else:
                print(f"Warning: {file_path} not found, skipping")

if __name__ == '__main__':
    main()
