import streamlit as st
import requests
from bs4 import BeautifulSoup
from google.cloud import language_v1 as gc
from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account
from annotated_text import annotated_text

"""
# NL Content Classifier
Add a URL and set parameters to run the demo classifier. The text model is based on the Google Clound NL API..
"""

# Get user inputs
URL = 'https://www.theguardian.com/commentisfree/joris-luyendijk-banking-blog/2011/nov/09/goldman-sachs-elevator-gossip-tweets'
Text = 'The small plane carrying a pilot and two passengers was travelling north over Haulover Inlet Bridge when it crashed into an SUV travelling southbound, Miami-Dade police said in a press release. The plane then caught fire and fire officials discovered a body in the plane while extinguishing the flames.'



# Show option based on user selection 


input_type = st.radio(
"Select Input ",
('URL', 'Free Text'))


# Show input fields based on user selection 

if input_type == 'Free Text':
     input_text = st.text_area("Insert Free Text", Text ) 
     text_content = input_text
elif input_type == 'URL':         
     input_text = st.text_area("Insert URL", URL)
     text_content = input
else:
     pass
     
 # Set threshold
input_threshold = st.slider(label="Set confidence threshold", min_value=0.1, max_value=1.0, value=0.7, step=.1)


# Define the NL API function
def classify_text(text_content):
    """
    Classifying Content in a String

    Args:
      text_content The text content to analyze. Must include at least 20 words.
    """

    credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
    )
    client = gc.LanguageServiceClient(credentials=credentials)
 


    # Available types: PLAIN_TEXT, HTML
    if input_type == 'Free Text':
         type_ = gc.Document.Type.PLAIN_TEXT
    else:
         type_ = gc.Document.Type.HTML 

    #document = {"content": text_content, "type_": type_}
    model = {"v2Model": {"contentCategoriesVersion": 'V2'}}
     
    document = {"content": text_content, "type_": type_, "language": language}
    response = client.classify_text(request = {'document': document}, {'classificationModelOptions': model})
    # Loop through classified categories returned from the API
    for category in response.categories:
          
        #st.write(u"Category name: {}".format(category.name))
        #st.write(u"Confidence: {}".format(category.confidence))
          
        if category.confidence >= input_threshold:
            signal = category.name
               
            # Note that the following output only details the first category and confidence that affects the brand safety flag   
            st.write(u"Category name: {}".format(category.name))
            st.write(u"Confidence: {}".format(category.confidence))   
          
    return signal




# If free text is detected, run the content moderation without URL scraping     
if input_type == 'Free Text':
   text_content = input_text
   signal = classify_text(text_content = text_content)
   background = "#dcdcdc"
   annotated_text(
   (text_content, signal, background),
   )

# Scrape URL and run classifier
elif input_type == 'URL': 
   text_content = input_text
   signal = classify_text(text_content = text_content)
   background = "#dcdcdc"
   annotated_text(
   (text_content, signal, background),
   )
        
