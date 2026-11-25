import os
import unittest
import json
import jc.parsers.m3u

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    # input
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/m3u-example.m3u'), 'r', encoding='utf-8') as f:
        m3u_example = f.read()

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/m3u-dirty.m3u'), 'r', encoding='utf-8') as f:
        m3u_dirty = f.read()

    # output
    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/m3u-example.json'), 'r', encoding='utf-8') as f:
        m3u_example_json = json.loads(f.read())

    with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/generic/m3u-dirty.json'), 'r', encoding='utf-8') as f:
        m3u_dirty_json = json.loads(f.read())


    def test_m3u_nodata(self):
        """
        Test 'm3u' parser with no data
        """
        self.assertEqual(jc.parsers.m3u.parse('', quiet=True), [])

    def test_m3u_example(self):
        """
        Test 'm3u' example file
        """
        self.assertEqual(jc.parsers.m3u.parse(self.m3u_example, quiet=True), self.m3u_example_json)

    def test_m3u_dirty(self):
        """
        Test 'm3u' example file with lots of difficult parsing
        """
        self.assertEqual(jc.parsers.m3u.parse(self.m3u_dirty, quiet=True), self.m3u_dirty_json)


    def test_m3u_extinf_without_path(self):
        """
        Test 'm3u' with #EXTINF: lines that are not followed by a path line
        """
        data = (
            '#EXTM3U\n'
            '#EXTINF:-1 tvg-id="movies.tv" group-title="Movies" tvg-logo="http://example.com/logo.png",Movies TV\n'
            '#http://example.com/movies\n'
            '#EXTINF:-1 tvg-id="kids.tv",Kids TV\n'
            'http://example.com/kids\n'
            '#EXTINF:105,Artist - 7" mix\n'
            '#EXTINF:321,Other Artist - Title\n'
            'music/b.ogg\n'
            '#EXTINF:-1 tvg-id="news.tv" group-title="News",News TV\n'
            '#EXTVLCOPT:network-caching=1000\n'
            'http://example.com/news\n'
            '#EXTINF:-1 tvg-id="last.tv",Last TV\n'
        )
        expected = [
            {
                'tvg-id': 'kids.tv',
                'runtime': -1,
                'display': 'Kids TV',
                'path': 'http://example.com/kids'
            },
            {
                'runtime': 321,
                'display': 'Other Artist - Title',
                'path': 'music/b.ogg'
            },
            {
                'tvg-id': 'news.tv',
                'group-title': 'News',
                'runtime': -1,
                'display': 'News TV',
                'path': 'http://example.com/news'
            }
        ]
        self.assertEqual(jc.parsers.m3u.parse(data, quiet=True), expected)

    def test_m3u_line_separator(self):
        """
        Test 'm3u' with a line-break character other than LF inside a field
        """
        data = '#EXTM3U\n#EXTINF:105,Artist - Intro\u2028http://example.com/a.mp3\nmusic/a.mp3\n'
        result = jc.parsers.m3u.parse(data, quiet=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['display'], 'Artist - Intro\u2028http://example.com/a.mp3')
        self.assertEqual(result[0]['path'], 'music/a.mp3')

    def test_m3u_cr_line_endings(self):
        """
        Test 'm3u' with CR-only line endings
        """
        data = '#EXTM3U\r#EXTINF:105,Artist - Title\rmusic/a.mp3\r#EXTINF:200,Other - Title\rmusic/b.mp3\r'
        result = jc.parsers.m3u.parse(data, quiet=True)
        self.assertEqual([x['path'] for x in result], ['music/a.mp3', 'music/b.mp3'])

    def test_m3u_attributes_only_before_title(self):
        """
        Test 'm3u' with key="value" text, '#' and repeated spaces in the title
        """
        data = ('#EXTM3U\n'
                '#EXTINF:-1 tvg-id="news.1" group-title="News",Kids tvg-id="x" group-title="Kids"\n'
                'http://example.com/a\n'
                '#EXTINF:-1 group-title="Local",El Paso #1  (720p) E=MC2\n'
                'http://example.com/b\n')
        result = jc.parsers.m3u.parse(data, quiet=True)
        self.assertEqual(result[0]['tvg-id'], 'news.1')
        self.assertEqual(result[0]['group-title'], 'News')
        self.assertEqual(result[0]['display'], 'Kids tvg-id="x" group-title="Kids"')
        self.assertEqual(result[1]['display'], 'El Paso #1  (720p) E=MC2')
        self.assertNotIn('E', result[1])


if __name__ == '__main__':
    unittest.main()
