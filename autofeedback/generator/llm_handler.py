import atexit
from ollama import Client
from autofeedback.generator.feedbacktools import eslint_tool


class LLMManager:
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

    def list_installed_models(self):
        print(self.llm.list().models)

    def pullChosenModel(self):
        print(self.llm.pull(self.model))

    def show_model(self):
        print(self.llm.show(self.model))

    def create_metadata(self, res):
        return (
            "\n\n\n\n Metadata: "
            f"Model: {res.model} | "
            f"Eval duration: {res.eval_duration} | "
            f"Done reason: {res.done_reason} | "
            f"Load duration: {res.load_duration} | "
            f"Created at: {res.created_at} | "
            f"Prompt eval count: {res.prompt_eval_count} | "
            f"Prompt eval duration: {res.prompt_eval_duration}"
        )

    def chat(self, query, input=[], verbose=False, tool=False, messages=[]):
        data = ""
        for d in input:
            data += d
        messages.extend(
            [
                {"role": "TA", "content": "You provide constructive feedback on code"},
                {"role": "user", "content": f"{query} {data}"},
            ]
        )
        print(f"{query}")
        res = self.llm.chat(
            model=self.model,
            stream=False,
            think=False,
            messages=messages,
            tools=[eslint_tool.run_eslint],
        )

        # Gets the meta data from the query.
        metadata = self.create_metadata(res=res)

        if verbose:
            return res.message.content, metadata
        if tool:
            return res
        else:
            return res.message.content

    def exit(self):
        self.llm.generate(model=self.model, prompt="", keep_alive=0)
