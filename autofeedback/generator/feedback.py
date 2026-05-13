from .pipeline import FeedbackPipeline
from autofeedback.generator.llm_handler import LLMManager


class FeedbackGenerator:
    llm = None

    def __init__(self, llmPath="http://localhost:11434", model="qwen3:0.6b"):
        self.llm = LLMManager(llmPath=llmPath, model=model)
        self.llm.startup()

    def single_prompt(self, input=[], dir="."):
        print("Running single prompt")
        return self.llm.generate(
            query="Provide formative feedback on this code. Dont provide fixes or solution of any kind. Dont ask any followup questions in the end",
            input=input,
        )

    def pipeline(self, inputFiles=[], dir="."):
        feedbackPipeline = FeedbackPipeline(self.llm)
        return feedbackPipeline.run(inputFiles, dir)
