from typing import List, Any, Dict, Optional, Union

from litellm import allowed_fails
from pydantic import Field
from langchain.agents.agent import Agent, AgentExecutor, AgentOutputParser
from langchain.schema import AgentAction, AgentFinish
from langchain.prompts import BasePromptTemplate, PromptTemplate
from langchain.chains import LLMChain
from langchain.llms.base import LLM
from llms.lmstudio_llm import get_llm
from tools import web_search_google, ppt_tool, ref_tool

# A simple custom output parser that expects a plain text answer.
class SimpleOutputParser(AgentOutputParser):
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        # In a real implementation you may parse tool instructions, parameters, etc.
        # Here we assume the output is the final answer.
        return AgentFinish({"output": text.strip()}, text.strip())

class AdvancedAgent(Agent):
    """
    Custom Agent that inherits from Agent.
    This agent uses an LLMChain to process user input using a provided prompt template.
    Allowed tools (by name) should match those provided to the executor.
    """
    # Define allowed tool names.
    allowed_tools: Optional[List[str]] = Field(default_factory=lambda: ["google_search", "create_ppt", "add_references"])
    # Declare additional attributes as Pydantic fields.
    tools: List[Any] = Field(...)
    prompt_template: BasePromptTemplate = Field(...)
    verbose: bool = Field(default=False)
    output_parser: AgentOutputParser = Field(default_factory=SimpleOutputParser)
    llm_chain: LLMChain = Field(...)

    def __init__(
        self,
        llm: LLM,
        tools: List[Any],
        prompt_template: BasePromptTemplate,
        verbose: bool = False,
        **kwargs: Any
    ):
        # Call Agent's __init__ to allow proper initialization of a Pydantic model.
        chain = LLMChain(llm=llm, prompt=prompt_template)
        super().__init__(
            tools=tools, #type: ignore
            prompt_template=prompt_template, #type: ignore
            verbose=verbose, #type: ignore
            llm_chain=chain,
            **kwargs)

    @property
    def input_keys(self) -> List[str]:
        # The agent expects a single "input" key.
        return ["input"]

    @property
    def output_keys(self) -> List[str]:
        # The agent produces a single "output" key.
        return ["output"]

    @property
    def observation_prefix(self) -> str:
        # Define an observation prefix.
        return "Observation:"

    @property
    def llm_prefix(self) -> str:
        # No special LLM prefix used.
        return ""

    @classmethod
    def _get_default_output_parser(cls, **kwargs: Any) -> AgentOutputParser:
        # Return our default output parser.
        return SimpleOutputParser()

    @classmethod
    def create_prompt(cls, tools: Any) -> BasePromptTemplate:
        """
        Create a prompt template for this agent.
        As a simple example, we ignore the tools parameter.
        """
        return PromptTemplate(
            input_variables=[],
            template="You are a very advanced agent that integrates web search and presentation tools."
        )

    def plan(
        self,
        intermediate_steps: List[tuple[AgentAction, str]],
        callbacks: Optional[Any] = None,
        **kwargs: Any
    ) -> Union[AgentAction, AgentFinish]:
        """
        Create a plan using the LLMChain.
        This simple implementation appends the user query to the base prompt.
        """
        user_input = kwargs.get("input", "")
        # Construct the full prompt using our prompt template.
        base_prompt = self.create_prompt(self.tools).format()
        full_prompt = f"{base_prompt}\nUser Query: {user_input}"
        if self.verbose:
            print("AdvancedAgent plan prompt:", full_prompt)
        # Invoke the LLMChain; here we feed just the user input.
        llm_output = self.llm_chain.run(user_input)
        if self.verbose:
            print("LLM raw output:", llm_output)
        # Parse the LLM output.
        return self.output_parser.parse(llm_output)

    def format_return_values(self, finish: AgentFinish) -> Dict[str, Any]:
        """
        Format the final output into a dict.
        """
        return {"output": finish.return_values.get("output", "")}

    @classmethod
    def create_executor(
        cls,
        llm: LLM,
        tools: List[Any],
        prompt_template: BasePromptTemplate,
        verbose: bool = False,
    ) -> AgentExecutor:
        """
        Convenience method to create an AgentExecutor for this agent.
        """
        agent = cls(llm=llm, tools=tools, prompt_template=prompt_template, verbose=verbose)
        return AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=verbose)

if __name__ == "__main__":
    # Initialize the model (ensure get_llm returns a valid LLM instance)
    model = get_llm()
    if not model:
        raise ValueError("No LLM provided. Please check your model initialization.")

    # Create a prompt template (for demonstration, no input variables are specified)
    prompt_template = PromptTemplate(
        input_variables=[],
        template="You are a very advanced agent that integrates web search and presentation tools."
    )

    # Define the list of tools for the agent. The actual tools for the agent, is the spur of the moment i.e. tools
    tools = [web_search_google, ppt_tool, ref_tool]

    agent = AdvancedAgent(
        llm=model,
        tools=tools,
        prompt_template=prompt_template,
        verbose=True,
        allowed_tools = ["google_search", "create_ppt"] # NOTE: This is a list of allowed tools for the agent, through which you control which tools for each instance
    )
    # Create an AgentExecutor from the custom AdvancedAgent.
    executor = AdvancedAgent.create_executor(
        llm=model,
        tools=tools,
        prompt_template=prompt_template,
        verbose=True,
        allowed_tools = ["google_search", "create_ppt"]]
    )

    # Use the executor to process a sample query.
    query = "Generate a presentation on latest tech innovations with references."
    response = executor.run({"input": query})
    print("Agent Response:")
    print(response)
