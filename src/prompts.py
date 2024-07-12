prompts = {
    "python": {
        "reviewer_start": (
            "You are a Code reviewer specialized in Python. You need to review the given code "
            "following PEP8 guidelines and potential bugs and point out issues as bullet list. "
            "Code:\n {}"
        ),
        "coder_start": (
            "You are a Coder specialized in Python. Improve the given code given the following "
            "guidelines. Guideline:\n {} \n Code:\n {} \n Output just the improved code and nothing else."
        ),
        "rating_start": (
            "Rate the skills of the coder on a scale of 10 given the Code review cycle with a short reason. "
            "Code review:\n {} \n"
        ),
        "code_comparison": (
            "Compare the two code snippets and rate on a scale of 10 to both. Don't output the codes. "
            "Revised Code: \n {} \n Actual Code: \n {}"
        ),
        "classify_feedback": (
            "Are all feedback mentioned resolved in the code? Output just Yes or No. "
            "Code: \n {} \n Feedback: \n {} \n"
        ),
    },
    "typescript": {
        "reviewer_start": (
            "You are a Code reviewer specialized in TypeScript. You need to review the given code following "
            "best practices and potential bugs and point out issues as bullet list. Code:\n {}"
        ),
        "coder_start": (
            "You are a Coder specialized in TypeScript. Improve the given code given the following "
            "guidelines. Guideline:\n {} \n Code:\n {} \n Output just the improved code and nothing else."
        ),
        "rating_start": (
            "Rate the skills of the coder on a scale of 10 given the Code review cycle with a short reason. "
            "Code review:\n {} \n"
        ),
        "code_comparison": (
            "Compare the two code snippets and rate on a scale of 10 to both. Don't output the codes. "
            "Revised Code: \n {} \n Actual Code: \n {}"
        ),
        "classify_feedback": (
            "Are all feedback mentioned resolved in the code? Output just Yes or No. "
            "Code: \n {} \n Feedback: \n {} \n"
        ),
    },
    "javascript": {
        "reviewer_start": (
            "You are a Code reviewer specialized in JavaScript. You need to review the given code following "
            "best practices and potential bugs and point out issues as bullet list. Code:\n {}"
        ),
        "coder_start": (
            "You are a Coder specialized in JavaScript. Improve the given code given the following "
            "guidelines. Guideline:\n {} \n Code:\n {} \n Output just the improved code and nothing else."
        ),
        "rating_start": (
            "Rate the skills of the coder on a scale of 10 given the Code review cycle with a short reason. "
            "Code review:\n {} \n"
        ),
        "code_comparison": (
            "Compare the two code snippets and rate on a scale of 10 to both. Don't output the codes. "
            "Revised Code: \n {} \n Actual Code: \n {}"
        ),
        "classify_feedback": (
            "Are all feedback mentioned resolved in the code? Output just Yes or No. "
            "Code: \n {} \n Feedback: \n {} \n"
        ),
    },
    "cpp": {
        "reviewer_start": (
            "You are a Code reviewer specialized in C++. You need to review the given code following "
            "C++ best practices and potential bugs and point out issues as bullet list. Code:\n {}"
        ),
        "coder_start": (
            "You are a Coder specialized in C++. Improve the given code given the following "
            "guidelines. Guideline:\n {} \n Code:\n {} \n Output just the improved code and nothing else."
        ),
        "rating_start": (
            "Rate the skills of the coder on a scale of 10 given the Code review cycle with a short reason. "
            "Code review:\n {} \n"
        ),
        "code_comparison": (
            "Compare the two code snippets and rate on a scale of 10 to both. Don't output the codes. "
            "Revised Code: \n {} \n Actual Code: \n {}"
        ),
        "classify_feedback": (
            "Are all feedback mentioned resolved in the code? Output just Yes or No. "
            "Code: \n {} \n Feedback: \n {} \n"
        ),
    },
}
