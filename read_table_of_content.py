import pdfplumber
import pprint
import re

"""
Read PDF table of contents
"""


def get_index():
    """
    Get the index pages and return arrays
    Note the start is page number - 1, and the end is just page number
    """
    with pdfplumber.open("book.pdf") as pdf:
        string = ""
        pages = pdf.pages[21:28]

        for page in pages:
            string += page.extract_text_simple() + "\n"
        with open("test/table_of_content.txt", "w") as f:
            f.write(string)


def parse_index(start, end):
    with open("test/table_of_content.txt", "r") as f:
        lines = f.readlines()
        return lines[start:end]


def get_table_of_contents():
    get_index()
    lines = parse_index(11, 216)
    d = {}
    order = 0
    include = True
    for idx in range(len(lines) - 1):
        if "...." not in lines[idx]:
            person = lines[idx + 1].split(",")[0]
            title = lines[idx].strip()
            start_page_number = "".join(re.findall("(?<=\.)[0-9]+", lines[idx + 1]))
            d[order] = {
                "person": person,
                "title": title,
                "start_page_number": start_page_number,
            }
            order += 1
            include = False
        elif include == False:
            include = True
        elif include == True:
            title = "".join(re.findall("[^.0-9]", lines[idx].strip()))
            start_page_number = "".join(re.findall("(?<=\.)[0-9]+", lines[idx]))

            d[order] = {"title": title, "start_page_number": start_page_number}
            order += 1

    for num in range(len(d) - 1):
        d[num]["end_page_number"] = d[num + 1]["start_page_number"]
    return d


if __name__ == "__main__":
    get_index()
    lines = parse_index(11, 216)
    d = {}

    order = 0
    include = True
    for idx in range(len(lines) - 1):
        if "...." not in lines[idx]:
            person = lines[idx + 1].split(",")[0]
            title = lines[idx].strip()
            start_page_number = "".join(re.findall("(?<=\.)[0-9]+", lines[idx + 1]))
            d[order] = {
                "person": person,
                "title": title,
                "start_page_number": start_page_number,
            }
            order += 1
            include = False
        elif include == False:
            include = True
        elif include == True:
            title = "".join(re.findall("[^.0-9]", lines[idx].strip()))
            start_page_number = "".join(re.findall("(?<=\.)[0-9]+", lines[idx]))

            d[order] = {"title": title, "start_page_number": start_page_number}
            order += 1

    for num in range(len(d) - 1):
        d[num]["end_page_number"] = d[num + 1]["start_page_number"]
    pprint.pp(d)
