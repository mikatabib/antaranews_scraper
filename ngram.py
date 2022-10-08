import nltk
import time
from pathlib import Path


def generate_bigram(text: str) -> tuple:
    tokens = nltk.tokenize.word_tokenize(text)
    bigrams = nltk.bigrams(tokens)
    frequency = nltk.FreqDist(bigrams)
    return tuple(frequency.items())


def generate_monogram(text: str) -> tuple:
    tokens = nltk.tokenize.word_tokenize(text)
    frequency = nltk.FreqDist(tokens)
    return tuple(frequency.items())


def load_monogram():
    with open("monogram.txt") as reader:
        lines = reader.read().strip()

    monogram = {}
    for line in lines:
        w, v = line.split()
        monogram[w] = int(v)

    return monogram


def load_bigram():
    with open("bigram.txt") as reader:
        lines = reader.read().strip()

    bigram = {}
    for line in lines:
        a, b, v = line.split()
        bigram[(a, b)] = int(v)

    return bigram


if __name__ == "__main__":
    bigram = {}
    with open("./full_text.txt") as reader:
        text = reader.read()

    with Path(f"./bigram-{file_id}.txt").open("w") as writer:
        for (a, b), f in generate_bigram(text):
            # ignore short words or low frequency
            if f < 100 or len(a) == 1 or len(b) == 1:
                continue
            writer.write(f"{a} {b} {f}\n")
