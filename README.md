# MCP OpenAI DeepResearch Server

A Model Context Protocol (MCP) server that integrates OpenAI's DeepResearch API, enabling agentic systems like Claude Code and Codex to perform comprehensive research tasks efficiently.

## Features

- 🔍 **Comprehensive Research**: Leverages OpenAI's DeepResearch models for multi-step research
- 🌐 **Web Integration**: Automatically searches and synthesizes information from web sources  
- 📖 **Citation-Rich**: Returns structured reports with proper citations and source links
- ⚙️ **Flexible Parameters**: Configurable research depth, domain restrictions, and output formats
- 🛡️ **Error Handling**: Robust error management following MCP best practices
- 🔄 **Async Support**: Non-blocking operations for better performance

## Requirements

- Python 3.10 or higher
- OpenAI API key with access to DeepResearch models
- Internet connectivity for web research

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MCP-OpenAI-DeepResearch-.git
cd MCP-OpenAI-DeepResearch-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install in development mode:
```bash
pip install -e ".[dev]"
```

## Configuration

### Environment Variables

Set the following environment variables:

```bash
# Required: Your OpenAI API key
export OPENAI_API_KEY="sk-your-openai-api-key-here"

# Optional: Choose DeepResearch model (default: o3-deep-research-2025-06-26)  
export DEEPRESEARCH_MODEL="o3-deep-research-2025-06-26"
# Alternative: export DEEPRESEARCH_MODEL="o4-mini-deep-research-2025-06-26"
```

### Adding to Claude Code

Claude Code provides several ways to add MCP servers. Choose the method that best fits your workflow:

#### Method 1: Using Claude Code CLI (Recommended)

```bash
# Add the server with environment variables
claude mcp add deep-research \
  --env OPENAI_API_KEY="sk-your-openai-api-key-here" \
  --env DEEPRESEARCH_MODEL="o3-deep-research-2025-06-26" \
  -- python -m mcp_deepresearch
```

#### Method 2: Project-Scoped Configuration

For project-specific access, use the `--scope project` flag:

```bash
claude mcp add deep-research \
  --scope project \
  --env OPENAI_API_KEY="sk-your-openai-api-key-here" \
  --env DEEPRESEARCH_MODEL="o3-deep-research-2025-06-26" \
  -- python -m mcp_deepresearch
```

#### Method 3: User-Wide Configuration

For access across all your projects:

```bash
claude mcp add deep-research \
  --scope user \
  --env OPENAI_API_KEY="sk-your-openai-api-key-here" \
  --env DEEPRESEARCH_MODEL="o3-deep-research-2025-06-26" \
  -- python -m mcp_deepresearch
```

#### Method 4: Manual Configuration

Alternatively, you can manually configure by editing the appropriate configuration file:

**Local/Project scope** (`.mcp.json` in project root):
```json
{
    "mcpServers": {
        "deep-research": {
            "command": "python",
            "args": ["-m", "mcp_deepresearch"],
            "env": {
                "OPENAI_API_KEY": "sk-your-openai-api-key-here",
                "DEEPRESEARCH_MODEL": "o3-deep-research-2025-06-26"
            }
        }
    }
}
```

### Adding to OpenAI Codex

For OpenAI Codex integration, add the server to your `~/.codex/config.toml` file:

```toml
[mcp_servers.deep-research]
command = "python"
args = ["-m", "mcp_deepresearch"]
env = { 
    "OPENAI_API_KEY" = "sk-your-openai-api-key-here",
    "DEEPRESEARCH_MODEL" = "o3-deep-research-2025-06-26"
}
```

### Testing Your Configuration

After adding the server, you can test it using the MCP Inspector:

```bash
# Test with Claude Code
claude mcp list

# Test with Codex
npx @modelcontextprotocol/inspector codex mcp
```

## Usage

Once configured, the MCP server exposes a `deep_research` tool that can be called by compatible AI assistants.

### Tool Parameters

- **query** (required): The detailed research question or topic
- **context** (optional): Background context about the research query
- **research_depth** (optional): Research thoroughness level (e.g., "comprehensive", "focused", "surface-level")
- **domain_restrictions** (optional): Domain limitations (e.g., "academic sources only", "recent news articles")  
- **output_format** (optional): Preferred output structure (e.g., "detailed report", "executive summary", "bullet points")

### Example Usage in Claude Code

```
Please use the deep_research tool to investigate the latest developments in quantum computing, 
focusing on recent breakthrough papers from academic sources, and provide a comprehensive 
technical analysis.
```

This would internally call:
```python
deep_research(
    query="latest developments in quantum computing breakthroughs", 
    context="investigating cutting-edge quantum computing research",
    research_depth="comprehensive",
    domain_restrictions="academic sources only", 
    output_format="technical analysis"
)
```

## Available Models

The server supports two OpenAI DeepResearch models:

- **o3-deep-research-2025-06-26**: Optimized for in-depth synthesis and higher-quality output
- **o4-mini-deep-research-2025-06-26**: Lightweight and faster alternative

## Cost Considerations  

- Research requests typically cost $2-5 per query (depending on complexity and model)
- No caching is implemented to avoid storage costs
- Consider setting usage limits in your OpenAI account if needed

## Running the Server

### Direct Execution

```bash
python -m mcp_deepresearch
```

### With Custom Configuration

```bash
OPENAI_API_KEY="your-key" DEEPRESEARCH_MODEL="o4-mini-deep-research-2025-06-26" python -m mcp_deepresearch
```

### Development Mode

For development and testing:

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run with debug logging  
python -c "import logging; logging.basicConfig(level=logging.DEBUG); from mcp_deepresearch.server import main; main()"
```

## Error Handling

The server handles various error conditions:

- **Authentication Errors**: Invalid or missing OpenAI API key
- **API Failures**: Network issues, rate limiting, or OpenAI service problems  
- **Parameter Validation**: Invalid input parameters or malformed requests
- **Timeout Issues**: Long-running research requests that exceed limits

All errors are properly formatted as MCP errors and logged for debugging.

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY environment variable is required"**
   - Ensure your OpenAI API key is set in the environment or MCP configuration

2. **"DeepResearch API error: 401 Unauthorized"**
   - Verify your API key is valid and has access to DeepResearch models

3. **"Research request timeout"**
   - Research can take 5-20 minutes; ensure your client has appropriate timeout settings

4. **"No research content returned"**
   - Check OpenAI's service status and your account usage limits

### Debug Logging

Enable debug logging to troubleshoot issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Development

### Project Structure

```
mcp_deepresearch/
├── __init__.py          # Package initialization
├── server.py            # Main MCP server implementation
requirements.txt         # Dependencies
pyproject.toml          # Project configuration  
PRD.md                  # Product Requirements Document
README.md               # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper tests
4. Submit a pull request

### Code Style

The project uses:
- **Black** for code formatting
- **MyPy** for type checking  
- **Ruff** for linting

Run code quality checks:
```bash
black mcp_deepresearch/
mypy mcp_deepresearch/
ruff check mcp_deepresearch/
```

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Check the [troubleshooting section](#troubleshooting)
- Review OpenAI's [DeepResearch documentation](https://platform.openai.com/docs/guides/deep-research)
- Open an issue on GitHub

## Acknowledgments

- Built with the [Model Context Protocol](https://modelcontextprotocol.io/)
- Powered by [OpenAI's DeepResearch](https://openai.com/index/introducing-deep-research/)
- Uses the official [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)