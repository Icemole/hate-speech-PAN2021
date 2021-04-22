import re, sys, os, argparse

## Extracts the text from a line
## given the format of the PAN2021 competition.
def get_text_from_xml_line(line):
    search_pattern = "\<document\>\<\!\[CDATA\[(.*)\]\]\>\<\/document\>"  ## Backslash everything lul
    result = re.search(search_pattern, line)
    return None if result is None else result.group(1)


## Extracts all text from all .xml files of a single language
## passed as a parameter, given the format of the PAN2021 competition.
def extract_lang(lang, filepath, group_writer):
    if group_writer:
        nonhaters_file = filepath + "nonhaters_" + lang + "_grouped.txt"
        haters_file = filepath + "haters_" + lang + "_grouped.txt"
    else:
        nonhaters_file = filepath + "nonhaters_" + lang + ".txt"
        haters_file = filepath + "haters_" + lang + ".txt"
    err_file = "data/err.txt"

    with open(nonhaters_file, "w") as f_nonhaters, \
            open(haters_file, "w") as f_haters, \
            open(err_file, "w") as f_err:
        for xml in os.listdir(filepath):
            #print(filepath + xml)
            if xml == "truth.txt":
                # Not interested in this file (contains references)
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
                for i in range(2, len(f_contents)):
                    text = get_text_from_xml_line(f_contents[i])
                    if text != None:
                        if group_writer:
                            f.write(text + " ")
                        else:
                            f.write(text + "\n")
                if group_writer:
                    f.write("\n")
            

def main():
    def str2bool(v):
        if isinstance(v, bool):
            return v
        if v.lower() == 'true':
            return True
        elif v.lower() == 'false':
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    parser = argparse.ArgumentParser()
    parser.add_argument('--extract_to', default='data/plain_text/',
                        help='Where to write the output of the data extraction')
    parser.add_argument('--group_writer', type=str2bool, nargs='?', const=True, default=False,
                        help='If set to True, one line of the extracted text will correspond to all sentences of a single writer')
    args = parser.parse_args()
    extract_lang("en", args.extract_to, args.group_writer)
    extract_lang("es", args.extract_to, args.group_writer)


if __name__ == "__main__":
    main()
