import json
import pprint

def parse_text(start, end):
    with open("raw_text.txt", "r") as f:
        lines = f.readlines()
        return lines[start:end]
    
def make_last_story_json():
    # these are my tags
    lines = parse_text(0, 151)
    with open("raw_text.json", "w") as file:
        file.write(json.dumps(lines))
    file.close()

def load_last_story():
    with open('raw_text.json') as file:
        return json.load(file)
    

if __name__ == "__main__":
    make_last_story_json()
    output = load_last_story()
    print(output)