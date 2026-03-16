"""Fact Checker agent — verifies research results and re-researches if needed."""
from __future__ import annotations

import anthropic
from .base import BaseAgent

FACT_CHECKER_SYSTEM = """\
あなたはファクトチェックの専門家です。

提供された調査内容を徹底的に検証し、以下の観点から確認を行います:
1. 事実の正確性（数字、日付、固有名詞など）
2. 情報の一貫性（矛盾する記述がないか）
3. ソースの信頼性
4. 最新性（情報が古くなっていないか）
5. 偏りや誇張がないか

検証プロセス:
- 疑わしい情報はウェブ検索で確認する
- 不正確な情報は修正し、その理由を明記する
- 確認できなかった情報は「要確認」として明示する
- 正確性に問題がある場合は、追加調査を行う

出力形式:
1. ファクトチェック結果（各項目の正確性評価）
2. 修正・補足が必要な情報のリスト
3. 検証済みの調査内容（修正版）

情報の正確性と信頼性を最優先に、厳格な確認を行ってください。
"""

WEB_SEARCH_TOOL = {
    "type": "web_search_20260209",
    "name": "web_search",
}


class FactChecker(BaseAgent):
    def __init__(self, client: anthropic.Anthropic):
        super().__init__(
            client=client,
            model="claude-sonnet-4-6",
            system_prompt=FACT_CHECKER_SYSTEM,
        )

    def run(self, original_query: str, research_result: str) -> str:
        """Verify research results and return fact-checked content."""
        messages = [
            {
                "role": "user",
                "content": (
                    f"元の調査テーマ:\n{original_query}\n\n"
                    f"調査結果:\n{research_result}\n\n"
                    "上記の調査内容をファクトチェックしてください。"
                    "不正確な情報や確認が必要な情報があれば、ウェブ検索で追加確認を行い、"
                    "正確な情報に修正した調査レポートを提供してください。"
                ),
            }
        ]
        return self._chat(messages, tools=[WEB_SEARCH_TOOL], max_tokens=8192)
