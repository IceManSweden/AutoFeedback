from generator.feedback import FeedbackGenerator
from os import path, listdir
from time import perf_counter

# Select Model

# Select Assignment

# Select Files / Folder With files.

# Generate a feedback report.

scanDir = "src/"


def recursiveFindFiles(directory, depth=0):
    files = []
    for file in listdir(directory):
        full_path = path.join(directory, file)

        if path.isdir(full_path):
            files.extend(recursiveFindFiles(full_path, depth + 1))

        elif path.isfile(full_path):
            if file.endswith(".py"):
                files.append(full_path)

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
    single = gen.singlePrompt(content)
    print(f"Single Prompt Time Taken: {round(perf_counter()- timeStart, 2)}s")
    createReport("singleprompt", single)

    timeStart = perf_counter()
    pipe = gen.pipeline(content)
    print(f"Pipeline Time Taken: {round(perf_counter()- timeStart, 2)}s")

    createReport("pipeline", pipe)


if __name__ == "__main__":
    main()
