# Media_Competitors

Simple tool for fetching headlines from multiple news sources via RSS and generating short summaries.

## Setup

1. (Optional) Install `transformers` to enable advanced summarization:
   ```bash
   pip install transformers
   ```
   The application will run without this package but will fall back to a simple text truncation.

2. Edit `sources.json` to add or remove RSS feeds.

## Usage

Run the script:

```bash
python -m src.news_fetcher
```

The output lists the latest headlines with summaries and links back to the original articles in Markdown format.
