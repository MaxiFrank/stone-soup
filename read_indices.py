import pdfplumber
import re
import pprint

"""other problem, most stories do overlap on a page...
basically OK except 
      activism. See also climate change activism; technology for activism; risks of
          activism; political activism     

      pollution. See water pollution; air pollution; ocean pollution; plastic pollution;
          soil pollution
then take out blank lines
new line is a little wonky

"""

def get_index() -> None:
    """
    Get the index pages and return arrays
    Note the start is page number - 1, and the end is just page number
    It writes the indices and preserves the PDF layout in indices.txt
    """
    with pdfplumber.open("book.pdf") as pdf:
        string = ""
        pages = pdf.pages[492:524]

        for page in pages:
            string += page.extract_text(layout=True)+ "\n"
        with open("indices.txt", "w") as f:
            f.write(string)

def parse_index(start:int, end:int):
    """
    this one needs to be processed_text.txt instead of indices.txt
    """
    with open("indices.txt", "r") as f:
        lines = f.readlines()
        return lines[start:end]

def parse_text(line: str):
    """
    take line and parse reference text and page numbers
    return the reference text (on the same line) and page numbers
    """
    regexp = re.compile(
        # r"^(?:\s{6})(?P<prefix>[^\d\s](?=\s\d))"
        # r"^(?:\s{6})(?P<reference_text>[A-Za-z][^\d]+)"
        r"^(?:\s{6})(?P<reference_text>[A-Za-z].+?)"
        r"(?P<page_number>\s\d+(?:,\s*\d+)*)"
        
        # r"(?P<page_number>\d+(?:,\s*\d+)*)"
    )
    result = regexp.search(line)
    if result == None:
        return None
    else:
        reference_text = result.group('reference_text').strip()
        page_number = result.group('page_number').strip()
        return reference_text, page_number

def check_prefix(line:str) -> str:
    """
    if a line starts with 6 spaces and then just text and there's a space + a number, then parse this as usual
    if a line starts with 6 spaces but is an uppercase character, then skip
    else if there are 6 spaces and no space and then number pattern, remember the line number.
        for as long as there are lines starting with 7 spaces, then a space and a number, 
        prepend the line number to the reference text.
    """

    # if a line starts with 6 spaces and then text and then a space and then one or more digits, parse
    regexp = re.compile(
        r"^(?:\s{6})(?P<prefix>[^\d\s][^\d]+)"
    )
    result = regexp.search(line)
    if result == None:
        return None
    else:
        prefix = result.group('prefix')
        return prefix

def to_concat(line):
    regexp = re.compile(
        r"(?P<text>^(\s{7}.*))"
    )
    result = regexp.search(line)
    if result == None:
        return False
    else:
        return True

def get_parsed_indices():
    tags = {}
    # makes indices.txt
    get_index()
    lines = parse_index(7, 1532)
    prefix_idx = None
    for idx, line in enumerate(lines):
        if len(line.strip()) < 1 or idx in [2, 3, 4, 1063, 1064]:
            continue
        result = parse_text(line)
        
        if result == None:            
            if check_prefix(line) is not None:                
                prefix_idx = idx
                continue
            elif to_concat(line):
                if prefix_idx is not None:
                    prefix = "".join((re.findall(r"^(?:\s{6})[A-Za-z\s]+",lines[prefix_idx]))).rstrip() + "\n"
                    new_line = prefix.rstrip() + " " + line.strip()
                    reference_text, page_number = parse_text(new_line)
                    tags[reference_text] = page_number
        else:
            reference_text, page_number = parse_text(line)
            prefix_idx = idx
            tags[reference_text] = page_number
            
    return tags
                    
    
if __name__ == "__main__":
    """
    10-12
    1071-1072
    """
    get_index()
    lines = parse_index(7, 1532)
    # pprint.pp(lines[2:5])
    # pprint.pp(lines[1063:1065])
    prefix_idx = None
    with open("parsed_indices.txt", "w") as f:
        for idx, line in enumerate(lines):
            f.write("-------------------------------------\n") 
            # print("-------------------------------------") 
            # print(line)
            # check if it fits the normal pattern
            # print(line)
            if len(line.strip()) < 1 or idx in [2, 3, 4, 1063, 1064]:
                f.write("empty line\n")
                continue
            # print("line length", len(line))
            # print("stripped line length", len(line.strip()))
            result = parse_text(line)
            # if not, check if there's 6 spaces and then no numbers
            # if so, remember the prefix line number, then
        # keep going to the next line for as long as it fits the pattern:
        #   lines starting with 7 spaces, then a space and a number, 
            # prepend the prefix to the reference text.
            #  then parse_text as if it's normal pattern
            
            if result == None:            
                if check_prefix(line) is not None:                
                    prefix_idx = idx
                    f.write("prefix-line\n")
                    continue
                elif to_concat(line):
                    if prefix_idx is not None:
                        # f.write("match stuff\n")
                        # f.write(str(re.findall(r"^(?:\s{6})[A-Za-z\s]+",lines[prefix_idx])).rstrip()+ "\n") 
                        prefix = "".join((re.findall(r"^(?:\s{6})[A-Za-z\s]+",lines[prefix_idx]))).rstrip() + "\n"
                        # f.write(prefix+"\n")
                        # f.write(str(len(prefix))+"\n")
                        # f.write(" ".join((re.findall(r"^(?:\s{6})[A-Za-z\s]+",lines[prefix_idx])))+line.strip())
                        # new_line = " ".join((re.findall(r"^(?:\s{6})[A-Za-z\s]+",lines[prefix_idx])))+line.strip()
                        new_line = prefix.rstrip() + " " + line.strip()
                        # print(new_line)
                        # print(new_line)
                        # print(len(new_line))
                        reference_text, page_number = parse_text(new_line)
                        # print(lines[prefix_idx].strip())
                        # print(line.lstrip())
                        f.write(reference_text+"\n")
                        f.write(page_number+"\n")
            else:
                reference_text, page_number = parse_text(line)
                prefix_idx = idx
                f.write(reference_text+"\n")
                f.write(page_number+"\n")
            
    

        


        
        

