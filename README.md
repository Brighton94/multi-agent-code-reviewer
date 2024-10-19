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


#### Option 1: Using Conda

1. Create a new Conda environment:

   ```sh
   conda create -n langchain python=3.10
   ```

2. Activate the environment:
   ```sh
   conda activate langchain
   ```

#### Option 2: Using Virtualenv

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

### Installing Ollama and Llama models

To use Ollama models, you need to install the [`ollama`](https://ollama.com/) package. 

1. Install Ollama by running the following command:

    ```sh
    curl -fsSL https://ollama.com/install.sh | sh
    ```

2. Verify the installation:

    ```sh
    ollama --version
    ```

3. Fetch and use Llama 3.1:

   ```sh
   ollama run llama3.1
   ```
   This fetches the default 8b param model. Once you are done, you can exit with `Ctrl + D`

4. Fetch and use Llama 3.2:

   ```sh
   ollama run llama3.2
   ```

### Using Models `llama3.1:8b` and `llama3.2`

⚠️ Warning: Performance Impact

<div style="background-color: #FFF3CD; padding: 10px; border-left: 4px solid #FFC107; color: #856404; margin-bottom: 20px;"> Running the `llama3.1:8b` and `llama3.2` models locally using Ollama can significantly slow down your machine due to the high computational requirements. Please ensure that you have sufficient system resources (CPU, GPU, and RAM) available. For more complex reviews, the duration may increase. Consider switching branches to the `gemini-reviewer` or use other cloud-based LLMs for faster performance if this becomes an issue.

</div>

## Usage

### Reviewer

Run the `main.py` script to generate the code review process. You must describe the problem in quotation marks. Optionally you can include a file containing the code to be reviewed. The default specialization of the reviewer is python, you at the moment, you can specify the specialization with this flag `--specialization=python` (`javascript`, `cpp` or `typescript`).

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
```

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
Open to contributions of all kinds. Changes, comments and suggestions. 

## License

## Project status

Ongoing project
