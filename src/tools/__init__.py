"""
Agentic Framework Tools Package
---------------------------------

This package consolidates utility functions into a single namespace by
dynamically importing all functions and methods from the modules and sub-packages
in this directory, and exposing them as tools.

Implemented by: Sheshank Joshi
Version: 1.0.0
Last Modified: 2025-04-03
"""

from .basic_tools import *


# Iterate over all modules and sub-packages in the current directory


# # Iterate over all modules and sub-packages in the current directory
# for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
#     full_module_name = f"{__name__}.{module_name}"
#     module = importlib.import_module(full_module_name)

#     # Iterate over members and import only functions/methods
#     for name, obj in inspect.getmembers(module):
#         if inspect.isfunction(obj) or inspect.ismethod(obj):
#             globals()[name] = obj

