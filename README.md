# Deep Research CLI

🔍 **Command-line interface for OpenAI's Deep Research API** - Conduct comprehensive research from your terminal and save results to markdown files.

Deep Research CLI leverages OpenAI's powerful Deep Research models (o3-deep-research & o4-mini-deep-research) to perform multi-step research, web searching, and information synthesis, generating comprehensive reports with citations.

## 🚀 Quick Start

```bash
# Install the CLI
pip install deepresearch-cli

# Set your OpenAI API key
export OPENAI_API_KEY=your-key-here

# Conduct research
deepresearch "Latest developments in quantum computing" -o research.md

# Research with specific formatting
deepresearch "Climate change impacts on agriculture" -o climate.md --format executive-summary
```

## 📦 Installation

### Via pip (Recommended)
```bash
pip install deepresearch-cli
```

### From source
```bash
git clone https://github.com/yourusername/cli-deepresearch.git
cd cli-deepresearch
pip install -e .
```

## 🛠️ Usage

### Basic Usage
```bash
deepresearch "Your research question" -o output_file.md
```

### Advanced Usage
```bash
deepresearch "AI safety research 2024" \
  --output reports/ai_safety.md \
  --format detailed-report \
  --model o3-deep-research-2025-06-26
```

### Available Options

| Option | Description | Default |
|--------|-------------|---------|
| `query` | Research question or topic (required) | - |
| `-o, --output` | Output file path (required) | - |
| `--model` | OpenAI model to use | `o4-mini-deep-research-2025-06-26` |
| `--format` | Output format preference (flexible) | None (optimized automatically) |
| `--context` | Background context for the research query | None |
| `--focus` | Source focus (academic, business, news, etc.) | None |
| `--sync` | Use synchronous mode (not recommended) | Background mode |
| `--no-enhance` | Disable prompt enhancement (faster) | Enhancement enabled |
| `-v, --verbose` | Enable verbose logging | False |

### Output Formats (Flexible)

Format preferences are now completely **flexible and open-ended**:

- **`"detailed report"`** - Comprehensive report with sections and analysis
- **`"executive summary"`** - Concise summary with key findings
- **`"technical analysis"`** - In-depth technical deep-dive
- **`"bullet points"`** - Structured bullet point format
- **`"comparison table"`** - Tabular comparison format
- **`"timeline"`** - Chronological timeline format
- **Custom formats** - Any format description (e.g., "infographic-style", "Q&A format")

### Source Focus Options

Control which types of sources the research prioritizes:

- **`academic`** - Peer-reviewed research, scholarly papers, academic publications
- **`business`** - Industry reports, market research, financial data, company reports
- **`news`** - Recent news articles, press releases, current events coverage
- **`reports`** - Official reports, government documents, white papers
- **`technical`** - Technical documentation, specifications, standards
- **Custom focus** - Any source description (e.g., "startup ecosystem", "regulatory documents")

### Models Available

- **`o4-mini-deep-research-2025-06-26`** - Fast and cost-effective (default)
- **`o3-deep-research-2025-06-26`** - More comprehensive but slower and more expensive

## ⏱️ Research Process

Deep Research typically takes **5-10 minutes** to complete:

1. **Prompt Enhancement** - Uses GPT-5-mini to optimize your research query (optional)
2. **Query Processing** - Analyzes and enhances your research question
3. **Web Research** - Searches multiple sources across the internet
4. **Source Analysis** - Reads and analyzes relevant documents
5. **Synthesis** - Combines findings into a comprehensive report
6. **Citation** - Adds inline citations and source references

### 🔧 Prompt Enhancement

By default, the CLI uses **GPT-5-mini** to enhance your research query before sending it to the Deep Research model. This:

- **Improves research quality** by adding specific instructions for the researcher
- **Optimizes source selection** based on your focus preferences
- **Structures output format** according to your requirements
- **Incorporates context** to provide more relevant results

You can disable this with `--no-enhance` for faster (but less optimized) results.

## 💰 Cost Considerations

- **`o4-mini-deep-research`**: ~**$0.20 per query** (fast and cost-effective)
- **`o3-deep-research`**: ~**$1.00 per query** (comprehensive but more expensive)
- Final cost depends on query complexity and research depth
- The CLI provides detailed cost breakdown after each research session
- No caching is implemented - each query runs fresh research

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | ✅ |

### Getting an API Key

