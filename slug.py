from slugify import slugify
from pathlib import Path

ARCHIVE = Path(__file__).parent / 'html'
for date_dir in ARCHIVE.iterdir():
    for page_dir in date_dir.iterdir():
        for article in page_dir.iterdir():
            original_filename = article.name
            slugified = slugify(original_filename)
            article.rename(slugified)
