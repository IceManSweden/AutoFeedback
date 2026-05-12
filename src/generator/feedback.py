from ollama import chat, ChatResponse, Client
import atexit
from pydantic import BaseModel


class FeedbackGenerator:
    llm = None
    path = ""
    model = ""
    pipeline = []

    def __init__(self, llmPath="http://localhost:11434", model="qwen3:0.6b"):
        self.path = llmPath
        self.llm = Client(host=llmPath)
        self.model = model
        self.startup()
        atexit.register(self.exit)

    def startup(self):
        print(f"Loading model {self.model}")
        self.llm.generate(model=self.model, prompt="", keep_alive=5)
        print("Model Loaded")

    def listInstalledModels(self):
        print(self.llm.list().models)

    def pullChosenModel(self):
        print(self.llm.pull(self.model))

    def showModel(self):
        print(self.llm.show(self.model))

    def chat(self, query, input=[], verbose=False):
        data = ""
        for d in input:
            data += d

        print(f"{query}")
        res = self.llm.chat(
            model=self.model,
            stream=False,
            think=False,
            messages=[{"role": "user", "content": f"{query} {data}"}],
        )
        summary = (
            "\n\n\n\n Metadata: "
            f"Model: {res.model} | "
            f"Eval duration: {res.eval_duration} | "
            f"Done reason: {res.done_reason} | "
            f"Load duration: {res.load_duration} | "
            f"Created at: {res.created_at} | "
            f"Prompt eval count: {res.prompt_eval_count} | "
            f"Prompt eval duration: {res.prompt_eval_duration}"
        )
        if verbose:
            return res.message.content, summary
        else:
            return res.message.content

    def singlePrompt(self, input=[]):
        print("Running single prompt")
        return self.chat(
            query="Provide feedback on this code.. Dont provide fixes",
            input=input,
            verbose=True,
        )

    def pipeline(self, inputFiles=[]):
        responses = []
        questions = [
            "Provide feedback on the syntax in this code.",
            "Provide feedback on the structure of this code.",
            "Provide feedback on the Correctness of this code.",
            "Provide feedback on the Efficiency of this code.",
        ]
        print("\n\nRunning Pipeline:")
        for q in questions:
            responses.append(self.chat(query=q, input=inputFiles))

        responses.extend(inputFiles)
        summery = self.chat(
            query="Summarize this feedback and provide formative feedback. Dont provide fixes or improvements",
            input=responses,
            verbose=True,
        )
        return summery

    def exit(self):
        self.llm.generate(model=self.model, prompt="", keep_alive=0)
