"""Proofreader (校閲者) agent — polishes the article into a final publishable piece."""
from __future__ import annotations

import anthropic
from .base import BaseAgent

PROOFREADER_SYSTEM = """\
あなたは経験豊かな校閲者（編集者）です。

ライターが書いた記事を熟読し、出版可能な完成品に仕上げることが役割です。

校閲のポイント:
1. 文章の流れと読みやすさ
   - 文章が自然に流れているか
   - 段落の構成は適切か
   - 読者を引きつける表現になっているか

2. 表現の統一性
   - 文体・トーンが記事全体で一貫しているか
   - 専門用語の使い方が統一されているか

3. 内容の明確さ
   - 各段落の主旨が明確か
   - 情報の優先順位付けは適切か
   - 不必要な繰り返しや冗長な表現がないか

4. 誤字・脱字・文法
   - 誤字脱字のチェック
   - 文法的な誤りの修正

5. 全体的な完成度
   - タイトルは魅力的で内容を反映しているか
   - 導入部は読者の興味を引くか
   - 結論は印象的で記憶に残るか

修正した最終版の記事を、読者に届ける完成品として提供してください。
記事には以下を含めてください:
- 魅力的なタイトル
- リード文（記事の要約・導入）
- 本文
- まとめ
"""


class Proofreader(BaseAgent):
    def __init__(self, client: anthropic.Anthropic):
        super().__init__(
            client=client,
            model="claude-opus-4-6",
            system_prompt=PROOFREADER_SYSTEM,
        )

    def run(self, original_query: str, draft_article: str) -> str:
        """Proofread and polish the draft article into a final publishable piece."""
        messages = [
            {
                "role": "user",
                "content": (
                    f"記事のテーマ:\n{original_query}\n\n"
                    f"ライターが書いた下書き:\n{draft_article}\n\n"
                    "上記の下書きを熟読し、読者に届ける完成品として仕上げてください。"
                    "魅力的なタイトル、読みやすい構成、洗練された表現で、"
                    "出版できるクオリティの記事を作成してください。"
                ),
            }
        ]
        return self._chat(messages, max_tokens=8192)
