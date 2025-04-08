from tools.state_manager import StateContext
class ToolStateContext:
    """
    A context manager to manage temporary state for LangChain Tools that wrap stateful functions.
    
    It converts (Tool, state_dict) pairs into (Tool.func, state_dict), assuming Tool.func has a temp_state context manager.
    """
    def __init__(self, *tool_state_pairs):
        # Adapt tools into (func, state_dict)
        self._state_ctx = StateContext(
            *((tool.func, state_dict) for tool, state_dict in tool_state_pairs)
        )

    def __enter__(self):
        return self._state_ctx.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._state_ctx.__exit__(exc_type, exc_val, exc_tb)

if __name__ == "__main__":
    import sys
    from pprint import pprint
    pprint(sys.path)
    print()
    import os
    pprint(os.environ["PYTHONPATH"])
    
    # from tools.langchain_tool_state_manager import ToolStateContext
    # from tools.declarations import web_tools