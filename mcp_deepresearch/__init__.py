"""MCP Server for OpenAI DeepResearch integration.

This package provides a Model Context Protocol (MCP) server that integrates 
OpenAI's DeepResearch API, enabling agentic systems to perform comprehensive 
research tasks with structured outputs and citations.
"""

__version__ = "1.0.0"
__author__ = "Arthur Calvi"

from .server import app

__all__ = ["app"]