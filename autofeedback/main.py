from os import path, listdir
from time import perf_counter
from fnmatch import fnmatch
import pathspec
from autofeedback.generator.feedback import FeedbackGenerator

# Select Model

# Select Assignment

# Select Files / Folder With files.

# Generate a feedback report.

project_path = "/home/ice/Dev/AutoFeedback/b2-crud"


def load_gitignore(scanDir):
    gitignorePath = path.join(scanDir, ".gitignore")

    if not path.isfile(gitignorePath):
        return None

    with open(gitignorePath, "r", encoding="utf-8") as file:
        return pathspec.GitIgnoreSpec.from_lines(file)


def is_ignored(filepath, scanDir, gitignoreSpec):
    if gitignoreSpec is None:
        return False

    relativePath = path.relpath(filepath, scanDir).replace("\\", "/")
    return gitignoreSpec.match_file(relativePath)


def recursive_find_files(directory, scanDir=None, gitignoreSpec=None):
    if scanDir is None:
        scanDir = directory
        gitignoreSpec = load_gitignore(scanDir)

    files = []

    for file in listdir(directory):
        fullPath = path.join(directory, file)

        if is_ignored(fullPath, scanDir, gitignoreSpec):
            continue

        if path.isdir(fullPath):
            files.extend(recursive_find_files(fullPath, scanDir, gitignoreSpec))

        elif path.isfile(fullPath):
            if file.endswith(".js"):
                files.append(fullPath)

    return files


def read_files_content(files):
    content = []
    for f in files:
        file = open(f)
        content.append(f)
        content.append(file.read(-1))
    return content


def create_feedback_report(name, content):
    f = open(f"feedback_{name}.md", "w+")
    f.write(f"\n# {name}\n")
    f.writelines(content)
    f.close()
    print(f"report created: feedback_{name}.md")


def main():
    filepaths = recursive_find_files(project_path)
    print("Files Found to be processed", filepaths)
    content = read_files_content(filepaths)

    gen = FeedbackGenerator()
    # model="gemma4:latest
    time_start = perf_counter()

    # Runs to single prompt.
    single = gen.single_prompt(content)
    print(f"Single Prompt Time Taken: {round(perf_counter()- time_start, 2)}s")
    create_feedback_report("singleprompt", single)

    # Runs the pipeline.
    time_start = perf_counter()
    pipe = gen.pipeline(content, dir=project_path)
    print(f"Pipeline Time Taken: {round(perf_counter()- time_start, 2)}s")

    create_feedback_report("pipeline", pipe)


if __name__ == "__main__":
    main()
