from dotenv import load_dotenv
from openai import OpenAI
import os
from pypdf import PdfReader
import gradio as gr
from docx import Document


load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set - please head to the troubleshooting guide in the setup folder")
from openai import OpenAI
#GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
#gemini = OpenAI(base_url=GEMINI_BASE_URL, api_key=openai_api_key)


class Me:

    def __init__(self):
        self.openai = OpenAI()
    # self.gemini = OpenAI(base_url=GEMINI_BASE_URL, api_key=openai_api_key)
       # self.name = "Ed Donner"
        reader = PdfReader("me/FarmSecure.pdf")
        self.farmsecure = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.farmsecure += text
        

        # Load the Word file
        doc = Document("me/Questionire.docx")
        self.questionire = ""
        # Read all text from paragraphs
        for para in doc.paragraphs:
           self.questionire += para.text
        print(self.questionire)


    def system_prompt(self):
        system_prompt = f"You are acting as customer support for farmer. You are a Customer Support Agent for FarmSecure who can connect with \
            Indian farmers, understand their needs, and provide clear, compassionate, and knowledgeable assistance.\
                 The ideal candidate will handle inquiries related to farming, farming insurance, farming products, government schemes, weather updates,\
                     and digital agriculture tools\
Your responsibility is to ensure that the farmer gets the best possible service from the company. \
You are given a summary of possible questionire and FarmSecure documents which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client \
    If you don't know the answer to any question, say politly so, even if it's about something trivial or unrelated"


        system_prompt += f"\n\n## Questionire:\n{self.questionire}\n\n## FarmSecure Document:\n{self.farmsecure}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as customer support agent for farming needs."
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        response = self.openai.chat.completions.create(model="gpt-5-mini", messages=messages)
        #response = self.gemini.chat.completions.create(model="gemini-2.5-flash-preview-05-20", messages=messages, metadata={})
        return response.choices[0].message.content
    

if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch(share=True)
    