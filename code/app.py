from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
from py_heideltime import py_heideltime
import re

def process(text, dct):
    results = py_heideltime(text, language='English', date_granularity="day", document_type='news', document_creation_time= dct)
    #return results[2]

    annotatedText = results[2]

    # Regex pattern to match the xml tags
    pattern = re.compile(r'<TIMEX3.*?>(.*?)</TIMEX3>')
    root  = ET.Element("TIMEXES")
    # Get the text without the xml tags
    text_without_tags = pattern.sub("", annotatedText)

    # Iterate through the matches
    for match in pattern.finditer(annotatedText):
        start_index = match.start() # Start index of the xml tag
        end_index = match.end() # End index of the xml tag
        text_span = match.group(1) # Text span within the xml tag
        start = match.start(1) # the start index of the span in the original text
        end = match.end(1) # the end index of the span in the original text
        original_st_index = start - start_index
        original_end_index = end - start + start_index
        # print(f"Text span: {text_span}, st: {start}, end: {end}, Start index: {start_index}, End index: {end_index}")
        # print(f"original start index: {start_index}, original end index: {original_end_index}")
        # print(match.group())

        child1 = ET.fromstring(match.group())

        child1.set("start_index", str(start_index))
        child1.set("end_index", str(original_end_index))
        root.append(child1)
    tree = ET.ElementTree(root)

    return tree
    

app = Flask(__name__)

@app.route("/annotate", methods=["POST"])
def annotate():
    # Get the input string from the request
    input_string = request.json["input"]
    dct = request.json["dct"]

    tree = process(input_string, dct=dct)

    # Perform the annotation
    # root = ET.Element("root")
    # text = ET.SubElement(root, "text")
    # text.text = input_string

    # # Create the XML document
    # #tree = ET.ElementTree(root)
    return ET.tostring(tree.getroot(), encoding='utf-8').decode()
    # Return the XML document as a string
    #return ET.tostring(tree.getroot(), encoding='utf8').decode()

if __name__ == "__main__":
    app.run(debug=True)
