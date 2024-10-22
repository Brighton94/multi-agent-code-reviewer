import subprocess
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel
from typing import Optional
import ttkbootstrap as ttk
from tkinter import scrolledtext, Tk, WORD, INSERT, Toplevel, Label, Button


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


def show_custom_popup(parent):
    """Create a custom pop-up window with a thumbs-up emoji, centered on the main window."""
    popup = Toplevel(parent)
    popup.title("Copied!")
    popup.geometry("300x150")

    parent_x = parent.winfo_x()
    parent_y = parent.winfo_y()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()

    popup_x = parent_x + (parent_width // 2) - (300 // 2)
    popup_y = parent_y + (parent_height // 2) - (150 // 2)

    popup.geometry(f"300x150+{popup_x}+{popup_y}")

    label = Label(popup, text="Copied to Clipboard! 👍", font=("Arial", 14))
    label.pack(pady=20)

    ok_button = Button(popup, text="OK", command=popup.destroy)
    ok_button.pack(pady=10)

    popup.transient(parent)  
    popup.grab_set() 
    parent.wait_window(popup)  


def show_summary_in_ttkbootstrap(summary: str):
    """Show the generated summary in a ttkbootstrap window, bring it to the front, and center it."""
    def copy_to_clipboard():
        root.clipboard_clear()
        root.clipboard_append(text_area.get(1.0, INSERT))
        
        show_custom_popup(root)

    root = Tk()
    root.title("Git Summary")

    text_area = scrolledtext.ScrolledText(root, wrap=WORD, width=80, height=20)
    text_area.pack(padx=10, pady=10)
    text_area.insert(INSERT, summary)

    copy_button = Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
    copy_button.pack(pady=10)

    root.update_idletasks()  
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


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

    print("\033[92m✔ See pop-up window for results.\033[0m")

    show_summary_in_ttkbootstrap(summary)


if __name__ == "__main__":
    main()
