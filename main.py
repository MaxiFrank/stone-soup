from read_stories import parse_stories
from read_indices import get_parsed_indices
from read_table_of_content import get_table_of_contents
import json
import pandas as pd


"""
last part of the project, figure out whether the tag should belong in one or another when end page of article a
is the same as the start age of article b
"""


def make_indices_json():
    # these are my tags
    indices = get_parsed_indices()
    with open("indices.json", "w") as indices_file:
        indices_file.write(json.dumps(indices))
    indices_file.close()


def make_stories_json():
    # this is my stories
    stories = parse_stories()
    with open("stories.json", "w") as stories_file:
        stories_file.write(json.dumps(stories))
    stories_file.close()


def make_contents_json():
    # this is table of content
    table_of_contents = get_table_of_contents()
    json_table_of_content = json.dumps(table_of_contents)
    with open("contents.json", "w") as f:
        f.write(json_table_of_content)
    # pprint.pp(table_of_contents)
    f.close()


def load_contents():
    with open("output/contents.json", "r") as contents_file:
        return json.load(contents_file)


def load_stories():
    with open("output/stories.json", "r") as stories_file:
        return json.load(stories_file)


def load_indices():
    with open("output/indices.json", "r") as indices_file:
        return json.load(indices_file)


def parse_num_string(page_numbers):
    numbers = [int(num.strip()) for num in page_numbers.split(",")]
    return numbers


def calculate_score(story, keywords):
    score = 0
    for keyword in keywords:
        if keyword in story:
            score += 1
    return score


def flatten(story):
    text = ""
    for sentence in story:
        text += sentence
    return text


if __name__ == "__main__":
    # make_indices_json()
    # make_stories_json()
    # make_contents_json()

    # stories
    stories = load_stories()
    # table of content
    contents = load_contents()
    # indices are actually tags
    indices = load_indices()

    # Attach story to the right person in contents
    for id, values in contents.items():
        # change the key in stories to match the person in values
        # except the last one because I just don't have an end date,
        # that one I should just copy and paste into the parsed values.
        if "person" in values and values["person"] in stories:
            person = values["person"]
            if person in stories:
                contents[id]["story"] = stories[person]

    for tag, page_numbers in indices.items():
        nums_l = parse_num_string(page_numbers)
        individual_words = [word.strip() for word in tag.split(" ")]

        for num in nums_l:
            prev_id = None
            # for a specific page number
            prev_end_page = None
            prev_story_score = None
            # find the article that has an interval that contains this number start:end inclusive
            for id, values in contents.items():
                start = None
                end = None
                if "start_page_number" in values and values["start_page_number"]:
                    start = int(values["start_page_number"])
                if "end_page_number" in values and values["end_page_number"]:
                    end = int(values["end_page_number"])
                if start and end and num >= start and num <= end:
                    if prev_end_page is not None:
                        if start == prev_end_page:
                            if "story" in values and values["story"]:
                                current_story_score = calculate_score(
                                    flatten(values["story"]), individual_words
                                )
                                if current_story_score > prev_story_score:
                                    # add tag to current story
                                    contents[id]["tags"] = contents[id].get("tags", [])
                                    contents[id]["tags"].append(tag)
                                    # take tag out of previous story
                                    contents[prev_id]["tags"].remove(tag)
                    else:
                        if "story" in values and values["story"]:
                            contents[id]["tags"] = contents[id].get("tags", [])
                            contents[id]["tags"].append(tag)
                            prev_story_score = calculate_score(
                                flatten(values["story"]), individual_words
                            )
                            prev_id = id
                            prev_end_page = end

    with open("test/output.json", "w") as output_file:
        output_file.write(json.dumps(contents))
    output_file.close()

    with open("test/output.json") as output_file:
        df = pd.read_json(output_file)
        df.T.to_csv("test/tags_book_2.csv")
