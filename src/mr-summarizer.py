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


class Style(BaseModel):
    language: Optional[str] = "English"
    formality: Optional[str] = "Professional"
    bullet_points: Optional[bool] = True
    tone: Optional[str] = "Neutral"
    detail_level: Optional[str] = "Detailed"
    audience: Optional[str] = "Technical team"
    structure: Optional[str] = "Big picture, Detailed changes"
    emphasis: Optional[str] = "New features, bug fixes"
    length: Optional[str] = "Medium"


parser = PydanticOutputParser(pydantic_object=Style)


def check_git_repo():
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError:
        print("Error: This is not a git repository.")
        exit(1)


def extract_git_changes():
    try:
        subprocess.run(
            ["git", "diff", "HEAD~1", "HEAD", "-U0"],
            check=True,
            stdout=open("changes.diff", "w"),
        )
    except subprocess.CalledProcessError as e:
        print("Error extracting git changes:", e)
        exit(1)


def read_git_changes():
    try:
        with open("changes.diff", "r") as file:
            return file.read()
    except FileNotFoundError:
        print("Error: 'changes.diff' file not found.")
        exit(1)


def main():
    check_git_repo()
    extract_git_changes()
    git_changes = read_git_changes()

    style = Style()
    format_instructions = parser.get_format_instructions(style)

    template = (
        f"Summarize the following git changes for my colleagues since the last merge request:\n\n{git_changes}\n\n"
        f"Language: {style.language}\n"
        f"Formality: {style.formality}\n"
        f"Bullet Points: {style.bullet_points}\n"
        f"Tone: {style.tone}\n"
        f"Detail Level: {style.detail_level}\n"
        f"Audience: {style.audience}\n"
        f"Structure: {style.structure}\n"
        f"Emphasis: {style.emphasis}\n"
        f"Length: {style.length}\n\n"
        f"{format_instructions}"
    )

    prompt = PromptTemplate(
        template=template,
        input_variables=["git_changes"],
        partial_variables={"format_instructions": format_instructions},
    )

    prompt_and_model = prompt | model
    response = prompt_and_model.invoke({"git_changes": git_changes})

    print(response.content)


if __name__ == "__main__":
    main()
