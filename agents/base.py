"""Base agent class shared by all agents."""
from __future__ import annotations

import anthropic


class BaseAgent:
    def __init__(self, client: anthropic.Anthropic, model: str, system_prompt: str):
        self.client = client
        self.model = model
        self.system_prompt = system_prompt

    def _chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        max_tokens: int = 4096,
    ) -> str:
        kwargs: dict = {
            "model": self.model,
            "max_tokens": max_tokens,
            "system": self.system_prompt,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools

        # Server-side tools (web_search) are handled automatically by the API.
        # We only need to loop when stop_reason == "pause_turn" (server hit its
        # iteration limit) by re-sending the assistant turn.
        current_messages = list(messages)
        max_continuations = 5

        for _ in range(max_continuations):
            response = self.client.messages.create(**kwargs | {"messages": current_messages})

            if response.stop_reason == "pause_turn":
                # Append assistant response and continue
                current_messages = current_messages + [
                    {"role": "assistant", "content": response.content}
                ]
                continue

            # end_turn or any other terminal state
            break

        text_blocks = [b.text for b in response.content if b.type == "text"]
        return "\n".join(text_blocks)
