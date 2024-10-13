import argparse
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
import os
import logger_setup
from prompts import prompts
from langchain_ollama import ChatOllama
import ttkbootstrap as ttk
from tkinter import scrolledtext, Toplevel, INSERT


model = ChatOllama(model="llama3.2", temperature=0)

def llm(x):
    return model.invoke(x).content


class GraphState(TypedDict):
    feedback: Optional[str] = None
    history: Optional[str] = None
    code: Optional[str] = None
    specialization: Optional[str] = None
    rating: Optional[str] = None
    iterations: Optional[int] = None
    code_compare: Optional[str] = None
    actual_code: Optional[str] = None


workflow = StateGraph(GraphState)


def handle_reviewer(state):
    history = state.get("history", "").strip()
    code = state.get("code", "").strip()
    specialization = state.get("specialization", "").strip()
    iterations = state.get("iterations")

    print("Reviewer working...")

    feedback = llm(prompts[specialization]["reviewer_start"].format(code))

    return {
        "history": history + "\n REVIEWER:\n" + feedback,
        "feedback": feedback,
        "iterations": iterations + 1,
    }


def handle_coder(state):
    history = state.get("history", "").strip()
    feedback = state.get("feedback", "").strip()
    code = state.get("code", "").strip()
    specialization = state.get("specialization", "").strip()

    print("CODER rewriting...")

    code = llm(prompts[specialization]["coder_start"].format(feedback, code))
    return {"history": history + "\n CODER:\n" + code, "code": code}


def handle_result(state):
    """Handle the final result, compute rating, and comparison."""
    print("Review done...")

    # Extract necessary information from the state
    history = state.get("history", "").strip()
    code1 = state.get("code", "").strip()
    code2 = state.get("actual_code", "").strip()
    specialization = state.get("specialization", "").strip()

    rating = llm(prompts[specialization]["rating_start"].format(history))
    
    code_compare = llm(prompts[specialization]["code_comparison"].format(code1, code2))
    return {"rating": rating, "code_compare": code_compare}


workflow.add_node("handle_reviewer", handle_reviewer)
workflow.add_node("handle_coder", handle_coder)
workflow.add_node("handle_result", handle_result)


def deployment_ready(state):
    specialization = state.get("specialization", "").strip()
    deployment_ready = (
        1
        if "yes"
        in llm(
            prompts[specialization]["classify_feedback"].format(
                state.get("code"), state.get("feedback")
            )
        )
        else 0
    )
    total_iterations = 1 if state.get("iterations") > 5 else 0
    return "handle_result" if deployment_ready or total_iterations else "handle_coder"


workflow.add_conditional_edges(
    "handle_reviewer",
    deployment_ready,
    {"handle_result": "handle_result", "handle_coder": "handle_coder"},
)

workflow.set_entry_point("handle_reviewer")
workflow.add_edge("handle_coder", "handle_reviewer")
workflow.add_edge("handle_result", END)


def show_custom_popup(root):
    """Create a custom pop-up window with a thumbs-up emoji, centered on the main window."""
    popup = Toplevel(root)
    popup.title("Copied!")
    popup.geometry("300x150")

    # Get the main window's dimensions and position
    root.update_idletasks()
    parent_x = root.winfo_x()
    parent_y = root.winfo_y()
    parent_width = root.winfo_width()
    parent_height = root.winfo_height()

    # Calculate the position to center the pop-up relative to the main window
    popup_x = parent_x + (parent_width // 2) - (300 // 2)
    popup_y = parent_y + (parent_height // 2) - (150 // 2)

    # Set the popup geometry to the calculated position
    popup.geometry(f"300x150+{popup_x}+{popup_y}")

    # Create a label with a thumbs-up emoji and text
    label = ttk.Label(popup, text="Copied to Clipboard! 👍", font=("Arial", 14))
    label.pack(pady=20)

    # Create an OK button to close the popup
    ok_button = ttk.Button(popup, text="OK", command=popup.destroy)
    ok_button.pack(pady=10)

    popup.transient(root)  # Ensure the popup is focused on top
    popup.grab_set()  # Make the window modal
    root.wait_window(popup)  # Wait for the popup to close before returning control


def main():
    parser = argparse.ArgumentParser(description="Run the multi-agent code reviewer.")
    parser.add_argument(
        "problem", type=str, help="The problem statement or code to review."
    )
    parser.add_argument(
        "files", type=str, nargs="*", help="Optional files containing the code to review."
    )
    parser.add_argument(
        "--save", type=str, default="src/log", help="Directory to save log files."
    )
    parser.add_argument(
        "--specialization",
        type=str,
        choices=["python", "typescript", "javascript", "cpp"],
        default=os.getenv(
            "DEFAULT_SPECIALIZATION", "python"
        ),  # Use environment variable if set
        help="Specialization of the reviewer.",
    )

    args = parser.parse_args()

    specialization = args.specialization

    # Combine code from multiple files, clearly marking each file
    if args.files:
        code = ""
        for file in args.files:
            with open(file, "r") as f:
                file_content = f.read()
                code += f"\n// File: {file}\n{file_content}\n"  # Label each file's code
    else:
        code = llm(args.problem)

    # Let LLM know that the code is from separate files
    app = workflow.compile()
    conversation = app.invoke(
        {
            "history": code,
            "code": code,
            "actual_code": code,
            "specialization": specialization,
            "iterations": 0,
        },
        {"recursion_limit": 100},
    )

    # Set up logging
    history_logger, code_compare_logger = logger_setup.setup_loggers(args.save)

    # Log conversation history and code comparison
    logger_setup.log_conversation(history_logger, code_compare_logger, conversation)

    print("\033[92m✔ See pop-up window for results.\033[0m")

    # Create the ttkbootstrap window
    root = ttk.Window(themename="superhero")
    root.title("Code Review Summary")

    # Create a scrolled text area to display the summary
    text_area = scrolledtext.ScrolledText(root, wrap="word", width=80, height=20)
    text_area.pack(padx=10, pady=10)
    text_area.insert(INSERT, f"Feedback: {conversation.get('feedback', '')}\n")
    text_area.insert(INSERT, f"Rating: {conversation.get('rating', '')}\n")

    # Create a button that shows a custom popup
    copy_button = ttk.Button(root, text="Copy to Clipboard", command=lambda: show_custom_popup(root))
    copy_button.pack(pady=10)

    # Center the main window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()