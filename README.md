# AutoFeedback

**AutoFeedback** is tool that is developed to examine the different software designs can effect Feedback generation using LLM's.

## Prerequisites

Stuff needed

- [Ollama](https://ollama.com/)
  - [Documentation](https://github.com/ollama/ollama-python)
- [Python](https://www.python.org/)

### Installing Ollama

Install [Ollama](https://ollama.com/) following the official guide

### Installing Python packages

To install the required packages needed to run the application.  
Run the following in the a Terminal

```bash
python3 -m pip install -r requirements.txt
```

This project is dependant on the following python packages

- Ollama
- Pathspec

## Run AutoFeedback

To run AutoFeedback run the following command in the terminal in the root project directory.

```bash
python3 -m autofeedback.main path/to/documents path/to/assignment
```

When running the program it will attempt to load a LLM model (default qwen3:0.8b) on the target ollama instance. Upon the program completion it will unload the model on the target to recover claimed system resources.
When you provide the path for the file or directory. The program looks for `.gitignore` and the ignores following the files and directories.
