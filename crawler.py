import time
import datetime
import requests
from pathlib import Path
from bs4 import BeautifulSoup

INDEX_URL = "https://www.antaranews.com/indeks"
# I have no need for request delay
# my internet is slow enough to test my patience
SLEEP_DURATION = 0.0

BASE_DIR = Path(__file__).parent
ARCHIVE_DIR = BASE_DIR / "html"

start_date = datetime.date(2019, 10, 16)
# yesterday news is the *limit*
# too lazy to implement way around news refreshes
end_date = (datetime.datetime.today() - datetime.timedelta(1)).date()

for day in range((end_date - start_date).days):
    date = (start_date + datetime.timedelta(day)).strftime("%d-%m-%Y")
    index_page = requests.post(f"{INDEX_URL}/{date}")

    bs = BeautifulSoup(index_page.text, "html.parser")
    uls = bs.find(attrs={"class": "pagination pagination-sm"})

    page_indexes = []
    for li in uls.find_all("li"):
        label = li.a.get_text()
        if label.isdecimal():
            n = int(label)
            page_indexes.append(n)

    start = min(page_indexes)
    end = max(page_indexes)

    current_date_dir = ARCHIVE_DIR / date
    if not current_date_dir.exists():
        current_date_dir.mkdir()

    for idx in range(start, end + 1):
        current_page_dir = current_date_dir / str(idx)
        if not current_page_dir.exists():
            current_page_dir.mkdir()

        index = requests.post(f"{INDEX_URL}/{date}/{idx}").text
        bs = BeautifulSoup(index, "html.parser")
        find = bs.find_all(attrs={"class": "simple-post simple-big clearfix"})
        for it in find:
            slug = it.find("p", attrs={"class": "slug"})
            if slug is not None:
                slug = slug.get_text().strip()
                if slug in {"Video", "Foto"}:
                    continue

            url = it.div.a["href"]
            title = it.div.a["title"].strip()
            category = it.header.find(attrs={"class": "simple-share"}).a.get_text()
            release_datetime = it.header.find(
                attrs={"class": "simple-share"}
            ).span.get_text()
            print(f"HALAMAN: {idx}", url, title, category, release_datetime)

            filename = f"{category}_{title}.html".replace("/", " ")
            current = current_page_dir / filename
            if not current.exists():
                article = requests.post(url).text
                current.write_text(article)
            time.sleep(SLEEP_DURATION)
