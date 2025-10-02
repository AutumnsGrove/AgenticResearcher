"""
MCP Integration Module

Wrappers for MCP servers (Omnisearch and Sequential Thinking)
"""

from .omnisearch import OmnisearchWrapper, SearchProvider, PROVIDER_SPECS
from .sequential_thinking import SequentialThinkingWrapper, ResearchPlan, VerificationAnalysis

__all__ = [
    'OmnisearchWrapper',
    'SearchProvider',
    'PROVIDER_SPECS',
    'SequentialThinkingWrapper',
    'ResearchPlan',
    'VerificationAnalysis'
]
