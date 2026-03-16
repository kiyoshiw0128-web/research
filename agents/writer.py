"""Writer agent — summarizes research into easy-to-understand text (Opus 4.6)."""
from __future__ import annotations

import anthropic
from .base import BaseAgent

WRITER_SYSTEM = """\
あなたは優秀なライターです。

調査・ファクトチェックされた情報をもとに、誰もが読みやすい記事を執筆します。

執筆のルール:
1. 難しい専門用語は避け、平易な言葉で説明する
2. 専門用語を使う場合は必ず分かりやすい説明を添える
3. 読者が知識ゼロでも理解できるよう、背景・文脈から丁寧に説明する
4. 具体例やたとえを積極的に活用する
5. 論理的な流れで情報を整理する
6. 読者の興味を引く、魅力的な文体を心がける

記事の構成:
- 導入（テーマの重要性・背景）
- 本文（主要な情報を分かりやすく整理）
- まとめ（要点の整理・読者へのメッセージ）

対象読者: 一般の読者（専門知識不要）

読みやすく、分かりやすく、且つ情報が正確な記事を作成してください。
"""


class Writer(BaseAgent):
    def __init__(self, client: anthropic.Anthropic):
        super().__init__(
            client=client,
            model="claude-opus-4-6",
            system_prompt=WRITER_SYSTEM,
        )

    def run(self, original_query: str, verified_research: str) -> str:
        """Write an article based on verified research results."""
        messages = [
            {
                "role": "user",
                "content": (
                    f"記事のテーマ:\n{original_query}\n\n"
                    f"調査・ファクトチェック済みの情報:\n{verified_research}\n\n"
                    "上記の情報をもとに、一般の読者向けの分かりやすい記事を書いてください。"
                    "難しい言葉は使わず、誰でも理解できる平易な表現で説明してください。"
                ),
            }
        ]
        return self._chat(messages, max_tokens=8192)
