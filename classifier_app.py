import streamlit as st
import requests
from bs4 import BeautifulSoup
#from google.cloud import language_v1
#from annotated_text import annotated_text

"""
# Brand Safety Classifier
Add a URL to run through the classifier. It may take 5-10 seconds to complete the task! The text model is based on the Google Clound NL API and Brand Safety Classifier.
"""

st.write("hello!")
URL = 'https://www.cbsnews.com/news/gun-control-biden-bill-into-law/'
input = st.text_area("Insert Text", URL)


def sample_classify_text(input):
    """
    Classifying Content in a String

    Args:
      text_content The text content to analyze. Must include at least 20 words.
    """

    client = language_v1.LanguageServiceClient()


    language = "en"
    #document = {"content": text_content, "type_": type_, "language": language}

    response = client.classify_text(request = {'document': document})
    # Loop through classified categories returned from the API
    for category in response.categories:

        st.write(u"Category name: {}".format(category.name))

        st.write(u"Confidence: {}".format(category.confidence))

URL = input
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

i=0
for para in soup.find_all("p"):
    if(len(str(para)) > 175):
        st.write("paragraph #",str(i))
        st.write(para.get_text())
        text_content = para.get_text()
        #sample_classify_text(text_content=text_content)
        i+=1
        
