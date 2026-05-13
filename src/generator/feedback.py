from ollama import chat, ChatResponse, Client
import atexit
from pydantic import BaseModel
from .feedbacktools.eslintTool import run_eslint


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

    def createMetadata(self, res):
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
            tools=[run_eslint],
        )

        # Gets the meta data from the query.
        metadata = self.createMetadata(res=res)

        if verbose:
            return res.message.content, metadata
        if tool:
            return res
        else:
            return res.message.content

    def singlePrompt(self, input=[], dir="."):
        print("Running single prompt")
        return self.chat(
            query="Provide formative feedback on this code. Dont provide fixes or solution of any kind. Dont ask any followup questions in the end",
            input=input,
            verbose=True,
        )

    def pipeline(self, inputFiles=[], dir="."):
        responses = []

        eslintres = self.chat(
            query=f"Get the result from running eslint and evaluate it in the path ${dir}",
            tool=True,
        )
        messages = []

        print(eslintres.message.content)
        if eslintres.message.tool_calls:
            for call in eslintres.message.tool_calls:
                if call.function.name == "run_eslint":
                    result = run_eslint(**call.function.arguments)

                    messages.append(
                        {
                            "role": "tool",
                            "tool_name": call.function.name,
                            "content": str(result),
                        }
                    )

        print(messages)

        questions = [
            "Provide direct feedback on only the Syntax in this code. In less then 200 words",
            "Provide direct feedback on only the structure of this code.In less then 200 words",
            "Provide direct feedback on only the Correctness of this code.In less then 200 words",
            "Provide direct feedback on only the Efficiency of this code.In less then 200 words",
        ]

        print("\n\nRunning Pipeline:")
        for q in questions:
            responses.append(self.chat(query=q, input=inputFiles, messages=messages))

        responses.extend(inputFiles)
        summery = self.chat(
            query="Only Summarize this feedback and provide formative feedback. Dont provide fixes or improvements or refactored code. Dont ask any followup questions in the end",
            input=responses,
            verbose=True,
        )
        return summery

    def exit(self):
        self.llm.generate(model=self.model, prompt="", keep_alive=0)
