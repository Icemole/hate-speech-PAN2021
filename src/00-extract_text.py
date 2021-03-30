import re, sys, os

## Extracts the text from a line
## given the format of the PAN2021 competition.
def get_text_from_xml_line(line):
    search_pattern = "\<document\>\<\!\[CDATA\[(.*)\]\]\>\<\/document\>"  ## Backslash everything lul
    result = re.search(search_pattern, line)
    return None if result is None else result.group(1)


## Extracts all text from all .xml files of a single language
## passed as a parameter, given the format of the PAN2021 competition.
def extract_lang(lang):
    filepath = "data/" + lang + "/"
    nonhaters_file = "data/nonhaters_" + lang + ".txt"
    haters_file = "data/haters_" + lang + ".txt"
    err_file = "data/err.txt"

    with open(nonhaters_file, "w") as f_nonhaters, \
            open(haters_file, "w") as f_haters, \
            open(err_file, "w") as f_err:
        for xml in os.listdir(filepath):
            #print(filepath + xml)
            if xml == "truth.txt":
                ## Not interested in this file (contains references)
                continue
            with open(filepath + xml, "r") as f:
                f_contents = list(f)
                author_class = f_contents[0].split()[2].split('"')[1]
                if author_class == "0":
                    # Non-hater
                    f = f_nonhaters
                elif author_class == "1":
                    # Hater
                    f = f_haters
                else:
                    # Unidentified class
                    f = f_err
                for i in range(2, len(f_contents)): #1+ intended
                    text = get_text_from_xml_line(f_contents[i])
                    if text != None:
                        f.write(text + "\n")
            

def main():
    extract_lang("en")
    extract_lang("es")


if __name__ == "__main__":
    main()