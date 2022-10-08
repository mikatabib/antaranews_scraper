from os import writev
import re
import sys
import ngram
from pathlib import Path
from bs4 import BeautifulSoup


def normalize_text(text: str) -> str:
    FLAG = re.IGNORECASE | re.MULTILINE

    result = text.lower()
    result = re.sub(r"[^a-z0-9 -]", " ", result, flags=FLAG)
    result = re.sub(r"( +)", " ", result, flags=FLAG)
    result = re.sub(r" - ", " ", result, flags=FLAG)

    return result.strip()


# there is must be better way to do this
def okey_word(article: str):
    allowed_chars = set("abcdefghijklmnopqrstuvwxyz!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
    for word in article:
        for ch in word.strip():
            if ch not in allowed_chars:
                return False
        else:
            return True
    return False


BASE_DIR = Path(__file__).parent
ARCHIVE_DIR = BASE_DIR / "html"

# + html
# | + Y-m-d
# | | + [1-n]
# | | | + articles here

with open("full_text.txt", "a") as append:
    for dir in ARCHIVE_DIR.iterdir():
        for page_dir in dir.iterdir():
            for article in page_dir.iterdir():
                with open(article) as reader:
                    bs = BeautifulSoup(reader, "html.parser")

                for it in bs.find_all("b"):
                    if it.get_text().startswith("Baca juga"):
                        it.decompose()

                for it in bs.find_all(attrs={"class": "baca-juga"}):
                    it.decompose()

                for it in bs.find_all(attrs={"class": "text-muted small mt10"}):
                    it.decompose()

                for it in bs.find_all(["script", "style"]):
                    it.decompose()

                try:
                    find = bs.find(attrs={"class": "post-content clearfix"})
                    if find is None:
                        find = bs.find(attrs={"class": "post-wrapper clearfix"})
                        if find is None:
                            find = bs.find(attrs={"class": "single-post"})
                            paragraphs = [w for w in find.get_text().split()]
                        else:
                            paragraphs = [w for w in find.get_text().split()]
                    else:
                        paragraphs = [
                            it.get_text().strip()
                            for it in find
                            if it.get_text().strip() != ""
                        ]

                    for idx, it in enumerate(paragraphs):
                        if "(ANTARA) -" in it:
                            start = paragraphs[idx].index("(ANTARA) -")
                            end = start + len("(ANTARA) -")
                            paragraphs[idx] = it[end:]
                            break

                    article = normalize_text(" ".join(paragraphs)).split()
                    article = " ".join(filter(okey_word, article))
                    append.write(article + " ")

                except Exception as err:
                    print(article)
                    print(err)
