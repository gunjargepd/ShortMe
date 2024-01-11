import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
from shortme.settings import  CONTENT_SAFETY_AI_ENDPOINT, CONTENT_SAFETY_AI_KEY


key = CONTENT_SAFETY_AI_KEY
endpoint = CONTENT_SAFETY_AI_ENDPOINT

# Create an Azure AI Content Safety client
client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

def analyze_text(t):

    secure = True
    categories = []
    
    # Contruct request
    request = AnalyzeTextOptions(text=t)

    # Analyze text
    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze text failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise

    for c in response.categories_analysis:
        if int(c['severity']) > 1:
           secure = False
           categories.append(c['category'])

    return secure, categories

