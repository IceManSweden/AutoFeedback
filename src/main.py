from generator.feedback import FeedbackGenerator
from os import path, listdir

# Select Model

# Select Assignment

# Select Files / Folder With files.

# Generate a feedback report.
content = []

filePath = "src/"

if path.isdir(filePath):
    files = listdir(filePath)
    print(files)
    for f in files:
        if path.isfile(filePath + f):
            content.append(open(filePath + f).read(-1))
elif path.isfile(filePath):
    if path.isfile(filePath):
        content.append(open(filePath).read(-1))
    else:
        print(f"Not a valid directory or file {filePath}")
        exit(0)
else:
    print(f"Not a valid directory or file {filePath}")
    exit(0)

print(content)

gen = FeedbackGenerator()
# model = "gemma4:latest"

feedback = []
feedback.append(gen.singlePrompt(content))
feedback.append(gen.pipeline(content))

# Creates a report file with the feedback from both methods.
f = open("feedback.md", "w+")
f.write("# Single Prompt Feedback\n\n")
f.writelines(feedback[0])
f.write("\n\n\n\n\n\n# Pipeline Feedback\n\n")
f.writelines(feedback[1])
f.close()
