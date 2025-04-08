

from tools.langchain_tool_state_manager import ToolStateContext
from tools.declarations import *
from tools.implementation import GOOGLE_IMAGE_STATES, GOOGLE_SEARCH_STATES

tools = [
    google_web_search_tool,
    google_search_images_tool
]

state1 = [
    GOOGLE_SEARCH_STATES["alternative_1"],
    GOOGLE_IMAGE_STATES["alternative_1"],
]

state2 = [
    GOOGLE_SEARCH_STATES["alternative_2"],
    GOOGLE_IMAGE_STATES["alternative_2"],
]

current_state1 = list(zip(tools, state1))
current_state2 = list(zip(tools, state2))

with ToolStateContext(*current_state1):
    result = google_web_search_tool.run("latest news")	
    print(result)
    print("Total Results: ", len(result))

print("-----------------")	
with ToolStateContext(*current_state2):
    result = google_web_search_tool.run("latest news")	
    print(result)
    print("Total Results: ", len(result))
print("-----------------")	

result = google_web_search_tool.run("latest news")
print(result)
print("Total Results: ", len(result))