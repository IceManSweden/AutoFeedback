import atexit
from ollama import Client
from autofeedback.generator.feedbacktools import eslint_tool


class LLMManager:
    def __init__(self, llmPath="http://localhost:11434", model="qwen3:0.6b"):
        """LLMManager constructor.
        Args:
            llmPath: The path to the ollama instance, default local.
            model: The model that is going to be used.
        """
        self.path = llmPath
        self.llm = Client(host=llmPath)
        self.model = model
        self.startup()
        # Sets up auto shutdown upon exit.
        atexit.register(self.exit)

    def startup(self):
        """Starts the model to be used. If the model is not found it will try to download the model."""
        print(f"Loading model {self.model}")
        try:
            self.llm.generate(model=self.model, prompt="", keep_alive=5)
        except:
            self.pullChosenModel()
        print("Model Loaded")

    def list_installed_models(self):
        """Lists the installed models on ollama instance."""
        print(self.llm.list().models)

    def pullChosenModel(self):
        """Downloads the chosen model."""
        print("Downloading Model")
        print(self.llm.pull(self.model))

    def show_model(self):
        """Shows the selected model information"""
        print(self.llm.show(self.model))

    def create_metadata(self, res):
        """Crates a metadata string for a llm response.
        Args:
            res: The response object.
        Returns:
            A formatted string containing relevant metadata.
        """
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

    def generate(self, query, input=[]):
        """Generates a single query with the llm

        Args:
            query: The question to be asked.
            input: Any additional data to be used.

        Returns:
            The LLM response message and the metadata generated with the response.
        """
        data = ""
        for d in input:
            data += d

        res = self.llm.chat(
            model=self.model,
            stream=False,
            think=False,
            messages=[{"role": "user", "content": f"{query} {data}"}],
            tools=[eslint_tool.run_eslint],
        )

        metadata = self.create_metadata(res=res)
        return res.message.content, metadata

    def chat(
        self,
        verbose: bool = False,
        tool: bool = False,
        messages=[],
    ):

        # Add new query.
        """Uses the LLM to chat.
        Args:
            verbose: Enables different output mode.
            tool:  Enables different output mode.
            messages: The messages sent and will be sent.
        """
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
        """Unloads the model from the ollama instance."""
        self.llm.generate(model=self.model, prompt="", keep_alive=0)
