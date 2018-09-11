# -*- coding: utf-8 -*-
"""
Created on 2018/9/10

Creator: cts
"""
import re

from torrent_washing_experimental import _load_torrent, sabotage, publisher_rgx, _find_rgx


def test_reading_torrents():
    p = r'../example_torrents/MDB687AVI.torrent'
    _ = _load_torrent(p)
    assert _


def test_sabotage():
    p = r'../example_torrents/MDB687AVI.torrent'
    _ = sabotage(p)
    assert _


def test_auto_load_rgx():
    print(_find_rgx())
