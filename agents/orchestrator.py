"""Orchestrator agent — coordinates all other agents."""
from __future__ import annotations

import json
import anthropic
from .base import BaseAgent

ORCHESTRATOR_SYSTEM = """\
あなたはリサーチエージェントシステムの総指揮者（オーケストレーター）です。

ユーザーからの依頼を受け取り、以下のエージェントのうちどれに依頼するかを判断し、
適切な順序で各エージェントを呼び出してください。

利用可能なエージェント:
- researcher: X・インターネット・論文・ブログなどを多角的に調査する
- fact_checker: 調査結果のファクトチェックを行う
- writer: 調査結果をわかりやすい文章にまとめる
- proofreader: ライターが書いた文章を熟読し、記事として仕上げる

通常のリサーチ依頼の場合、以下の順序で処理してください:
1. researcher → 調査
2. fact_checker → 事実確認
3. writer → 執筆
4. proofreader → 校閲・仕上げ

ユーザーの依頼内容に応じて、必要なエージェントのみを呼び出すことも可能です。
例えば、単純な質問には researcher のみ、執筆依頼には writer のみなど。

最終的な出力はユーザーが読みやすい形式で提供してください。
"""


class Orchestrator(BaseAgent):
    def __init__(self, client: anthropic.Anthropic):
        super().__init__(
            client=client,
            model="claude-sonnet-4-6",
            system_prompt=ORCHESTRATOR_SYSTEM,
        )

    def run(self, user_query: str, pipeline_results: dict) -> str:
        """
        Decide the pipeline plan based on the user query.
        Returns a JSON plan or plain text depending on the stage.
        """
        messages = [
            {
                "role": "user",
                "content": (
                    f"ユーザーの依頼:\n{user_query}\n\n"
                    "この依頼に対して、どのエージェントをどの順番で呼び出すべきか判断してください。"
                    "JSONで以下の形式で回答してください:\n"
                    '{"pipeline": ["researcher", "fact_checker", "writer", "proofreader"]}'
                    "\n\n必要なエージェントだけを含め、必要に応じて順序を変えてください。"
                ),
            }
        ]
        response = self._chat(messages)

        # Extract JSON from response
        try:
            start = response.index("{")
            end = response.rindex("}") + 1
            plan = json.loads(response[start:end])
            return plan.get("pipeline", ["researcher", "fact_checker", "writer", "proofreader"])
        except (ValueError, json.JSONDecodeError):
            return ["researcher", "fact_checker", "writer", "proofreader"]

    def summarize(self, user_query: str, final_article: str) -> str:
        """Provide a final summary/introduction for the output."""
        messages = [
            {
                "role": "user",
                "content": (
                    f"ユーザーの依頼: {user_query}\n\n"
                    f"完成した記事:\n{final_article}\n\n"
                    "この記事の簡単な紹介文（2〜3文）を書いてください。"
                ),
            }
        ]
        return self._chat(messages)
