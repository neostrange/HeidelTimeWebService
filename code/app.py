from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
from py_heideltime import py_heideltime
import re
    

def process(text, dct):
    results = py_heideltime(text, language='English', date_granularity="day", document_type='news', document_creation_time= dct)
    #return results[2]

    annotatedText = results[2]
    root  = ET.Element("TIMEXES")
    pattern = r'<TIMEX3.*?>(.*?)</TIMEX3>'

    match = re.search(pattern, annotatedText)
    while (match):
        start_index = match.start() # Start index of the xml tag
        end_index = match.end() # End index of the xml tag
        text_span = match.group(1) # Text span within the xml tag
        start = match.start(1) # the start index of the span in the original text
        end = match.end(1) # the end index of the span in the original text
        original_st_index = start - start_index
        original_end_index = end - start + start_index

        child1 = ET.fromstring(match.group())

        child1.set("start_index", str(start_index))
        child1.set("end_index", str(original_end_index))
        root.append(child1)
        
        #print(f"Tag: {match.group(1)}, Text: {match.group(2)}, Start index: {start_index}, End index: {end_index}")
        
        annotatedText = re.sub(match.group(), f"{match.group(1)}", annotatedText, count=1)

        match = re.search(pattern, annotatedText)

        if not match:
            break
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
