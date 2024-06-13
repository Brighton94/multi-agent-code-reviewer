from dotenv import load_dotenv
import subprocess
import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel
from typing import Optional

# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("No GOOGLE_API_KEY provided")

genai.configure(api_key=GOOGLE_API_KEY)
model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

# style = """American English  \
#          formal  \
#          in bullet points \
#          """


class Style(BaseModel):
    language: Optional[str]
    formality: Optional[str]
    bullet_points: Optional[bool]


parser = PydanticOutputParser(pydantic_object=Style)


# def llm(x):
#     return model.invoke(x).content


def main():
    # 1: Extract Git Changes
    subprocess.run(
        ["git", "diff", "HEAD~1", "HEAD", "-U0"], stdout=open("changes.diff", "w")
    )

    # 2: Read the Git Changes
    with open("changes.diff", "r") as file:
        git_changes = file.read()

    # 3: Summarize Using an LLM
    # prompt = f"Summarize the following git changes for my colleagues since the last merge request:\n\n{git_changes} into a style that is {style}"

    template = f"Summarize the following git changes for my colleagues since the last merge request:\n\n{git_changes}"

    prompt = PromptTemplate(
        template=template,
        input_variables=["git_changes"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    # response = llm(prompt)

    prompt_and_model = prompt | model
    response = prompt_and_model.invoke({"git changes": git_changes})

    print(response.content)


main()
