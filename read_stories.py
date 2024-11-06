import pdfplumber
import re

"other problem, most stories do overlap on a page..."

MAKE_INDEX = True


def get_index():
    """
    Get the index pages and return arrays
    Note the start is page number - 1, and the end is just page number
    """
    with pdfplumber.open("book.pdf") as pdf:
        string = ""
        pages = pdf.pages[30:462]

        for page in pages:
            string += page.extract_text_simple() + "\n"
        with open("test/stories.txt", "w") as f:
            f.write(string)
    MAKE_INDEX = False


def parse_index(start, end):
    with open("test/stories.txt", "r") as f:
        lines = f.readlines()
        return lines[start:end]


"""
1. grab line with |, text before on same line is person, text after on the same line is location (done)
2. when I find this pattern, give me the line above, which will be title
"""


def parse_text(line):
    # do multi-line and get the line before
    regexp = re.compile(
        # r"\n^(?P<title>(?:[A-Za-z:]+\s?)+)\n"
        r"^\s*(?P<person>[^|]+[^\s|])\s*"
        r"\|\s*(?P<location>.+)$",
    )
    result = regexp.search(line)
    if result == None:
        return None
    else:
        person = result.group("person").strip()
        location = result.group("location").strip()
        return person, location


def parse_stories():
    get_index()
    text = parse_index(0, 13978)
    prev = None
    next = None
    prev_person = None
    # chapters = None
    excerpts = {}
    for idx, line in enumerate(text):
        if parse_text(line) is not None:
            person, location = parse_text(line)
            # chapters[person] = {"location": location}
            next = idx - 1
            title = text[next]
            if next:
                excerpt = text[prev:next]
                excerpts[prev_person] = excerpt
            prev_person = person
            prev = next

    return excerpts


if __name__ == "__main__":
    # I must have writted into processed_stories.txt here
    # I think there's some refactoring that I did but didn't take good notes on
    get_index()
    text = parse_index(0, 13978)
    prev = None
    next = None
    prev_person = None
    excerpts = {}
    # chapters = {}
    for idx, line in enumerate(text):
        if parse_text(line) is not None:
            person, location = parse_text(line)
            # chapters[person] = {'location': location}

            print("person text is", person)
            print("location is", location)
            print("---------------------------------------")
            next = idx - 1

            title = text[next]

            if next:
                excerpt = text[prev:next]

                excerpts[prev_person] = excerpt
            prev_person = person
            prev = next
    print(excerpts["Jamie Margolin"])
    print(excerpts["Lilly Platt"])
