#!/usr/bin/env python3
"""
Deep Research CLI - OpenAI Deep Research from the command line.

A simple CLI tool that leverages OpenAI's Deep Research API to conduct
comprehensive research and save results to markdown files.
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from openai import AsyncOpenAI
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("deepresearch-cli")


class DeepResearchConfig:
    """Configuration for Deep Research CLI."""

    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            logger.error("OPENAI_API_KEY environment variable not set")
            sys.exit(1)


async def enhance_research_prompt(
    query: str,
    context: Optional[str] = None,
    focus: Optional[str] = None,
    format_type: Optional[str] = None,
    client: AsyncOpenAI = None
) -> str:
    """Enhance the research prompt using an intermediate model like gpt-5-mini."""

    instructions = """
You will be given a research task by a user. Your job is to produce a set of
instructions for a researcher that will complete the task. Do NOT complete the
task yourself, just provide instructions on how to complete it.

GUIDELINES:
1. **Maximize Specificity and Detail**
- Include all known user preferences and explicitly list key attributes or
  dimensions to consider.
- It is of utmost importance that all details from the user are included in
  the instructions.

2. **Fill in Unstated But Necessary Dimensions as Open-Ended**
- If certain attributes are essential for a meaningful output but the user
  has not provided them, explicitly state that they are open-ended or default
  to no specific constraint.

3. **Avoid Unwarranted Assumptions**
- If the user has not provided a particular detail, do not invent one.
- Instead, state the lack of specification and guide the researcher to treat
  it as flexible or accept all possible options.

4. **Use the First Person**
- Phrase the request from the perspective of the user.

5. **Structure and Organization**
- If you determine that including tables, charts, or structured sections will help
  organize the information, explicitly request that the researcher provide them.
- Ask for clear headers and formatting that ensures clarity and structure.

6. **Source Requirements**
- Be specific about source prioritization based on the user's focus area.
- For academic queries, prefer peer-reviewed research and official publications.
- For business analysis, prioritize industry reports, financial data, and market research.
- For current events, focus on reliable news sources and official statements.
- Always request inline citations and source metadata.

7. **Analysis Depth**
- Be analytical and avoid generalities.
- Request specific figures, trends, statistics, and measurable outcomes.
- Ensure each section supports data-backed reasoning.
"""

    # Build the enhanced prompt request
    prompt_parts = [f"Research Query: {query}"]

    if context:
        prompt_parts.append(f"Background Context: {context}")

    if focus:
        prompt_parts.append(f"Source Focus: {focus}")

    if format_type:
        prompt_parts.append(f"Preferred Output Format: {format_type}")

    input_text = "\n\n".join(prompt_parts)

    try:
        logger.debug("Enhancing research prompt with gpt-5-mini...")

        response = await client.responses.create(
            model="gpt-5-mini",
            input=input_text,
            instructions=instructions,
            reasoning={"effort": "low"},
            text={"verbosity": "medium"}
        )

        enhanced_prompt = response.output_text
        logger.debug(f"Enhanced prompt length: {len(enhanced_prompt)} characters")
        return enhanced_prompt

    except Exception as e:
        logger.warning(f"Prompt enhancement failed, using original query: {e}")
        return query


async def conduct_research(
    query: str,
    output_path: str,
    model: str = "o4-mini-deep-research-2025-06-26",
    format_type: Optional[str] = None,
    context: Optional[str] = None,
    focus: Optional[str] = None,
    background: bool = True,
    enhance_prompt: bool = True
) -> str:
    """Conduct deep research using OpenAI's Deep Research API.

    Args:
        query: The research question or topic
        output_path: Where to save the results
        model: OpenAI model to use
        format_type: Output format preference (optional, flexible)
        context: Background context for the research query
        focus: Source focus (e.g., academic, reports, news, etc.)
        background: Whether to use background mode
        enhance_prompt: Whether to use prompt enhancement with intermediate model

    Returns:
        The research results as a string
    """

    config = DeepResearchConfig()
    client = AsyncOpenAI(
        api_key=config.openai_api_key,
        timeout=3600  # 1 hour timeout
    )

    logger.info(f"🔍 Starting Deep Research for: {query[:100]}...")
    logger.info(f"📝 Using model: {model}")
    if format_type:
        logger.info(f"📄 Output format: {format_type}")
    if context:
        logger.info(f"📋 Background context provided")
    if focus:
        logger.info(f"🎯 Source focus: {focus}")
    logger.info(f"💾 Results will be saved to: {output_path}")

    if background:
        logger.info("⏱️  Using background mode (research may take 5-10 minutes)")

    try:
        # Enhance the prompt if requested
        if enhance_prompt:
            logger.info("✨ Enhancing research prompt...")
            enhanced_query = await enhance_research_prompt(
                query, context, focus, format_type, client
            )
        else:
            # Build a basic enhanced query
            enhanced_query = _build_basic_query(query, context, focus, format_type)
        # Make the Deep Research API call
        response = await client.responses.create(
            model=model,
            input=enhanced_query,
            background=background,
            reasoning={"summary": "auto"},
            tools=[{"type": "web_search_preview"}]
        )

        if background:
            logger.info(f"✅ Research started in background! Request ID: {response.id}")
            logger.info("⏳ Polling for completion...")

            # Poll for completion
            while True:
                try:
                    status_response = await client.responses.retrieve(response.id)

                    if hasattr(status_response, 'status'):
                        if status_response.status == "completed":
                            logger.info("🎉 Research completed!")
                            research_result = status_response.output_text
                            break
                        elif status_response.status == "failed":
                            logger.error("❌ Research failed")
                            return "Research failed"
                        else:
                            logger.info(f"⏳ Status: {status_response.status}")

                    await asyncio.sleep(30)  # Poll every 30 seconds

                except Exception as poll_error:
                    logger.debug(f"Polling error: {poll_error}")
                    await asyncio.sleep(30)

        else:
            # Synchronous mode
            research_result = response.output_text
            logger.info("✅ Research completed!")

        # Save results to file
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(_format_results(research_result, query, model))

        logger.info(f"💾 Results saved to: {output_path}")
        logger.info(f"📊 Result length: {len(research_result)} characters")

        return research_result

    except Exception as e:
        error_msg = f"Deep Research API error: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"


def _build_basic_query(query: str, context: Optional[str], focus: Optional[str], format_type: Optional[str]) -> str:
    """Build a basic enhanced query without using prompt enhancement."""

    parts = [f"Research Query: {query}"]

    if context:
        parts.append(f"Background Context: {context}")

    # Source focus guidance
    focus_instructions = {
        "academic": "Prioritize peer-reviewed research, academic papers, official publications, and scholarly sources.",
        "business": "Focus on industry reports, market research, financial data, company reports, and business analytics.",
        "news": "Emphasize recent news articles, press releases, official statements, and current events coverage.",
        "reports": "Concentrate on official reports, government documents, white papers, and institutional publications.",
        "technical": "Focus on technical documentation, specifications, standards, and expert technical sources."
    }

    source_instruction = "Include reliable, up-to-date sources with inline citations."
    if focus and focus.lower() in focus_instructions:
        source_instruction = focus_instructions[focus.lower()]
    elif focus:
        source_instruction = f"Prioritize sources related to: {focus}. Include inline citations."

    parts.append(f"Source Requirements: {source_instruction}")

    if format_type:
        parts.append(f"Output Format: {format_type}")

    parts.extend([
        "Requirements:",
        "- Include specific figures, trends, statistics, and measurable outcomes",
        "- Provide inline citations and return all source metadata",
        "- Be analytical and avoid generalities",
        "- Use clear, professional language",
        "- Structure information with appropriate headers and formatting"
    ])

    return "\n\n".join(parts)


def _format_results(content: str, query: str, model: str) -> str:
    """Format the research results with metadata."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""# Deep Research Results

