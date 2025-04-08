
# This is a temporary provision here

from langchain.tools import Tool
import wikipedia
from functools import partial

from tools.implementation.web_tools import *

google_web_search_tool = Tool(
    name = "google_search_web",
    description="Search Google for recent results. Use this tool to find the latest information on a topic.",
    func=google_search_web(),
    return_direct=True
)

youtube_search_tool = Tool(
    name = "youtube_search",
    description="Search YouTube for videos. Use this tool to find videos related to a topic.",
    func=youtube_search(),
    return_direct=True
)

wikipedia_search_tool = Tool(
    name = "wikipedia_search",
    description="Search Wikipedia for a summary of a topic. Use this tool to get a brief overview of a subject.",
    func=wikipedia_search(),
    return_direct=True
)
google_search_images_tool = Tool(
    name = "google_image_search",
    description="Search Google for images. Use this tool to find images related to a topic.",
    func=google_image_search(),
    return_direct=True
)

youtube_search_tool = Tool(
    name = "youtube_search",
    description="Search YouTube for videos. Use this tool to find videos related to a topic.",
    func=youtube_search(),
    return_direct=True
)