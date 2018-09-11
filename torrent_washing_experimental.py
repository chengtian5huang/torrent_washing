# -*- coding: utf-8 -*-
"""
Created on 2018/9/10

Creator: cts
"""
import os
import re

publisher_rgx = re.compile(b'publisher')
comment_rgx = re.compile(b'comment')
creat_rgx = re.compile(b'creat')


def _load_torrent(path):
    with open(path, 'rb') as torrent_hnd:
        torrent_content = torrent_hnd.read()
    return torrent_content


def _dump_torrent(path, content):
    head, file_name = os.path.split(path)
    new_path = os.path.join(head, ' '.join(('#', file_name)))
    with open(new_path, 'wb') as torrent_hnd:
        written_length = torrent_hnd.write(content)
    return written_length


def _reversed_b(match_obj):
    return match_obj.group(0)[::-1]


def sabotage(path):
    sabotaged_content = _load_torrent(path)
    for rgx in _find_rgx():
        sabotaged_content = re.sub(rgx, _reversed_b, sabotaged_content)

    written_len = _dump_torrent(path, sabotaged_content)
    return written_len


def _find_rgx():
    return [globals()[name] for name in globals() if name.endswith('_rgx') and name != '_find_rgx']


find_rgx = _find_rgx
dump_tort = _dump_torrent
load_tort = _load_torrent
reverse_matched = _reversed_b
