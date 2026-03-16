"""
Research Agent System
======================
Multi-agent pipeline for research, fact-checking, writing, and proofreading.

Agents:
  Orchestrator  (claude-sonnet-4-6) — coordinates the pipeline
  Researcher    (claude-sonnet-4-6) — web search & multi-source research
  Fact Checker  (claude-sonnet-4-6) — verifies accuracy, re-researches if needed
  Writer        (claude-opus-4-6)   — writes in plain, easy-to-read language
  Proofreader   (claude-opus-4-6)   — polishes into a publishable article

Usage:
  ANTHROPIC_API_KEY=<key> python main.py
  ANTHROPIC_API_KEY=<key> python main.py "AIの最新動向について調査してください"
"""
from __future__ import annotations

import sys
import anthropic

from agents import Orchestrator, Researcher, FactChecker, Writer, Proofreader

AGENT_DISPLAY_NAMES = {
    "researcher": "Researcher（調査）",
    "fact_checker": "Fact Checker（事実確認）",
    "writer": "Writer（執筆）",
    "proofreader": "Proofreader（校閲）",
}


def run_pipeline(query: str, verbose: bool = True) -> str:
    client = anthropic.Anthropic()

    orchestrator = Orchestrator(client)
    researcher = Researcher(client)
    fact_checker = FactChecker(client)
    writer = Writer(client)
    proofreader = Proofreader(client)

    agent_map = {
        "researcher": researcher,
        "fact_checker": fact_checker,
        "writer": writer,
        "proofreader": proofreader,
    }

    if verbose:
        print("=" * 60)
        print("リサーチエージェントシステム")
        print("=" * 60)
        print(f"テーマ: {query}\n")

    # Step 1: Orchestrator decides the pipeline
    if verbose:
        print("[Orchestrator] パイプラインを決定中...")
    pipeline = orchestrator.run(query, {})
    if verbose:
        print(f"[Orchestrator] パイプライン: {' → '.join(pipeline)}\n")

    # Step 2: Execute each agent in sequence
    results: dict[str, str] = {}
    current_input = query

    for step in pipeline:
        agent = agent_map.get(step)
        if agent is None:
            if verbose:
                print(f"[警告] 不明なエージェント '{step}' をスキップします。")
            continue

        display_name = AGENT_DISPLAY_NAMES.get(step, step)
        if verbose:
            print(f"[{display_name}] 処理中...")

        if step == "researcher":
            result = researcher.run(query)
        elif step == "fact_checker":
            research_result = results.get("researcher", query)
            result = fact_checker.run(query, research_result)
        elif step == "writer":
            verified = results.get("fact_checker") or results.get("researcher") or query
            result = writer.run(query, verified)
        elif step == "proofreader":
            draft = results.get("writer") or results.get("fact_checker") or query
            result = proofreader.run(query, draft)
        else:
            result = current_input

        results[step] = result
        current_input = result

        if verbose:
            print(f"[{display_name}] 完了 ({len(result)} 文字)\n")

    # The final output is the last agent's result
    final_output = current_input

    if verbose:
        print("=" * 60)
        print("最終記事")
        print("=" * 60)
        print(final_output)

    return final_output


def main() -> None:
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        print("リサーチしたいテーマを入力してください:")
        query = input("> ").strip()
        if not query:
            query = "AIの最新動向について教えてください"

    run_pipeline(query)


if __name__ == "__main__":
    main()
