# Script to
# 1. Convert XML data to a pandas dataframe
# 2. Inspect quality of data



# -------------------------------------------
# LIBRARIES
# -------------------------------------------
import pandas as pd
import xml.etree.ElementTree as ElT
import re
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
from tqdm import tqdm

# -------------------------------------------
# FUNCTIONS
# -------------------------------------------

def parse_xml_to_csv(path, save_path=None):
    """
    Open .xml posts dump and convert the text to a csv, tokenizing it in the
         process
    :param path: path to the xml document containing posts
    :return: a dataframe of processed text
    """

    # Use python's standard library to parse XML file
    doc = ElT.parse(path)
    root = doc.getroot()

    # Each row is a question
    all_rows = [row.attrib for row in root.findall("row")]

    print(all_rows[0].keys())
    # Using tdqm to display progress since preprocessing takes time
    for item in tqdm(all_rows):

        try:
            # Decode text from HTML

            if 'Text' in item:
                soup = BeautifulSoup(item["Text"], features="html.parser")
                item["body_text"] = soup.get_text()
            else:
                item["body_text"] = "No Text"

        except:
            item["body_text"] = "ERR GENERATED"

    # Create dataframe from our list of dictionaries
    df = pd.DataFrame.from_dict(all_rows)

    # save data
    if save_path:
        df.to_csv(save_path)
    return df


# -------------------------------------------
# MAIN
# -------------------------------------------

# constants
PATH                = r'..\..\data\stack_exchange\raw'
SAVE_PATH           = r'C:\Users\nrosh\Desktop\Personal Coding Projects\Python\ml-powered-applications\neel\dataframes'
PATTERN_REGEX_XML   = r'(\w+)(.xml)'

# get file names
xml_file_names = [re.match(PATTERN_REGEX_XML, f)[1] for f in listdir(PATH) if isfile(join(PATH, f))]

# convert data to csv and save to file
for fn in xml_file_names:
    if "PostHistory" in fn:
        data_path = PATH + '\\' + fn + '.xml'
        save_path = SAVE_PATH + '\\' + fn + '.csv'
        # df = parse_xml_to_csv(data_path, save_path=save_path)
        parse_xml_to_csv(data_path, save_path=save_path)

    
# print(df.info())
