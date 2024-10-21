# AI Code-Reviewer and Summarizer

This project leverages Large Language Models (LLMs) to summarize Git changes for merge/pull requests and assist in code reviews. You can choose to set up this project either using Conda or Docker, based on your preference.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Option 1: Conda Installation](#option-1-conda-installation)
  - [Using the `setup.sh` Bash Script](#using-the-setupsh-bash-script-for-conda)
- [Option 2: Docker Installation](#option-2-docker-installation)
  - [Using the `setup.sh` Bash Script](#using-the-setupsh-bash-script-for-docker)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- [Poetry](https://python-poetry.org/docs/#installation) for dependency management.
- Python 3.10 or higher.
- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) (optional, for creating isolated environments).
- [Docker](https://docs.docker.com/get-docker/) (optional, for running the project in a container).
- Llama models installed locally (e.g., Llama 3.1 or 3.2).

---

## Option 1: Conda Installation

To install the project in a Conda environment, follow these steps:

### Step 1: Create a Conda Environment

```bash
conda create -n langchain python=3.10
conda activate langchain
```

### Step 2: Install Dependencies Using Poetry

1.	Clone the repository:
```bash
git clone https://github.com/your-repo/ai-code-reviewer.git
cd ai-code-reviewer
```

2.	Install dependencies using Poetry:
```bash
poetry install
```

#### Using the setup.sh Bash Script for Conda

You can also automate the setup process using the provided setup.sh script. This script will install the project dependencies, set up environment variables, and add bash aliases for running the cr (code reviewer) and mrs (merge request summarizer) commands.

1.	Ensure you have the necessary permissions to run the script:
```bash
chmod +x setup.sh
```

2.	Run the script:
```bash
./setup.sh
```

The script will create the Conda environment, install dependencies, and set up bash aliases for cr and mrs.

## Option 2: Docker Installation

You can choose to install and run the project using Docker, which will containerize the entire setup and allow you to run the cr and mrs commands outside the container in any directory.

### Step 1: Build the Docker Image

1.	Clone the repository:
```bash
git clone https://github.com/your-repo/ai-code-reviewer.git
cd ai-code-reviewer
```

2. Build the Docker image:
```bash
docker build -t ai-code-reviewer .
```

## Usage

### Code Reviewer (cr)

The cr command allows you to generate code reviews for various programming languages (e.g., Python, JavaScript, C++). You can run the code reviewer by using the cr alias:
```bash
cr "How do I create a simple publisher node in ROS2?"
```

Or, specify a file to review:
```bash
cr "Review the cylinder_area function" {path_to_examples}/area_example.py
```

Note: By default, the specialization is Python. You can change this by adding the flag --specialization=javascript, --specialization=cpp, or --specialization=typescript.

#### Git Summarizer (mrs)

The mrs command generates a summary of the Git changes since the last merge request / pull request. You must be in a Git repository to use this command:
```bash
mrs
```
This will provide you with a summarized report of the changes in your repository.

## Contributing

Contributions to the project are welcome! Feel free to open issues or submit pull requests for improvements, new features, or bug fixes.