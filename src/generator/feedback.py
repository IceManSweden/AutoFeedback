from ollama import chat, ChatResponse, Client
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

    def listInstalledModels(self):
        print(self.llm.list().models)

    def pullChosenModel(self):
        print(self.llm.pull(self.model))

    def showModel(self):
        print(self.llm.show(self.model))

    def chat(self, query):
        res = self.llm.chat(
            model=self.model,
            stream=False,
            messages=[{"role": "user", "content": f"{query}"}],
        )
        print(res.message.content)
