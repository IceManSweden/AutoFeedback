from os import path, listdir
from time import perf_counter
from fnmatch import fnmatch
import pathspec
from .generator.feedback import FeedbackGenerator
import sys

project_path = None
assignment_path = None

# Gets the arguments.
if sys.argv[1]:
    fn = sys.argv[1]
    if path.exists(fn):
        print(f"Performing feedback on the folder {path.basename(fn)}")
    project_path = fn
else:
    print("No project files were provided!")
    exit(1)

if sys.argv[2]:
    fn = sys.argv[2]
    if path.exists(fn):
        print(f"Assignment provided: {path.basename(fn)}")
    assignment_path = fn


def load_gitignore(scan_dir):
    """Gets the gitignore in the project folder.

    Args:
        scan_dir: The project directory path

    Returns:
        The gitignore.
    """
    gitignore_path = path.join(scan_dir, ".gitignore")

    if not path.isfile(gitignore_path):
        return None

    with open(gitignore_path, "r", encoding="utf-8") as file:
        return pathspec.GitIgnoreSpec.from_lines(file)


def is_ignored(filepath, scan_dir, gitignoreSpec):
    """Checks if the a file or directory is ignored by the .gitignore

    Args:
        filepath: files path.
        scan_dir: Directory used.
        gitignoreSpec: The gitignore object.

    Returns:
        Whether the file is ignored or not.
    """
    if gitignoreSpec is None:
        return False

    relative_path = path.relpath(filepath, scan_dir).replace("\\", "/")
    return gitignoreSpec.match_file(relative_path)


def recursive_find_files(directory, scan_dir=None, gitignoreSpec=None):
    """Finds the project files recursively using the gitignore

    Args:
        directory: Directory.
        scan_dir: directory to be scanned.
        gitignoreSpec: The gitignore object.

    Returns:
        The File paths found.
    """
    if scan_dir is None:
        scan_dir = directory
        gitignoreSpec = load_gitignore(scan_dir)

    files = []

    for file in listdir(directory):
        fullPath = path.join(directory, file)

        if is_ignored(fullPath, scan_dir, gitignoreSpec):
            continue

        if path.isdir(fullPath):
            files.extend(recursive_find_files(fullPath, scan_dir, gitignoreSpec))

        elif path.isfile(fullPath):
            if file.endswith(".js"):
                files.append(fullPath)

    return files


def read_files_content(files) -> list[str]:
    """Reads the files contents.

    Args:
        List of the files paths

    Returns:
        A list of the files content including the filename.
    """
    content = []
    for f in files:
        file = open(f)
        # Writes the header of the file content.
        document = ""
        document += f"# {f}\n```{str(f).split('.')[-1]}\n"
        document += file.read(-1)
        document += "```\n"

        content.append(document)
    return content


def create_feedback_report(name, content, dest):
    """Creates a feedback report file.

    Args:
        name: The name of the report.
        content: The content for the report.
        dest: The target destination.

    """
    f = open(f"{dest}/feedback_{name}.md", "w+")
    f.write(f"\n# {name}\n")
    f.writelines(content)
    f.close()
    print(f"report created: feedback_{name}.md")


def main():
    filepaths = recursive_find_files(project_path)
    print("Files Found to be processed", filepaths)
    content = read_files_content(filepaths)
    assignment_content = None
    if assignment_path:
        assignment_content = read_files_content([assignment_path])[0]

    create_feedback_report("Content", content, project_path)

    generator = FeedbackGenerator(model="qwen3:8b")
    # model="gemma4:latest
    time_start = perf_counter()

    # Runs to single prompt.
    single = generator.single_prompt(content, assignment=assignment_content)
    print(f"Single Prompt Time Taken: {round(perf_counter()- time_start, 2)}s")
    create_feedback_report("singleprompt", single, project_path)

    # Runs the pipeline.
    time_start = perf_counter()
    pipe = generator.pipeline(content, dir=project_path, assignment=assignment_content)
    print(f"Pipeline Time Taken: {round(perf_counter()- time_start, 2)}s")

    create_feedback_report("pipeline", pipe, project_path)


if __name__ == "__main__":
    main()
