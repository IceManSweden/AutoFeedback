from autofeedback.generator.feedbacktools.eslint_tool import run_eslint
from autofeedback.generator.llm_handler import LLMManager


class FeedbackPipeline:
    def __init__(self, llm: LLMManager):
        self.llm = llm

    def run(self, inputFiles=[], dir="."):
        responses = []

        toolResult = self.llm.chat(
            query=f"Get the result from running eslint and evaluate it in the path ${dir}",
            tool=True,
        )
        messages = []

        print(toolResult.message.content)
        if toolResult.message.tool_calls:
            for call in toolResult.message.tool_calls:
                if call.function.name == "run_eslint":
                    result = run_eslint(**call.function.arguments)

                    messages.append(
                        {
                            "role": "tool",
                            "tool_name": call.function.name,
                            "content": str(result),
                        }
                    )

        print(f"Result of running eslint {messages}")

        """
        questions = [
            "Provide direct feedback on only the Syntax in this code. In less then 200 words",
            "Provide direct feedback on only the structure of this code.In less then 200 words",
            "Provide direct feedback on only the Correctness of this code.In less then 200 words",
            "Provide direct feedback on only the Efficiency of this code.In less then 200 words",
        ]

        print("\n\nRunning Pipeline:")
        for q in questions:
            responses.append(self.chat(query=q, input=inputFiles, messages=messages))
        """

        responses.extend(inputFiles)
        summery = self.llm.chat(
            query="Only Summarize this feedback and provide formative feedback. Dont provide fixes or improvements or refactored code. Dont ask any followup questions in the end",
            input=responses,
            verbose=True,
        )
        return summery
