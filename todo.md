# MCP Server Implementation TODO

## 🎯 Goal
Create an MCP server that integrates the Deep Research CLI, providing tools and resources for conducting research within Claude Code and other MCP clients.

## 🏗️ Architecture Overview

Your idea is **definitely feasible**! Here's how it can work:

### Core Concept
- **Tool**: `start_deep_research` - Initiates research and returns immediately
- **Resources**: Each research session creates a resource representing the .md file
- **Background Processing**: Research continues while tool call completes
- **Notifications**: Client gets notified when research completes via resource updates

### Solving the Timeout Problem
The key insight is that MCP tools **can return immediately** while work continues in background:

1. Tool call starts research process → Returns resource URI immediately
2. Background task monitors research progress → Updates resource when complete
3. Resource notification alerts client → Client can fetch updated content

## 📋 Implementation Plan

### Phase 1: Basic MCP Server Structure

#### 1.1 Project Setup
- [ ] Create new directory: `deepresearch_mcp/`
- [ ] Setup `pyproject.toml` for MCP server
- [ ] Create basic MCP server structure using `mcp` Python SDK

#### 1.2 Dependencies
```toml
dependencies = [
    "mcp>=1.0.0",
    "deepresearch-cli>=1.0.0",  # Our existing CLI
    "asyncio",
    "pathlib",
    "uuid",
    "watchdog",  # For file system monitoring
]
```

### Phase 2: Core MCP Components

#### 2.1 Tools Implementation
- [ ] **`start_deep_research`** tool:
  ```python
  @mcp.tool()
  async def start_deep_research(
      query: str,
      format_type: Optional[str] = None,
      context: Optional[str] = None,
      focus: Optional[str] = None,
      model: str = "o4-mini-deep-research"
  ) -> str:
      """Start deep research and return resource URI immediately"""
      research_id = str(uuid.uuid4())
      resource_uri = f"deepresearch://research/{research_id}"

      # Start background research
      asyncio.create_task(_start_background_research(
          research_id, query, format_type, context, focus, model
      ))

      return f"Research started! Track progress at: {resource_uri}"
  ```

#### 2.2 Resources Implementation
- [ ] **Dynamic Resource Provider**:
  ```python
  @mcp.resource("deepresearch://research/{research_id}")
  async def get_research_resource(research_id: str) -> Resource:
      """Provide research content as MCP resource"""
      research_data = _get_research_status(research_id)

      if research_data["status"] == "completed":
          content = _load_markdown_content(research_data["file_path"])
      else:
          content = f"Research in progress... Status: {research_data['status']}"

      return Resource(
          uri=f"deepresearch://research/{research_id}",
          name=f"Research: {research_data['query'][:50]}...",
          mimeType="text/markdown",
          text=content
      )
  ```

#### 2.3 Background Processing
- [ ] **Research Manager**:
  ```python
  async def _start_background_research(research_id, query, format_type, context, focus, model):
      """Run deepresearch CLI in background and monitor progress"""

      # Store research metadata
      research_registry[research_id] = {
          "status": "running",
          "query": query,
          "started_at": datetime.now(),
          "file_path": None
      }

      try:
          # Use our existing CLI
          result = await conduct_research(
              query=query,
              output_path=f"./research_output/{research_id}.md",
              format_type=format_type,
              context=context,
              focus=focus,
              model=model
          )

          # Update status
          research_registry[research_id].update({
              "status": "completed",
              "completed_at": datetime.now(),
              "file_path": f"./research_output/{research_id}.md"
          })

          # Notify subscribers
          await _notify_resource_updated(f"deepresearch://research/{research_id}")

      except Exception as e:
          research_registry[research_id].update({
              "status": "failed",
              "error": str(e)
          })
  ```

### Phase 3: Advanced Features

#### 3.1 Resource Notifications
- [ ] Implement resource subscription system
- [ ] Send notifications when research completes
- [ ] Handle resource updates efficiently

#### 3.2 File System Integration
- [ ] Watch `./research_output/` directory for file changes
- [ ] Auto-register new .md files as resources
- [ ] Support listing all research results

#### 3.3 Status Tool
- [ ] **`list_research`** tool - List all research sessions
- [ ] **`get_research_status`** tool - Check specific research progress

### Phase 4: Enhanced Functionality

#### 4.1 Research Management
- [ ] **`cancel_research`** tool - Cancel running research
- [ ] **`delete_research`** tool - Remove research results
- [ ] **`export_research`** tool - Export to different formats

#### 4.2 Resource Organization
- [ ] Group resources by date/topic
- [ ] Search through research results
- [ ] Tag and categorize research

## 🔧 Technical Implementation Details

### MCP Server Entry Point
```python
# deepresearch_mcp/server.py
from mcp.server.models import Resource
from mcp.server import Server, NotificationOptions
from mcp.types import TextResourceContents

app = Server("deepresearch-mcp")

# Global research registry
research_registry = {}

@app.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List all available research resources"""
    resources = []
    for research_id, data in research_registry.items():
        resources.append(Resource(
            uri=f"deepresearch://research/{research_id}",
            name=f"Research: {data['query'][:50]}...",
            description=f"Status: {data['status']}",
            mimeType="text/markdown"
        ))
    return resources

# ... tools and resource handlers
```

### Configuration
```json
// deepresearch-mcp-config.json
{
  "name": "deepresearch-mcp",
  "version": "1.0.0",
  "description": "MCP server for OpenAI Deep Research integration",
  "tools": [
    "start_deep_research",
    "list_research",
    "get_research_status",
    "cancel_research"
  ],
  "resources": [
    "deepresearch://research/*"
  ]
}
```

## 🚀 Usage Example

Once implemented, Claude Code could use it like this:

```python
# Start research
research_uri = await start_deep_research(
    query="Latest developments in quantum computing",
    focus="academic",
    format_type="technical analysis"
)

# Resource is immediately available (shows "in progress")
content = await get_resource(research_uri)

# Later, when research completes, client gets notification
# and can fetch updated content with full research results
```

## 💡 Key Benefits

1. **No Timeout Issues**: Tool returns immediately with resource URI
2. **Real-time Updates**: Resources update automatically when research completes
3. **Persistent Storage**: Research results are saved as resources
4. **Background Processing**: Multiple research sessions can run concurrently
5. **Integration Ready**: Works seamlessly with Claude Code and other MCP clients

## 🔍 Next Steps

1. **Start with Phase 1**: Basic MCP server structure
2. **Test with simple tool**: Verify MCP integration works
3. **Add background processing**: Implement the core async pattern
4. **Add resource notifications**: Complete the feedback loop
5. **Enhance with advanced features**: Add management tools

## 📚 Resources to Reference

- [MCP Server Concepts](https://modelcontextprotocol.io/docs/learn/server-concepts)
- [MCP Resources Specification](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)
- [Claude Code MCP Integration](https://docs.anthropic.com/en/docs/claude-code/mcp)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

This implementation approach **definitely works** and solves the timeout problem elegantly! The combination of immediate tool responses + background processing + resource notifications is exactly how MCP is designed to handle long-running tasks.