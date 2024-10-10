import subprocess
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel
from typing import Optional


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


def check_git_repo():
    """Check if the current directory is a git repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.stdout.strip() != "true":
            raise ValueError("This directory is not a git repository.")
    except subprocess.CalledProcessError:
        print("Error: This directory is not a git repository.")
        exit(1)


def get_last_merge_commit() -> str:
    """Get the last merge commit hash."""
    try:
        result = subprocess.run(
            ["git", "log", "--merges", "-1", "--format=%H"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        last_merge_commit = result.stdout.strip()
        if not last_merge_commit:
            raise ValueError("No merge commits found in this repository.")
        return last_merge_commit
    except subprocess.CalledProcessError as e:
        print("Error finding the last merge commit:", e)
        exit(1)


def get_git_changes_since_last_merge() -> str:
    """Get the git changes since the last merge commit."""
    last_merge_commit = get_last_merge_commit()
    try:
        result = subprocess.run(
            ["git", "diff", last_merge_commit, "HEAD"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error extracting git changes:", e)
        exit(1)


def create_prompt_template(git_changes: str, style: Style) -> str:
    """Create a prompt template using the git changes and style preferences."""
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
        "Based on these preferences, generate a concise summary of the above changes."
    )

    return template


def generate_summary(git_changes: str, style: Style) -> str:
    """Generate a summary using the given git changes and style preferences."""
    model = ChatOllama(model="llama3.1:latest", temperature=0)

    prompt = create_prompt_template(git_changes, style)

    response = model.invoke(prompt)
    return response.content


def main():
    """Main function to extract git changes, create a prompt, and generate a summary."""
    check_git_repo()

    git_changes = get_git_changes_since_last_merge()

    style = Style(
        language="English",
        formality="Professional",
        bullet_points=True,
        tone="Neutral",
        detail_level="Detailed",
        audience="Technical team",
        structure="Big picture, Detailed changes",
        emphasis="New features, bug fixes",
        length="Medium"
    )

    summary = generate_summary(git_changes, style)

    print("Summary of the changes since the last merge request:")
    print(summary)


if __name__ == "__main__":
    main()
