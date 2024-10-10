# logger_setup.py
import os
import logging

def setup_loggers(log_dir):
    os.makedirs(log_dir, exist_ok=True)

    history_log_file = os.path.join(log_dir, "history.log")
    code_compare_log_file = os.path.join(log_dir, "code_compare.log")

    history_logger = logging.getLogger("historyLogger")
    code_compare_logger = logging.getLogger("codeCompareLogger")

    history_handler = logging.FileHandler(history_log_file)
    code_compare_handler = logging.FileHandler(code_compare_log_file)

    # Configure logging levels
    history_handler.setLevel(logging.INFO)
    code_compare_handler.setLevel(logging.INFO)

    history_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    code_compare_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    history_handler.setFormatter(history_formatter)
    code_compare_handler.setFormatter(code_compare_formatter)

    history_logger.addHandler(history_handler)
    code_compare_logger.addHandler(code_compare_handler)

    # Avoid propagation to root logger which could print to console
    history_logger.propagate = False
    code_compare_logger.propagate = False

    return history_logger, code_compare_logger


def log_conversation(history_logger, code_compare_logger, conversation):
    if "feedback" in conversation:
        history_logger.info("Final Feedback:\n%s", conversation["feedback"])

    if "code_compare" in conversation:
        code_compare_logger.info("Code Comparison:\n%s", conversation["code_compare"])

    if "rating" in conversation:
        history_logger.info("Rating:\n%s", conversation["rating"])
