from dotenv import load_dotenv
import google.generativeai as genai
import subprocess
import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("No GOOGLE_API_KEY provided")

style = """American English  \
         formal  \
         in bullet points \ """


def main():

    genai.configure(api_key=GOOGLE_API_KEY)
    model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

    # 1: Extract Git Changes
    subprocess.run(
        ["git", "diff", "HEAD~1", "HEAD", "-U0"], stdout=open("changes.diff", "w")
    )

    # 2: Read the Git Changes
    with open("changes.diff", "r") as file:
        git_changes = file.read()

    # 3: Summarize Using an LLM
    prompt = f"Summarize the following git changes for my colleagues from the previous merge request:\n\n{git_changes} into a style that is {style}"

    response = model.generate_content(prompt)
    print(response.text)
