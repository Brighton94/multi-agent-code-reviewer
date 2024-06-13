# AI Code-Reviewer and -Summarizer

This project uses LLMs to summarize Git changes and assist in code reviews.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Google API Key

### Installation

1. Clone the repository:

```sh
git clone http://lu-plm-actualitas.csir.co.za/software-sig/code-reviewer.git
```

2. Install the required Python packages:

```sh
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Google API Key:

```env
GOOGLE_API_KEY=your_google_api_key
```

## Usage

### Reviewer

Run the `main.py` script to generate the code review process. You must describe the problem in quotation marks. Optionally you can include a file containing the code to be reviewed. Here is an example

```sh
python src/main.py "How do I create a simple publisher node in ROS2 using Python?"
```

````sh
python src/main.py "Review the cylinder_area function" area_example.py

Include the following lines in your `.bashrc` file with the correct path to `main.py`:

```sh
export CODE_REVIEWER_PATH="{path_to_main.py}/main.py"
alias cr="python \$CODE_REVIEWER_PATH"
````

Then run,

```sh
source ~/.bashrc
```

Run `cr --help` for more info.

### Summarizer

Run the `mr-summarizer.py` script to generate a summary of the Git changes since the last merge request:

```sh
python src/mr-summarizer.py
```

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
