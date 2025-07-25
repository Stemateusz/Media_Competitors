import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from typing import List, Dict

try:
    from transformers import pipeline  # type: ignore
    _summarizer = pipeline('summarization')
except Exception:
    _summarizer = None


def load_sources(path: str) -> List[Dict[str, str]]:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('sources', [])


def fetch_feed(url: str) -> List[Dict[str, str]]:
    with urllib.request.urlopen(url) as resp:
        content = resp.read()
    root = ET.fromstring(content)
    items = []
    for item in root.findall('.//item'):
        title_el = item.find('title')
        link_el = item.find('link')
        desc_el = item.find('description')
        if title_el is None or link_el is None:
            continue
        title = title_el.text or ''
        link = link_el.text or ''
        description = desc_el.text if desc_el is not None else ''
        items.append({'title': title, 'link': link, 'description': description})
    return items


def summarize(text: str, max_words: int = 60) -> str:
    if _summarizer is not None:
        try:
            res = _summarizer(text, max_length=max_words, min_length=max_words//2, do_sample=False)
            return res[0]['summary_text']
        except Exception:
            pass
    words = text.split()
    summary = ' '.join(words[:max_words])
    if len(words) > max_words:
        summary += '...'
    return summary


def main(config_path: str = 'sources.json', limit: int = 5) -> None:
    sources = load_sources(config_path)
    for source in sources:
        print(f"# {source['name']}")
        try:
            entries = fetch_feed(source['rss'])
        except Exception as e:
            print(f"Failed to fetch {source['rss']}: {e}")
            continue
        for entry in entries[:limit]:
            summary = summarize(entry.get('description', ''))
            title = entry['title']
            link = entry['link']
            print(f"- [{title}]({link}): {summary}")
        print()


if __name__ == '__main__':
    main()
