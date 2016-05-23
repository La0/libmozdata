# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import unittest
from clouseau.HGFileInfo import HGFileInfo
from clouseau import utils


class HGFileInfoTest(unittest.TestCase):

    def test_hgfileinfo(self):
        path = 'netwerk/protocol/http/nsHttpConnectionMgr.cpp'
        hi = HGFileInfo(path)
        fi = hi.get(path)

        self.assertIn('authors', fi)
        self.assertIsNotNone(fi['authors'])
        self.assertIn('bugs', fi)
        self.assertIsNotNone(fi['bugs'])

    def test_hgfileinfo_date(self):
        path = 'LICENSE'
        hi = HGFileInfo(path)

        fi = hi.get(path)
        self.assertEqual(len(fi['authors']), 2)
        self.assertEqual(fi['authors']['Phil Ringnalda <philringnalda@gmail.com>']['count'], 1)
        self.assertEqual(len(fi['authors']['Phil Ringnalda <philringnalda@gmail.com>']['reviewers']), 1)
        self.assertEqual(fi['authors']['Phil Ringnalda <philringnalda@gmail.com>']['reviewers']['gerv'], 1)
        self.assertEqual(fi['authors']['hg@mozilla.com']['count'], 1)
        self.assertEqual(fi['authors']['hg@mozilla.com']['reviewers'], {})
        self.assertEqual(fi['bugs'], set(['547914']))
        self.assertEqual(len(fi['patches']), 2)
        self.assertEqual(fi['patches'][0]['author'], 'Phil Ringnalda <philringnalda@gmail.com>')
        self.assertEqual(fi['patches'][1]['author'], 'hg@mozilla.com')

        fi = hi.get(path, utils.get_timestamp('2009-01-01'))
        self.assertEqual(len(fi['authors']), 1)
        self.assertEqual(fi['authors']['Phil Ringnalda <philringnalda@gmail.com>']['count'], 1)
        self.assertEqual(len(fi['authors']['Phil Ringnalda <philringnalda@gmail.com>']['reviewers']), 1)
        self.assertEqual(fi['authors']['Phil Ringnalda <philringnalda@gmail.com>']['reviewers']['gerv'], 1)
        self.assertEqual(fi['bugs'], set(['547914']))
        self.assertEqual(len(fi['patches']), 1)
        self.assertEqual(fi['patches'][0]['author'], 'Phil Ringnalda <philringnalda@gmail.com>')

        fi = hi.get(path, utils.get_timestamp('2008-01-01'), utils.get_timestamp('2009-01-01'))
        self.assertEqual(fi['authors']['hg@mozilla.com']['count'], 1)
        self.assertEqual(fi['authors']['hg@mozilla.com']['reviewers'], {})
        self.assertEqual(fi['bugs'], set())
        self.assertEqual(len(fi['patches']), 1)
        self.assertEqual(fi['patches'][0]['author'], 'hg@mozilla.com')

        fi = hi.get(path, utc_ts_to=utils.get_timestamp('2009-01-01'))
        self.assertEqual(len(fi['authors']), 1)
        self.assertEqual(fi['authors']['hg@mozilla.com']['count'], 1)
        self.assertEqual(fi['authors']['hg@mozilla.com']['reviewers'], {})
        self.assertEqual(fi['bugs'], set())
        self.assertEqual(len(fi['patches']), 1)
        self.assertEqual(fi['patches'][0]['author'], 'hg@mozilla.com')

        fi = hi.get(path, utils.get_timestamp('2006-01-01'), utils.get_timestamp('2007-01-01'))
        self.assertEqual(fi['authors'], {})
        self.assertEqual(fi['bugs'], set())
        self.assertEqual(fi['patches'], [])

        fi = hi.get(path, utils.get_timestamp('2008-01-01'), utils.get_timestamp('2012-01-01'))
        self.assertEqual(len(fi['authors']), 2)
        self.assertEqual(fi['authors']['Phil Ringnalda <philringnalda@gmail.com>']['count'], 1)
        self.assertEqual(len(fi['authors']['Phil Ringnalda <philringnalda@gmail.com>']['reviewers']), 1)
        self.assertEqual(fi['authors']['Phil Ringnalda <philringnalda@gmail.com>']['reviewers']['gerv'], 1)
        self.assertEqual(fi['authors']['hg@mozilla.com']['count'], 1)
        self.assertEqual(fi['authors']['hg@mozilla.com']['reviewers'], {})
        self.assertEqual(fi['bugs'], set(['547914']))
        self.assertEqual(len(fi['patches']), 2)
        self.assertEqual(fi['patches'][0]['author'], 'Phil Ringnalda <philringnalda@gmail.com>')
        self.assertEqual(fi['patches'][1]['author'], 'hg@mozilla.com')

    def test_hgfileinfo_author(self):
        path = 'LICENSE'
        hi = HGFileInfo(path)

        fi = hi.get(path, author='hg@mozilla.com')
        self.assertEqual(fi['authors']['hg@mozilla.com']['count'], 1)
        self.assertEqual(fi['authors']['hg@mozilla.com']['reviewers'], {})
        self.assertEqual(fi['bugs'], set())
        self.assertEqual(len(fi['patches']), 1)
        self.assertEqual(fi['patches'][0]['author'], 'hg@mozilla.com')

        self.assertEqual(fi, hi.get(path, utils.get_timestamp('2008-01-01'), utils.get_timestamp('2012-01-01'), author='hg@mozilla.com'))

    def test_hgfileinfo_multiple(self):
        path1 = 'netwerk/protocol/http/nsHttpConnectionMgr.cpp'
        path2 = 'LICENSE'
        hi = HGFileInfo([path1, path2])
        fi1 = hi.get(path1)
        fi2 = hi.get(path2)

        self.assertIn('authors', fi1)
        self.assertIn('authors', fi2)
        self.assertIsNotNone(fi1['authors'])
        self.assertIsNotNone(fi2['authors'])
        self.assertIn('bugs', fi1)
        self.assertIn('bugs', fi2)
        self.assertIsNotNone(fi1['bugs'])
        self.assertIsNotNone(fi2['bugs'])


if __name__ == '__main__':
    unittest.main()
