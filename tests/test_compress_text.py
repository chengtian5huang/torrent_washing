# -*- coding: utf-8 -*-
"""
Created on 2018/9/11

Creator: cts
"""
from torrent_washer import compress_text


def test_short_text():
    _ = '第一會所新片@SIS001@(sister)(SIS-079)風俗店開店！？自宅で姉がまさかの開業！お客は毎日弟の俺！佐々木あき.torrent'
    assert 20 == len(compress_text(_))
