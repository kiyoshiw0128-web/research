# リサーチエージェントシステム

このリポジトリはリサーチエージェントシステムです。
ユーザーから調査依頼を受けたら、以下のパイプラインを順番に実行してください。

---

## エージェント構成

各エージェントの詳細な定義は `agents/` ディレクトリにあります。

| エージェント | 定義ファイル | 役割 |
|------------|-------------|------|
| Orchestrator（総指揮） | [`agents/orchestrator.md`](agents/orchestrator.md) | ユーザーの依頼を受け取り、必要なエージェントと順序を決定する |
| Researcher（調査） | [`agents/researcher.md`](agents/researcher.md) | X・インターネット・論文・ブログなどを多角的に調査する |
| Fact Checker（事実確認） | [`agents/fact-checker.md`](agents/fact-checker.md) | 調査結果の正確性を検証し、不備があれば再調査する |
| Writer（執筆） | [`agents/writer.md`](agents/writer.md) | 調査結果をわかりやすい文章にまとめる |
| Proofreader（校閲者） | [`agents/proofreader.md`](agents/proofreader.md) | 記事を熟読し、完成記事として仕上げる |

---

## パイプライン

Orchestratorが依頼内容に応じて、以下のパイプラインを選択します。

| パイプライン | フロー | 用途 |
|------------|--------|------|
| A: フルリサーチ | Researcher → Fact Checker → Writer → Proofreader | 新しいトピックの調査 |
| B: 事実確認のみ | Fact Checker | 既存情報の検証 |
| C: 執筆のみ | Writer → Proofreader | 調査済み情報の記事化 |
| D: 簡易調査 | Researcher | 簡単な質問への回答 |

---

## 実行方法

ユーザーから調査依頼を受けたら：

1. **Orchestrator として**、どのパイプラインを使うか宣言する
2. **各エージェントとして**、順番に処理を実行する（各エージェントの詳細は定義ファイルを参照）
3. 各ステップの完了を明示しながら進める
4. 最後に完成した記事を `articles/` ディレクトリに出力する

### 例

ユーザー: 「量子コンピュータの現状を調べてほしい」

```
[Orchestrator] パイプライン: Researcher → Fact Checker → Writer → 校閲者

[Researcher] 調査中...
（WebSearchで情報収集）

[Fact Checker] 事実確認中...
（情報の正確性を検証）

[Writer] 執筆中...
（わかりやすい記事を作成）

[校閲者] 仕上げ中...
（完成記事を出力）
```

---

## ディレクトリ構成

```
research/
├── CLAUDE.md          # このファイル（システム概要）
├── agents/            # エージェント定義ファイル
│   ├── orchestrator.md
│   ├── researcher.md
│   ├── fact-checker.md
│   ├── writer.md
│   └── proofreader.md
└── articles/          # 完成記事の出力先
```
