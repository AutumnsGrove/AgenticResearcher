"""
Specialized agents for the Agentic Research System.

Each agent has a specific role in the research workflow:
- Orchestrator: Coordinates research and manages agent lifecycle
- SearchAgent: Executes searches via MCP Omnisearch tools
- VerificationAgent: Quality control and sufficiency checking
- CompressionAgent: Automatic content compression
- ContextEditor: Context window optimization
- SynthesisAgent: Final report generation
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .orchestrator import OrchestratorAgent
    from .search_agent import SearchAgent
    from .verification_agent import VerificationAgent
    from .compression_agent import CompressionAgent
    from .context_editor import ContextEditorAgent
    from .synthesis_agent import SynthesisAgent

__all__ = [
    "OrchestratorAgent",
    "SearchAgent",
    "VerificationAgent",
    "CompressionAgent",
    "ContextEditorAgent",
    "SynthesisAgent",
]
