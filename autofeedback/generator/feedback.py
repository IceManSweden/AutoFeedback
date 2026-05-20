from .pipeline import FeedbackPipeline
from autofeedback.generator.llm_handler import LLMManager


class FeedbackGenerator:
    llm = None

    def __init__(self, llmPath="http://localhost:11434", model="qwen3:0.6b"):
        self.llm = LLMManager(llmPath=llmPath, model=model)
        self.llm.startup()

    def single_prompt(self, input=[], dir=".", assignment=None):
        """Runs the single prompt method

        Args:
            input: The input files.
            dir: directory.
            assignment: The assignment related to the code.

        Returns:
            The feedback that has been generated.
        """
        print("Running single prompt")
        if assignment:
            query = f"Provide formative feedback on this code to this assignment {assignment} .Dont provide fixes or solution of any kind. Dont ask any followup questions in the end"
        else:
            query = f"Provide formative feedback on this code. Dont provide fixes or solution of any kind. Dont ask any followup questions in the end"
        return self.llm.generate(
            query=query,
            input=input,
        )

    def pipeline(self, input_files=[], dir=".", assignment=None):
        """Runs the pipeline feedback generation method.
        Args:
            input_files: The input files.
            dir: directory.
            assignment: The assignment related to the code.

        Returns:
            The feedback that has been generated.
        """
        feedbackPipeline = FeedbackPipeline(self.llm)
        return feedbackPipeline.run(input_files, dir, assignment)
