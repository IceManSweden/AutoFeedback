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
        print("Loading model")
        self.llm.generate(model=self.model, prompt="", keep_alive=5)
        print("Model Loaded")

    def listInstalledModels(self):
        print(self.llm.list().models)

    def pullChosenModel(self):
        print(self.llm.pull(self.model))

    def showModel(self):
        print(self.llm.show(self.model))

    def chat(self, query, input=[]):
        data = ""
        for d in input:
            data += d

        print(f"{query}")
        res = self.llm.chat(
            model=self.model,
            stream=False,
            messages=[{"role": "user", "content": f"{query} {data}"}],
        )
        return res.message.content

    def singlePrompt(self, input=[]):
        return self.chat(
            query="Provide feedback on this code. Dont be to harsh. Dont provide fixes",
            input=input,
        )

    def pipeline(self, inputFiles=[]):
        responses = []
        questions = [
            "Provide feedback on the syntax in this code. Dont be to harsh",
            "Provide feedback on the structure of this code. Dont be to harsh",
            "Provide feedback on the Correctness of this code. Dont be to harsh",
            "Provide feedback on the Efficiency of this code. Dont be to harsh",
        ]
        for q in questions:
            responses.append(self.chat(query=q, input=inputFiles))

        summery = self.chat(
            query="Summarize this feedback. Dont provide fixes", input=responses
        )
        return summery

    def exit(self):
        self.llm.generate(model=self.model, prompt="", keep_alive=0)
