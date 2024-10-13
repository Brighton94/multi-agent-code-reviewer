# AI Code-Reviewer and -Summarizer

This project uses LLMs to summarize Git changes and assist in code reviews.

# README

## Project Overview

This project leverages LangGraph and LangChain to create applications using language models. It includes scripts for generating summaries, running workflows, and more.

## Installation

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) (optional, for creating isolated environments)

### Setting Up the Environment

#### Using Conda

1. Create a new Conda environment:

   ```sh
   conda create -n langchain python=3.10
   ```

2. Activate the environment:
   ```sh
   conda activate langchain
   ```

#### Using Virtualenv

1. Create a virtual environment:

   ```sh
   python -m venv langchain
   ```

2. Activate the virtual environment:
   - On Windows:
     ```sh
     .\langchain\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source langchain/bin/activate
     ```

### Installing Dependencies

This project uses `pyproject.toml` for dependency management instead of `requirements.txt`. Follow these steps to install the dependencies:

1. Install Poetry:

   ```sh
   pip install poetry
   ```

2. Install the project dependencies:
   ```sh
   poetry install
   ```

## Using Ollama Models

### Installing Ollama

To use Ollama models, you need to install the [`ollama`](https://ollama.com/) package. This is already included in the `pyproject.toml`, so it will be installed with the other dependencies.

### Using Models `llama3.1:8b` and `llama3.2`

⚠️ Warning: Performance Impact

<div style="background-color: #FFF3CD; padding: 10px; border-left: 4px solid #FFC107; color: #856404; margin-bottom: 20px;"> Running the `llama3.1:8b` and `llama3.2` models locally using Ollama can significantly slow down your machine due to the high computational requirements. Please ensure that you have sufficient system resources (CPU, GPU, and RAM) available.
Expect the review process to take at least 6 minutes. For more complex reviews, the duration may increase. Consider switching branches to the `gemini-reviewer` or use other cloud-based LLMs for faster performance if this becomes an issue.

</div>

## Usage

### Reviewer

Run the `main.py` script to generate the code review process. You must describe the problem in quotation marks. Optionally you can include a file containing the code to be reviewed. The default specialization of the reviewer is python, you at the moment, you can specify the specialization with this flag `--specialization=python` (`javascript`, `cpp` or `typescript`). 
```

Include the following lines in your `.bashrc` file with the correct path to `main.py`:

```sh
export CODE_REVIEWER_PATH="{path_to_main.py}/main.py"
export DEFAULT_SPECIALIZATION="python"  # Set your default specialization here
alias cr="python \$CODE_REVIEWER_PATH"
```

Then run,

```sh
source ~/.bashrc
```

Run `cr --help` for more info.

Here are some examples of the usage:

```sh
cr "How do I create a simple publisher node in ROS2?"
```

or

```sh
cr "Review the cylinder_area function" area_example.py

### Summarizer

Run the `mr-summarizer.py` script to generate a summary of the Git changes since the last merge request:

```sh
python src/mr-summarizer.py
```

You can also add these lines to the `.bashrc` file:

```sh
export MR_SUMMARIZER_PATH="$HOME/ma-code-reviewer/src/mr-summarizer.py"
alias mrs="python \$MR_SUMMARIZER_PATH"
```

After updating the `.bashrc` file, make sure to source it to apply the changes:

```sh
source ~/.bashrc
```

You just need to be in a git repository and run `mrs` in the terminal.

**N.B:** These commands do not work inside docker containers. They would need to be echoed in someway.

## Contributing

State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment

Show your appreciation to those who have contributed to the project.

## License

For open source projects, say how it is licensed.

## Project status

If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.

```

```
