"""MCP Server for OpenAI DeepResearch integration.

This module implements the main MCP server that exposes OpenAI's DeepResearch 
capabilities as a callable tool for agentic systems.
"""

import os
import sys
import logging
from typing import Optional, Any, Dict
import asyncio

from mcp.server.fastmcp import FastMCP
from mcp.server.session import ServerSession
from mcp.server.fastmcp import Context
from mcp.shared.exceptions import McpError
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

# Configure logging to stderr (MCP requirement)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("mcp-deepresearch")

# Initialize FastMCP server
app = FastMCP(name="OpenAI DeepResearch Server")

class DeepResearchConfig:
    """Configuration for DeepResearch integration."""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("DEEPRESEARCH_MODEL", "o3-deep-research-2025-06-26")
        
        if not self.openai_api_key:
            logger.error("OPENAI_API_KEY environment variable not set")
            raise McpError("OPENAI_API_KEY environment variable is required")

# Global configuration
config = DeepResearchConfig()

# Initialize OpenAI client
openai_client = AsyncOpenAI(api_key=config.openai_api_key)

def _build_system_message(
    context: Optional[str], 
    research_depth: Optional[str],
    domain_restrictions: Optional[str],
    output_format: Optional[str]
) -> str:
    """Build the system message for DeepResearch based on parameters."""
    
    base_message = (
        "You are a comprehensive research assistant powered by OpenAI's DeepResearch. "
        "Your task is to conduct thorough, multi-step research on the given topic, "
        "synthesizing information from web sources and providing citation-rich reports."
    )
    
    instructions = []
    
    if context:
        instructions.append(f"Research context: {context}")
    
    if research_depth:
        instructions.append(f"Research depth requirement: {research_depth}")
    
    if domain_restrictions:
        instructions.append(f"Domain restrictions: {domain_restrictions}")
    
    if output_format:
        instructions.append(f"Output format preference: {output_format}")
    else:
        instructions.append("Output format: Provide a comprehensive research report with clear citations")
    
    if instructions:
        base_message += "\n\nSpecific instructions:\n" + "\n".join(f"- {inst}" for inst in instructions)
    
    base_message += (
        "\n\nEnsure your research includes:\n"
        "- Multiple reliable sources\n"
        "- Proper citations and source links\n"
        "- Comprehensive analysis and synthesis\n"
        "- Clear, well-structured output"
    )
    
    return base_message

@app.tool()
async def deep_research(
    query: str,
    context: Optional[str] = None,
    research_depth: Optional[str] = None,
    domain_restrictions: Optional[str] = None,
    output_format: Optional[str] = None,
    ctx: Optional[Context[ServerSession, None]] = None
) -> str:
    """Conduct comprehensive research using OpenAI's DeepResearch API.
    
    This tool leverages OpenAI's DeepResearch capabilities to perform multi-step 
    research, web searching, and information synthesis on complex topics.
    
    Args:
        query: The detailed research question or topic (required)
        context: Background context about the research query (optional)
        research_depth: Research thoroughness level - e.g., "comprehensive", 
                       "focused", "surface-level" (optional)
        domain_restrictions: Domain limitations - e.g., "academic sources only", 
                           "recent news articles", "technical documentation" (optional)
        output_format: Preferred output structure - e.g., "detailed report", 
                      "executive summary", "bullet points", "technical analysis" (optional)
    
    Returns:
        Comprehensive research report with citations and structured analysis
        
    Raises:
        McpError: For API errors, authentication issues, or other failures
    """
    
    if ctx:
        await ctx.info(f"Starting DeepResearch for query: {query[:100]}...")
    
    try:
        # Build the system message with parameters
        system_message = _build_system_message(
            context, research_depth, domain_restrictions, output_format
        )
        
        if ctx:
            await ctx.debug(f"Using model: {config.model}")
            await ctx.debug("Sending request to OpenAI DeepResearch API...")
        
        # Make the DeepResearch API call
        response: ChatCompletion = await openai_client.chat.completions.create(
            model=config.model,
            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user", 
                    "content": query
                }
            ],
            # Enable web search and reasoning capabilities
            tools=[
                {"type": "web_search_preview"}
            ],
            # Request structured reasoning summary
            # Note: This may vary based on OpenAI's current API structure
            temperature=0.1,  # Lower temperature for more focused research
            max_tokens=4000,  # Allow for comprehensive responses
        )
        
        if ctx:
            await ctx.info("Research completed successfully")
        
        # Extract and return the research content
        if response.choices and response.choices[0].message.content:
            research_result = response.choices[0].message.content
            
            if ctx:
                await ctx.debug(f"Research result length: {len(research_result)} characters")
            
            return research_result
        else:
            error_msg = "No research content returned from DeepResearch API"
            logger.error(error_msg)
            raise McpError(error_msg)
    
    except Exception as e:
        error_msg = f"DeepResearch API error: {str(e)}"
        logger.error(error_msg)
        
        if ctx:
            await ctx.info(f"Research failed: {str(e)}")
        
        # Re-raise as MCP error for proper client handling
        raise McpError(error_msg)

def main():
    """Main entry point for the MCP server."""
    
    logger.info("Starting MCP OpenAI DeepResearch Server")
    logger.info(f"Using model: {config.model}")
    
    try:
        # Run the server with STDIO transport (default for MCP)
        app.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()