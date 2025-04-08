from functools import partial
from typing import Optional
from tools.state_manager import stateful_function

@stateful_function
def google_search_web(num_results=5):
    from langchain_google_community import GoogleSearchAPIWrapper
    """
    Searches Google for recent results and returns a callable function that performs the search.

    Parameters:
        num_results (int): The number of search results to retrieve. Must be a positive integer.

    Returns:
        callable: A function that when executed returns search results from Google.

    Raises:
        TypeError: If 'num_results' is not an integer.
        ValueError: If 'num_results' is not a positive integer.
    """
    if not isinstance(num_results, int):
        raise TypeError("num_results must be an integer")
    if num_results <= 0:
        raise ValueError("num_results must be a positive integer")

    search = GoogleSearchAPIWrapper()
    def do_search(query: str):
        """
        Perform a Google search with the given query and return the results.

        Parameters:
            query (str): The search query.

        Returns:
            list: A list of search results.
        """
        return search.results(query, num_results=num_results)
    return do_search

@stateful_function
def wikipedia_search():
    """
    Returns a callable function that searches Wikipedia for a summary of a query.

    Returns:
        callable: A function that when executed with a search query returns 
                  a summary from Wikipedia or an error message.
    """
    import wikipedia

    def search(query: str):
        try:
            summary = wikipedia.summary(query)
            return summary
        except Exception as e:
            return f"Error retrieving Wikipedia summary: {e}"

    return search

@stateful_function
def google_image_search(num_results=5, file_type: Optional[str] = None, img_size: Optional[str] = None, img_type: Optional[str] = None, img_color_type: Optional[str] = None, img_dominant_color: Optional[str] = None):
    """
    Returns a callable function that performs a Google Image search with additional filter parameters.

    Parameters:
        num_results (int): The number of image results to retrieve.
        file_type (str, optional): Filter by file extension (e.g., "jpg", "png").
        img_size (str, optional): Specify image size (e.g., "large", "xlarge").
        img_type (str, optional): Filter by image type (e.g., "photo", "clipart").
        img_color_type (str, optional): Filter by image color type (e.g., "color", "gray").
        img_dominant_color (str, optional): Filter by dominant image color (e.g., "red", "blue").
        
    Returns:
        callable: A function that when executed with a query returns image search results.
    """
    if not isinstance(num_results, int):
        raise TypeError("num_results must be an integer")
    if num_results <= 0:
        raise ValueError("num_results must be a positive integer")

    from langchain_google_community import GoogleSearchAPIWrapper
    # Build search parameters including the additional filters.
    
    search_params = {
        "searchType": "image",
    }
    if file_type:
        search_params["fileType"] = file_type
    if img_size:
        search_params["imgSize"] = img_size
    if img_type:
        search_params["imgType"] = img_type
    if img_color_type:
        search_params["imgColorType"] = img_color_type
    if img_dominant_color:
        search_params["imgDominantColor"] = img_dominant_color

    search = GoogleSearchAPIWrapper()
    def search_images(query: str):
        return search.results(query, num_results, search_params=search_params)
    return search_images

@stateful_function
def yahoo_finance():
    """
    Returns a callable function that retrieves financial information for a given ticker symbol from Yahoo Finance.

    Returns:
        callable: A function that when executed with a ticker symbol returns financial data.
    """
    import yfinance as yf

    def get_finance_info(ticker: str):
        try:
            data = yf.Ticker(ticker).info
            return data
        except Exception as e:
            return f"Error retrieving financial data for '{ticker}': {e}"

    return get_finance_info

# @stateful_function
# def youtube_search(num_results=5):
#     """
#     Returns a callable function that performs a YouTube search and returns video results.

#     Parameters:
#         num_results (int): The number of search results to retrieve. Must be a positive integer.

#     Returns:
#         callable: A function that when executed with a search query returns YouTube search results.
#     """
#     if not isinstance(num_results, int):
#         raise TypeError("num_results must be an integer")
#     if num_results <= 0:
#         raise ValueError("num_results must be a positive integer")
    
#     from youtube_search2 import YoutubeSearch
#     def search(query: str):
#         try:
#             results = YoutubeSearch(query, max_results=num_results).to_dict()
#             return results
#         except Exception as e:
#             return f"Error retrieving YouTube results: {e}"

#     return search

@stateful_function
def youtube_search(num_result=5):
    return lambda x : print (f"Searching YouTube for {x} with {num_result} results")


# -----------------------------------------------------------------------------
# Example State Configurations for Tools
# -----------------------------------------------------------------------------
#
# These dictionaries represent different state settings for the tools.
# For tools that support state management (e.g., when wrapped using a stateful
# decorator), these states can be applied via a context manager.
#
# GOOGLE_SEARCH_STATES: States for the google_search_web tool.
#   - "default": The standard configuration.
#   - "alternative_1": An alternative configuration with a custom API key and proxy.
#   - "alternative_2": Another configuration variant.
#
# GOOGLE_IMAGE_STATES: States for the google_image_search tool.
#   - "default": The standard configuration for image search.
#   - "alternative_1": A configuration with custom file type and image size filters.
#   - "alternative_2": A configuration with additional image type and color filters.
#
GOOGLE_SEARCH_STATES = {
    "default": {"api_key": "DEFAULT_GOOGLE_API_KEY", "proxy": None},
    "alternative_1": {"num_results": 10},
    "alternative_2": {"num_results":7},
}

GOOGLE_IMAGE_STATES = {
    "default": {
        "num_results": 10,
        "file_type": "jpg",
        "img_size": "large",
        "img_type": None,
        "img_color_type": None,
        "img_dominant_color": None,
    },
    "alternative_1": {
        "num_results": 12,
        "file_type": "png",
        "img_size": "xlarge",
        "img_type": "photo",
        "img_color_type": None,
        "img_dominant_color": None,
    },
    "alternative_2": {
        "num_results": 20,
        "file_type": "gif",
        "img_size": "medium",
        "img_type": None,
        "img_color_type": "color",
        "img_dominant_color": "blue",
    },
}

