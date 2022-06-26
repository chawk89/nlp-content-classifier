import streamlit as st
import requests
from bs4 import BeautifulSoup
from google.cloud import language_v1 as gc
from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account
from annotated_text import annotated_text

"""
# Brand Safety Classifier
Add a URL to run through the classifier. It may take 5-10 seconds to complete the task! The text model is based on the Google Clound NL API and Brand Safety Classifier.
"""

URL = 'https://www.cbsnews.com/news/gun-control-biden-bill-into-law/'
input = st.text_area("Insert Text", URL)
input2 = st.multiselect(
     'Which categories should be flaffed?',
     ['Sensitive Subjects', 'Adult'],
     ['Sensitive Subjects'])
input3 = st.slider(label="Set confidence threshold", min_value=0.1, max_value=1.0, value=0.7, step=.1)



def sample_classify_text(text_content):
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
    type_ = gc.Document.Type.PLAIN_TEXT

    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    response = client.classify_text(request = {'document': document})
    
    # Define the brand safety signal, and assume safe unless indicated otherise:
    signal = 'brand safe'
    # Loop through classified categories returned from the API
    for category in response.categories:
        st.write(u"Category name: {}".format(category.name))
        st.write(u"Confidence: {}".format(category.confidence))
        if input2 in category.name and category.confidence >= input3 and signal == 'brand safe':
            signal = 'brand unsafe'
    return signal
URL = input
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

i=0
for para in soup.find_all("p"):
    if(len(str(para)) > 175):
        st.write("paragraph #",str(i))
        text_content = para.get_text()
        st.write(text_content)
        annotated_text(

        (text_content, signal),
        
        )
        sample_classify_text(text_content = text_content)
        i+=1
        
