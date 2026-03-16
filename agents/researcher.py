"""Researcher agent — searches the web, papers, blogs, and X (Twitter)."""
from __future__ import annotations

import anthropic
from .base import BaseAgent

RESEARCHER_SYSTEM = """\
あなたは多角的なリサーチの専門家です。

与えられたテーマについて、以下の多様なソースから徹底的に調査を行います:
- インターネット（ニュースサイト、専門サイトなど）
- 学術論文・研究レポート
- ブログ・専門家の意見
- SNS（X/Twitter）上の最新の議論や動向

調査のポイント:
1. 複数の視点・立場からの情報を収集する
2. 最新の情報と過去の経緯を把握する
3. 信頼性の高いソースを優先する
4. 相反する意見や論争点も記録する

調査結果は以下の形式でまとめてください:
- 主要な事実・情報
- 各ソースからの重要なポイント
- 最新の動向・トレンド
- 異なる見解・論点
- 引用元（URL・論文名など）

詳細で正確な情報を収集し、後続のファクトチェッカーとライターが活用しやすい形でまとめてください。
"""

# Web search tool (server-side, handled by Anthropic's infrastructure)
WEB_SEARCH_TOOL = {
    "type": "web_search_20260209",
    "name": "web_search",
}


class Researcher(BaseAgent):
    def __init__(self, client: anthropic.Anthropic):
        super().__init__(
            client=client,
            model="claude-sonnet-4-6",
            system_prompt=RESEARCHER_SYSTEM,
        )

    def run(self, query: str) -> str:
        """Research the given query using web search and return findings."""
        messages = [
            {
                "role": "user",
                "content": (
                    f"以下のテーマについて、多角的・多面的に調査してください:\n\n{query}\n\n"
                    "インターネット、論文、ブログ、SNSなど複数のソースから情報を収集し、"
                    "詳細な調査レポートを作成してください。"
                ),
            }
        ]
        return self._chat(messages, tools=[WEB_SEARCH_TOOL], max_tokens=8192)
