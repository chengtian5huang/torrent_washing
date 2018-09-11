# -*- coding: utf-8 -*-
"""
Created on 2018/9/10

Creator: cts
"""

import logging
import os
import re
import time

from torrent_washing_experimental import sabotage, publisher_rgx, comment_rgx, creat_rgx, load_tort, dump_tort, \
    reverse_matched


def compress_text(text, *, length=20):
    _l = len(text)
    if _l < length:
        return text
    else:
        length -= 3
        head, tail = int(length / 2), -1 * (length - int(length / 2))
        return '...'.join((text[:head], text[tail:]))


class TorrentWasher:
    def __init__(self, surveillance_dir, *, verbose=False):
        self._rgxs = self._find_rgx()
        self._is_verbose = verbose
        self._logger = self._log_conf()
        self._surveillance_dir = surveillance_dir

        if not self._rgxs:
            raise LookupError('cant find any rgx for replacement')
        self._logger.info('find rgx group > \n{}'.format(self._rgxs))

        self._s = compress_text

    @staticmethod
    def _find_rgx():
        return [globals()[name] for name in globals() if name.endswith('_rgx') and name != '_find_rgx']

    def _log_conf(self):
        core_log = logging.getLogger(self.__class__.__name__)
        core_log.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(asctime)s||%(name)s > %(levelname)s @LineNo.%(lineno)s|| %(message)s',
                                              datefmt='%H:%M:%S')

        console_log = logging.StreamHandler()
        console_log.setLevel(logging.DEBUG if self._is_verbose else logging.INFO)
        console_log.setFormatter(console_formatter)
        core_log.addHandler(console_log)
        return core_log

    def _unwashed_torts(self):
        return [file for file in os.listdir(self._surveillance_dir) if
                file.endswith('torrent') and not file.startswith('#')]

    def _all_torts(self):
        return [file for file in os.listdir(self._surveillance_dir) if
                file.endswith('torrent')]

    def _is_washed(self, file_name):
        self._logger.debug("check if it's washed > {}".format(file_name))
        self._logger.debug('torrents in dir > {}'.format(self._all_torts()))

        washed_file_name = ' '.join(('#', file_name))
        washed_full_path = os.path.join(self._surveillance_dir, washed_file_name)
        return self._really_exist(washed_full_path)

    def _sabotage(self, torrent_name):
        full_path = os.path.join(self._surveillance_dir, torrent_name)
        sabotaged_content = load_tort(full_path)
        repl_count = 0

        for rgx in self._rgxs:
            sabotaged_content, repl_count = re.subn(rgx, reverse_matched, sabotaged_content)

        self._logger.debug(
            '{replaced_count} items in {tort_name}'.format(replaced_count=repl_count, tort_name=torrent_name))
        written_len = dump_tort(full_path, sabotaged_content)
        return written_len, repl_count

    @staticmethod
    def _really_exist(full_path):
        return os.path.exists(full_path) and os.path.isfile(full_path)

    def _engage(self):
        for torrent in self._unwashed_torts():
            if not self._is_washed(torrent):
                self._logger.info('Unwashed > {unwashed}'.format(unwashed=torrent))

                full_path = os.path.join(self._surveillance_dir, torrent)
                if self._really_exist(full_path):
                    self._logger.debug('Override existed washed torrent.')
                _, repl_count = self._sabotage(full_path)

                if self._really_exist(full_path):
                    self._logger.info(
                        'successfully generate > {0} replaced {1} items.'.format(torrent, repl_count))
                else:
                    self._logger.info('failed to generate > {}'.format(full_path))

    @staticmethod
    def _idle():
        time.sleep(2)

    def run(self):
        dir_torrents = None
        while True:
            if self._unwashed_torts() != dir_torrents:
                self._engage()
                dir_torrents = self._unwashed_torts()
            else:
                self._idle()


if __name__ == '__main__':
    _ = TorrentWasher(r'D:\torrent_cleaning', verbose=False)
    _.run()
