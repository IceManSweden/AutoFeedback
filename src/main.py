from generator.feedback import FeedbackGenerator

# Select Model

# Select Assignment

# Select Files / Folder With files.

# Generate a feedback report.

code = """

"""

gen = FeedbackGenerator(model="gemma4:latest")

print(gen.singlePrompt([code]))
print(gen.pipeline([code]))
