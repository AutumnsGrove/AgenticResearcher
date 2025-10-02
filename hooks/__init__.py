"""
Hook System for Agentic Research

Centralized hook management for content compression, validation, and context optimization.

Hook Types:
- PRE_TOOL: Execute before tool calls (validation)
- POST_SEARCH: Execute after search tools (compression)
- PRE_MESSAGE: Execute before LLM calls (context optimization)
- POST_MESSAGE: Execute after LLM calls (tracking)

Usage:
    from hooks import HookManager, register_hook

    manager = HookManager()
    await manager.execute_hooks('pre_tool', tool_name='search', arguments={'query': 'test'})
"""

from typing import Dict, List, Callable, Any, Optional
import asyncio

# Import all hook modules
from .compression_hooks import (
    compress_search_results,
    deduplicate_search_results,
    COMPRESSION_HOOKS
)

from .validation_hooks import (
    validate_tool_call,
    validate_search_arguments,
    validate_url_arguments,
    log_tool_execution,
    VALIDATION_HOOKS,
    ValidationError
)

from .context_hooks import (
    optimize_context,
    remove_duplicate_urls,
    prioritize_messages,
    compress_old_messages,
    track_context_stats,
    CONTEXT_HOOKS
)


class HookManager:
    """
    Central hook management system

    Manages registration and execution of hooks across different lifecycle events.
    """

    def __init__(self):
        """Initialize hook manager"""
        self.hooks: Dict[str, List[Callable]] = {
            'pre_tool': [],
            'post_tool': [],
            'pre_search': [],
            'post_search': [],
            'pre_message': [],
            'post_message': [],
        }

        # Register default hooks
        self._register_default_hooks()

    def _register_default_hooks(self):
        """Register all default hooks from modules"""
        # Compression hooks
        for event_type, hook_list in COMPRESSION_HOOKS.items():
            for hook in hook_list:
                self.register_hook(event_type, hook)

        # Validation hooks
        for event_type, hook_list in VALIDATION_HOOKS.items():
            for hook in hook_list:
                self.register_hook(event_type, hook)

        # Context hooks
        for event_type, hook_list in CONTEXT_HOOKS.items():
            for hook in hook_list:
                self.register_hook(event_type, hook)

    def register_hook(self, event_type: str, hook: Callable):
        """
        Register a hook for an event type

        Args:
            event_type: Type of event (pre_tool, post_search, etc.)
            hook: Hook function to register
        """
        if event_type not in self.hooks:
            self.hooks[event_type] = []

        if hook not in self.hooks[event_type]:
            self.hooks[event_type].append(hook)

    def unregister_hook(self, event_type: str, hook: Callable):
        """
        Unregister a hook

        Args:
            event_type: Type of event
            hook: Hook function to unregister
        """
        if event_type in self.hooks and hook in self.hooks[event_type]:
            self.hooks[event_type].remove(hook)

    async def execute_hooks(
        self,
        event_type: str,
        *args,
        **kwargs
    ) -> Any:
        """
        Execute all hooks for an event type

        Args:
            event_type: Type of event
            *args: Positional arguments for hooks
            **kwargs: Keyword arguments for hooks

        Returns:
            Result from hooks (may be modified data)
        """
        hooks = self.hooks.get(event_type, [])

        if not hooks:
            # No hooks registered, return first arg or None
            return args[0] if args else None

        # Sort hooks by priority (if available)
        sorted_hooks = sorted(
            hooks,
            key=lambda h: getattr(h, '_hook_priority', 100),
            reverse=True
        )

        result = args[0] if args else None

        # Execute hooks in sequence
        for hook in sorted_hooks:
            try:
                # Pass result from previous hook
                hook_result = await hook(*args, **kwargs)

                # Update result if hook returns something
                if hook_result is not None:
                    result = hook_result
                    # Update args for next hook
                    if args:
                        args = (result,) + args[1:]

            except Exception as e:
                print(f"⚠️ Hook {hook.__name__} failed: {e}")
                # Continue with other hooks unless it's a validation error
                if isinstance(e, ValidationError):
                    raise

        return result

    def get_registered_hooks(self, event_type: Optional[str] = None) -> Dict[str, List[str]]:
        """
        Get list of registered hooks

        Args:
            event_type: Optional event type to filter by

        Returns:
            Dictionary of event types to hook names
        """
        if event_type:
            return {
                event_type: [h.__name__ for h in self.hooks.get(event_type, [])]
            }

        return {
            evt: [h.__name__ for h in hooks]
            for evt, hooks in self.hooks.items()
            if hooks
        }


# Global hook manager instance
_global_manager: Optional[HookManager] = None


def get_hook_manager() -> HookManager:
    """Get or create global hook manager"""
    global _global_manager
    if _global_manager is None:
        _global_manager = HookManager()
    return _global_manager


def register_hook(event_type: str, hook: Callable):
    """
    Register a hook using the global manager

    Args:
        event_type: Type of event
        hook: Hook function
    """
    manager = get_hook_manager()
    manager.register_hook(event_type, hook)


async def execute_hooks(event_type: str, *args, **kwargs) -> Any:
    """
    Execute hooks using the global manager

    Args:
        event_type: Type of event
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        Result from hooks
    """
    manager = get_hook_manager()
    return await manager.execute_hooks(event_type, *args, **kwargs)


# Export all hook functions and classes
__all__ = [
    # Manager
    'HookManager',
    'get_hook_manager',
    'register_hook',
    'execute_hooks',

    # Compression hooks
    'compress_search_results',
    'deduplicate_search_results',

    # Validation hooks
    'validate_tool_call',
    'validate_search_arguments',
    'validate_url_arguments',
    'log_tool_execution',
    'ValidationError',

    # Context hooks
    'optimize_context',
    'remove_duplicate_urls',
    'prioritize_messages',
    'compress_old_messages',
    'track_context_stats',
]