1. Sign up at [OpenAI Platform](https://platform.openai.com)
2. Navigate to API Keys section
3. Create a new API key
4. Set the environment variable:
   ```bash
   export OPENAI_API_KEY=sk-your-key-here
   ```

## 📋 Examples

### Research Examples

```bash
# Basic Research
deepresearch "Emerging trends in artificial intelligence 2024" -o ai_trends.md

# Academic Research with Source Focus
deepresearch "Recent breakthroughs in cancer immunotherapy" -o cancer_research.md --focus academic --format "technical analysis"

# Business Analysis with Context
deepresearch "Electric vehicle market opportunities" -o ev_market.md \
  --context "For venture capital investment decision" \
  --focus business --format "executive summary"

# News Research
deepresearch "Latest AI regulation updates" -o ai_regulation.md --focus news

# Technical Documentation Research
deepresearch "Kubernetes best practices 2024" -o k8s_guide.md --focus technical --format "implementation guide"

# Custom Focus and Format
deepresearch "Startup ecosystem in biotech" -o biotech_startups.md \
  --focus "startup databases and industry reports" \
  --format "investor briefing with key metrics tables"
```

## 🤖 Claude Code Sub-Agent Integration

This repository includes a pre-configured Claude Code sub-agent for seamless integration. The sub-agent enables Claude Code to automatically conduct deep research using this CLI tool.

### Quick Setup

1. **Copy the sub-agent configuration**:
   ```bash
   # For user-level installation (recommended)
   mkdir -p ~/.claude/agents
   cp deep-research-cli.md ~/.claude/agents/

   # For project-level installation
   mkdir -p .claude/agents
   cp deep-research-cli.md .claude/agents/
   ```

2. **Verify installation**:
   ```bash
   # In Claude Code, check available agents
   /agents
   ```

3. **The sub-agent will automatically activate** when you ask Claude Code for comprehensive research on complex topics.

### How It Works

The `deep-research-cli` sub-agent:
- **Activates automatically** when Claude detects research needs
- **Takes 10 minutes** to complete thorough research
- **Stores results** in `./deepresearch/` folder
- **Uses all available CLI parameters** for optimal results
- **Provides comprehensive analysis** with citations and sources

### Usage Examples

Once installed, simply ask Claude Code questions like:

```
"I need comprehensive research on quantum computing developments"
"Research the environmental impact of lithium battery production"
"Analyze recent AI regulation changes across different countries"
```

Claude Code will automatically use the deep-research sub-agent for thorough investigation.

### Manual Sub-Agent Creation

If you want to customize the sub-agent or create similar ones, reference the [Claude Code Sub-Agents Documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents) and use `deep-research-cli.md` as a template.

Key requirements for Claude Code sub-agents:
- Must be a Markdown file with YAML frontmatter
- Requires `name`, `description`, and optionally `tools` fields
- Store in `~/.claude/agents/` (user-level) or `.claude/agents/` (project-level)
- Use focused, single-responsibility design

## 🧪 Development

### Running from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/cli-deepresearch.git
cd cli-deepresearch

# Install in development mode
pip install -e .

# Run directly
python -m deepresearch_cli "Your research question" -o output.md

# Or use the installed command
deepresearch "Your research question" -o output.md
```

### Testing the CLI

```bash
# Test basic functionality (requires OPENAI_API_KEY)
deepresearch "What is Python programming language?" -o test.md --verbose

# Test with focus and format
deepresearch "Benefits of exercise" -o exercise.md --focus academic --format "bullet points"

# Test with context and custom focus
deepresearch "Machine learning trends" -o ml.md \
  --context "For a tech startup CTO" \
  --focus "industry reports and startup news" \
  --format "executive summary"

# Test without prompt enhancement (faster)
deepresearch "Quick overview of blockchain" -o blockchain.md --no-enhance
```

## 📄 Output Format

Research results are saved as markdown files with:

- **Metadata header** - Query, timestamp, model used
- **Comprehensive content** - Research findings with structure
- **Inline citations** - Source links and references
- **Footer** - Tool attribution

Example output structure:
```markdown
# Deep Research Results

**Query:** Your research question
**Generated:** 2024-01-15 14:30:00
**Model:** o3-deep-research-2025-06-26
**Tool:** deepresearch-cli

---

[Research content with inline citations]

---

*Generated using OpenAI Deep Research via deepresearch-cli*
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/cli-deepresearch/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/cli-deepresearch/discussions)

## ⚠️ Important Notes

- **API Costs**: Deep Research queries consume OpenAI API credits
- **Time Requirements**: Each query takes 5-10 minutes to complete
- **Rate Limits**: Respect OpenAI's rate limits for your account tier
- **Content Policy**: Follow OpenAI's usage policies for research content

---

Built with ❤️ using OpenAI's Deep Research API