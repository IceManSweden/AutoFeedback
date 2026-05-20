from autofeedback.generator.feedbacktools.eslint_tool import run_eslint
from autofeedback.generator.llm_handler import LLMManager
from ollama import ChatResponse


class FeedbackPipeline:
    def __init__(self, llm: LLMManager):
        self.llm = llm

    def file_analysis(self, file_content, assignment) -> str:
        """Analyses a specific file and generates feedback using tools
        Args:
            file_content: the content of a specific file.
            assignment: the content of the assignment.
        Returns:
            The feedback generated of a specific file.
        """
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. that provides constructive feedback on code.",
            }
        ]

        messages.append(
            {
                "role": "user",
                "content": f"Get the result from running eslint on the provided file. and evaluate the code. {file_content}, with this assignment this file may only be a part of the assignment. {assignment}",
            }
        )

        tool_result = self.llm.chat(tool=True, messages=messages)

        messages.append(tool_result.message)

        if tool_result.message.tool_calls:
            for call in tool_result.message.tool_calls:
                if call.function.name == "run_eslint":
                    result = run_eslint(**call.function.arguments)

                    messages.append(
                        {
                            "role": "tool",
                            "tool_name": call.function.name,
                            "content": str(result),
                        }
                    )

        messages.append(
            {
                "role": "user",
                "content": "Provide formative feedback based on the linting and code and metrics syntax quality, structure correctness and effiency",
            }
        )
        summery = self.llm.chat(
            messages=messages,
        )

        return summery

    def run(self, inputFiles=[], dir=".", assignment=None):
        """Runs the pipeline method
        Args:
            inputFiles: The contents of relevant files.
            dir: directory of the project.
            assignment: The assignment content.

        Returns:
            The feedback generated.
        """

        print("\n\nRunning Pipeline:")

        # Sets up the LLM.
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. that provides constructive feedback on code.",
            }
        ]

        feedbacks = []
        file_feedback = ""
        # Adds the input files.
        for f in inputFiles:
            data = self.file_analysis(f, assignment)
            feedbacks.append(data)
            file_feedback += data

        # Tool Message.

        questions = [
            "Provide direct feedback on only the Syntax on the code above. ",
            "Provide direct feedback on only the structure on the code above",
            "Provide direct feedback on only the Correctness on the code above",
            "Provide direct feedback on only the Efficiency on the code above",
        ]

        # Summery Question
        messages.append(
            {
                "role": "user",
                "content": f"Summarize this feedback and provide formative feedback report. {file_feedback}",
            }
        )
        summery = self.llm.chat(
            verbose=True,
            messages=messages,
        )

        return summery
