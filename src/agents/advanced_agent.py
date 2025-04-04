from typing import List, Any, Dict, Optional, Union

from pydantic import Field
from langchain.agents import Agent, AgentExecutor, AgentOutputParser
from langchain_core.tools import BaseTool, Tool
from langchain.schema import AgentAction, AgentFinish
from langchain.prompts import BasePromptTemplate, PromptTemplate
from langchain.llms.base import LLM
from langchain_core.runnables import RunnableSequence  # Use RunnableSequence instead of LLMChain
from langchain.chains.llm import LLMChain
from llms.lmstudio_llm import get_llm
from tools import web_search_google, ppt_tool, ref_tool

# A simple custom output parser that expects a plain text answer.
class SimpleOutputParser(AgentOutputParser):
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        # Here we assume the output is the final answer.
        return AgentFinish({"output": text.strip()}, text.strip())

class AdvancedAgent(Agent):
    """
    Custom Agent that inherits from Agent.
    This agent uses a RunnableSequence (prompt | llm) to process user input using a provided prompt template.
    Allowed tools (by name) should match those provided to the executor.
    """
    allowed_tools: Optional[List[str]] = Field(default=None)
    tools: List[Any] = Field(...)
    prompt_template: BasePromptTemplate = Field(...)
    verbose: bool = Field(default=False)
    output_parser: AgentOutputParser = Field(default_factory=SimpleOutputParser)
    # Replace LLMChain with a RunnableSequence
    runnable_chain: RunnableSequence = Field(...) # This is forward compatible for future use case
    llm_chain: LLMChain = Field(default=None)
    # The LLMChain is now a part of the RunnableSequence, so we don't need it separately. But for the sake of compatibilty we have to keep it

    def __init__(
        self,
        llm: LLM,
        tools: List[Tool],
        prompt_template: BasePromptTemplate,
        verbose: bool = False,
        allowed_tools: Optional[List[str]] = None,
        **kwargs: Any
    ):
        runnable_chain = prompt_template | llm
        llm_chain = LLMChain(llm=llm, prompt=prompt_template)
        # Call Agent's __init__ as a Pydantic model.
        super().__init__(
            tools=tools,               # type: ignore
            prompt_template=prompt_template,  # type: ignore
            verbose=verbose,           # type: ignore
            allowed_tools=allowed_tools,  # type: ignore
            llm_chain = llm_chain, #type: ignore
            runnable_chain = runnable_chain, # type: ignore
            **kwargs
        )
        # Use the RunnableSequence pattern: combine the prompt and LLM.
        # This is equivalent to: chain = prompt_template | llm


    @property
    def input_keys(self) -> List[str]:
        return ["input"]

    @property
    def output_keys(self) -> List[str]:
        return ["output"]

    @property
    def observation_prefix(self) -> str:
        return "Observation:"

    @property
    def llm_prefix(self) -> str:
        return ""

    @classmethod
    def _get_default_output_parser(cls, **kwargs: Any) -> AgentOutputParser:
        return SimpleOutputParser()

    @classmethod
    def create_prompt(cls, tools: Any) -> BasePromptTemplate:
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
        Create a plan by appending the user query to the base prompt.
        """
        user_input = kwargs.get("input", "")
        # Construct the full prompt using our prompt template.
        base_prompt = self.create_prompt(self.tools).format()
        full_prompt = f"{base_prompt}\nUser Query: {user_input}"
        if self.verbose:
            print("AdvancedAgent plan prompt:", full_prompt)
        # Invoke the chain using the user input.
        llm_output = self.llm_chain.invoke(user_input)
        if self.verbose:
            print("LLM raw output:", llm_output)
        # Extract the string output from llm_output.
        if isinstance(llm_output, dict):
            if "output" in llm_output:
                llm_output_text = llm_output["output"]
            elif "text" in llm_output:
                llm_output_text = llm_output["text"]
            else:
                raise ValueError("LLM output is not in the expected format.")
        else:
            llm_output_text = llm_output
        return self.output_parser.parse(llm_output_text)

    def format_return_values(self, finish: AgentFinish) -> Dict[str, Any]:
        return {"output": finish.return_values.get("output", "")}

    @classmethod
    def create_executor(
        cls,
        llm: LLM,
        tools: List[Any],
        prompt_template: BasePromptTemplate,
        verbose: bool = False,
    ) -> AgentExecutor:
        agent = cls(llm=llm, tools=tools, prompt_template=prompt_template, verbose=verbose)
        return AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=verbose)

if __name__ == "__main__":
    model = get_llm()
    if not model:
        raise ValueError("No LLM provided. Please check your model initialization.")

    # Create a prompt template (for demonstration, input variable 'agent_scratchpad' is provided)
    prompt_template = PromptTemplate(
        input_variables=["agent_scratchpad"],
        template="You are a very advanced agent that integrates web search and presentation tools.\n\n{agent_scratchpad}"
    )

    accessible_tools = [web_search_google, ppt_tool, ref_tool]

    agent = AdvancedAgent(
        llm=model,
        tools=accessible_tools,
        prompt_template=prompt_template,
        verbose=True,
        allowed_tools=["google_search", "create_ppt", "add_references"]
    )
    # Create an AgentExecutor with return_intermediate_steps enabled.
    executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=agent.tools,
        verbose=agent.verbose,
        return_intermediate_steps=True,
    )
    query = "Generate a presentation on latest tech innovations with references."
    # Use invoke() to support multiple outputs (i.e. including intermediate_steps)
    response = executor.invoke({"input": query})
    print("Agent Response:")
    print(response)
