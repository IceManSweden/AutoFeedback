from generator.feedback import FeedbackGenerator
from os import path, listdir
from time import perf_counter
from fnmatch import fnmatch
import pathspec

# Select Model

# Select Assignment

# Select Files / Folder With files.

# Generate a feedback report.

scanDir = "/home/ice/Dev/AutoFeedback/b2-crud"


def loadGitignore(scanDir):
    gitignorePath = path.join(scanDir, ".gitignore")

    if not path.isfile(gitignorePath):
        return None

    with open(gitignorePath, "r", encoding="utf-8") as file:
        return pathspec.GitIgnoreSpec.from_lines(file)


def isIgnored(filepath, scanDir, gitignoreSpec):
    if gitignoreSpec is None:
        return False

    relativePath = path.relpath(filepath, scanDir).replace("\\", "/")
    return gitignoreSpec.match_file(relativePath)


def recursiveFindFiles(directory, scanDir=None, gitignoreSpec=None):
    if scanDir is None:
        scanDir = directory
        gitignoreSpec = loadGitignore(scanDir)

    files = []

    for file in listdir(directory):
        fullPath = path.join(directory, file)

        if isIgnored(fullPath, scanDir, gitignoreSpec):
            continue

        if path.isdir(fullPath):
            files.extend(recursiveFindFiles(fullPath, scanDir, gitignoreSpec))

        elif path.isfile(fullPath):
            if file.endswith(".js"):
                files.append(fullPath)

    return files


def readFileContents(files):
    content = []
    for f in files:
        file = open(f)
        content.append(f)
        content.append(file.read(-1))
    return content


def createReport(name, content):
    f = open(f"feedback_{name}.md", "w+")
    f.write(f"\n# {name}\n")
    f.writelines(content)
    f.close()
    print(f"report created: feedback_{name}.md")


def main():
    filepaths = recursiveFindFiles(scanDir)
    print("Files Found to be processed", filepaths)
    content = readFileContents(filepaths)

    gen = FeedbackGenerator()
    # model="gemma4:latest
    timeStart = perf_counter()

    # Runs to single prompt.
    single = gen.singlePrompt(content)
    print(f"Single Prompt Time Taken: {round(perf_counter()- timeStart, 2)}s")
    createReport("singleprompt", single)

    # Runs the pipeline.
    timeStart = perf_counter()
    pipe = gen.pipeline(content, dir=scanDir)
    print(f"Pipeline Time Taken: {round(perf_counter()- timeStart, 2)}s")

    createReport("pipeline", pipe)


if __name__ == "__main__":
    main()
