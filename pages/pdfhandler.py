from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
import pprint
import os
import requests
import warnings

fieldset = [b'Date of assault(s)']
rapedate = "5/1/2023"
stateoccurred = "California"

def extract_form_fields(pdf_path):
    with open(pdf_path, 'rb') as file:
        parser = PDFParser(file)
        doc = PDFDocument(parser)
        global rapedate
        form_fields = {}

        if 'AcroForm' in doc.catalog:
            fields = resolve1(doc.catalog['AcroForm']).get('Fields', [])
            for field in fields:
                field = resolve1(field)
                name, value = field.get('T'), field.get('V')
                if name in fieldset:
                    form_fields[name] = value
                    if name == b'Date of assault(s)':
                        rapedate = value

        return form_fields

filename = "./Filledform.pdf"

# filled_fields = extract_form_fields(filename)


import json
os.environ["GOOGLE_API_TOKEN"] = "67905247868-1t708l9c0bpfktmvhd6m09bkppbo6jj2.apps.googleusercontent.com"
os.environ["OPENAI_API_KEY"] = "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"

import secrets
import json

import openai

MODEL = "gpt-3.5-turbo"

prompt = f"""
A girl was raped on {rapedate}, 
when does she have to press charges based on {stateoccurred} law? 
Export as a list of calendar events spanning the maximum dates of opportunities for each legal action that can be taken starting from {rapedate}. 
For the description of each event, include the relevant institutions that should be engaged and how to present her case to them. 
Output as a JSON object. """

# An example of a system message that primes the assistant to explain concepts in great depth
def GetResult(filename):
    try:
        extract_form_fields(filename)
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": prompt},
            ],
            temperature=0,
        )

        asdict = json.loads(response["choices"][0]["message"]["content"])
        with open("textresult.txt","w") as f:
            pprint.pprint(asdict,f)

        events = asdict['events']
        with open("events.txt","w") as f:
            pprint.pprint(events,f)

        institutions = asdict['institutions']
        with open("institutions.txt","w") as f:
            pprint.pprint(institutions,f)
        return json.dumps(asdict, indent=4)
    except Exception as e:
        return str(e)
# # Create a GoogleCalendarAPI object
# calendar_api = GoogleCalendarAPI(creds)
#
# # Create a new calendar called "4pm" if it does not exist
# calendar_api.create_calendar('4pm')
