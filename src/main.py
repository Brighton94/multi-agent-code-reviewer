import argparse
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
import os
import logger_setup
from prompts import prompts
from langchain_ollama import ChatOllama

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


def main():
    parser = argparse.ArgumentParser(description="Run the multi-agent code reviewer.")
    parser.add_argument(
        "problem", type=str, help="The problem statement or code to review."
    )
    parser.add_argument(
        "file", type=str, nargs="?", help="Optional file containing the code to review."
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

    # Load code from file if provided
    if args.file:
        with open(args.file, "r") as file:
            code = file.read()
    else:
        code = llm(args.problem)

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

    # Print conversation parts
    print("Feedback:", conversation.get("feedback", ""))
    # print("Code Comparison:", conversation.get("code_compare", ""))
    print("Rating:", conversation.get("rating", ""))


if __name__ == "__main__":
    main()