**Query:** {query}
**Generated:** {timestamp}
**Model:** {model}
**Tool:** deepresearch-cli

---

{content}

---

*Generated using OpenAI Deep Research via deepresearch-cli*
"""


def main():
    """Main CLI entry point."""

    parser = argparse.ArgumentParser(
        description="Deep Research CLI - Comprehensive research using OpenAI's Deep Research API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  deepresearch "Latest AI breakthroughs in 2024" -o research.md
  deepresearch "Climate change impacts" -o climate.md --format "executive summary"
  deepresearch "Quantum computing trends" -o quantum.md --focus academic
  deepresearch "Market analysis for EVs" -o market.md --context "For investment decision" --focus business

Advanced Examples:
  deepresearch "Gene therapy developments" -o gene.md --focus academic --format "technical analysis"
  deepresearch "Tech startup landscape" -o startups.md --context "VC research" --focus "business reports"
  deepresearch "AI regulation updates" -o regulation.md --focus news --no-enhance

Environment Variables:
  OPENAI_API_KEY    Required: Your OpenAI API key

Models:
  o4-mini-deep-research-2025-06-26  Fast and cost-effective (default)
  o3-deep-research-2025-06-26       More comprehensive but slower

Focus Options:
  academic    Peer-reviewed research and scholarly sources
  business    Industry reports, market research, financial data
  news        Recent news articles and current events
  reports     Official reports, government documents, white papers
  technical   Technical documentation and specifications
  [custom]    Any custom focus description
"""
    )

    parser.add_argument(
        "query",
        help="The research question or topic to investigate"
    )

    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output file path (e.g., research_results.md)"
    )

    parser.add_argument(
        "--model",
        default="o4-mini-deep-research-2025-06-26",
        choices=["o3-deep-research-2025-06-26", "o4-mini-deep-research-2025-06-26"],
        help="OpenAI model to use (default: o4-mini-deep-research-2025-06-26)"
    )

    parser.add_argument(
        "--format",
        help="Output format preference (flexible, e.g., 'detailed report', 'executive summary', 'technical analysis', 'bullet points', or any custom format)"
    )

    parser.add_argument(
        "--context",
        help="Background context for the research query"
    )

    parser.add_argument(
        "--focus",
        help="Source focus (e.g., 'academic', 'business', 'news', 'reports', 'technical', or any custom focus)"
    )

    parser.add_argument(
        "--sync",
        action="store_true",
        help="Use synchronous mode instead of background mode (not recommended)"
    )

    parser.add_argument(
        "--no-enhance",
        action="store_true",
        help="Disable prompt enhancement with intermediate model (faster but less optimized)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate OPENAI_API_KEY
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable is required", file=sys.stderr)
        print("\nSet your OpenAI API key:")
        print("  export OPENAI_API_KEY=your-key-here")
        sys.exit(1)

    # Run the research
    try:
        result = asyncio.run(
            conduct_research(
                query=args.query,
                output_path=args.output,
                model=args.model,
                format_type=args.format,
                context=args.context,
                focus=args.focus,
                background=not args.sync,
                enhance_prompt=not args.no_enhance
            )
        )

        if result.startswith("Error:"):
            print(f"❌ {result}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"✅ Research completed successfully!")
            print(f"📄 Results saved to: {args.output}")

    except KeyboardInterrupt:
        print("\n🛑 Research interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()