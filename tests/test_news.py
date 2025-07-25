import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import src.news_fetcher as nf

SAMPLE_RSS = Path(__file__).parent / "sample_rss.xml"

class DummyResponse:
    def __init__(self, data: bytes):
        self._data = data
    def read(self):
        return self._data
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        return False


def test_fetch_feed(monkeypatch):
    data = SAMPLE_RSS.read_bytes()

    def dummy_urlopen(url):
        return DummyResponse(data)

    monkeypatch.setattr(nf.urllib.request, 'urlopen', dummy_urlopen)
    items = nf.fetch_feed('dummy')
    assert len(items) == 2
    assert items[0]['title'] == 'Article 1'
    assert items[0]['link'] == 'http://example.com/article1'


def test_summarize_basic():
    text = "This is a sentence. This is another sentence. And a third one."
    summary = nf.summarize(text, max_words=5)
    assert summary.startswith("This is a sentence.")
