from __future__ import annotations

from collections import deque
from typing import Deque, Dict, List, Optional


class ContextManager:
    def __init__(self, max_history: int = 20):
        self.max_history: int = max_history
        self._history: Deque[Dict[str, object]] = deque(maxlen=max_history)

    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, object]] = None):
        message = {"role": role, "content": content, "timestamp": "now"}
        if metadata:
            message["metadata"] = metadata
        self._history.append(message)

    def get_conversation_history(self, last_n: int = 10) -> List[Dict[str, object]]:
        items = list(self._history)
        if last_n is not None:
            return items[-last_n:]
        return items

    def clear(self):
        self._history.clear()


context_manager = ContextManager()
