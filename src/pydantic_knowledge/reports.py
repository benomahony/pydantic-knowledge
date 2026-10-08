from __future__ import annotations

import json
from html import escape
from pathlib import Path

from .evals import cases_from_jobs, run_baselines, ship_gate
from .models import KnowledgeBase


def _pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def write_eval_artifacts(kb: KnowledgeBase, output_dir: str | Path) -> Path:
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    baseline = run_baselines(kb)
    gate = ship_gate(baseline)
    baseline["ship_gate"] = gate

    (root / "routing-cases.json").write_text(
        json.dumps(
            [
                {
                    "name": name,
                    "inputs": inputs.model_dump(mode="json"),
                    "expected": expected.model_dump(mode="json"),
                }
                for name, inputs, expected in cases_from_jobs(kb)
            ],
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (root / "baseline-results.json").write_text(
        json.dumps(baseline, indent=2) + "\n", encoding="utf-8"
    )

    experiments = baseline["experiments"]
    assert isinstance(experiments, dict)
    lines = [
        "# Documentation routing evaluation",
        "",
        "The dataset is generated automatically from the library's Jobs-to-be-Done example phrases.",
        "Pydantic Evals is the canonical experiment harness; these deterministic results are cheap local baselines.",
        "",
        "| Experiment | Route@1 | Hit@3 | Answer assertions |",
        "|---|---:|---:|---:|",
    ]
    for name, result in experiments.items():
        lines.append(
            f"| {name} | {_pct(result['route_at_1'])} | {_pct(result['hit_at_3'])} | {_pct(result['answer_assertions'])} |"
        )
    lines += [
        "",
        f"## Ship gate: `{gate['decision']}`",
        "",
        str(gate["reason"])
        if "reason" in gate
        else "Compare the AI experiment against the strongest deterministic baseline.",
        "",
        "The AI router should only ship if it improves Route@1 by the configured margin without regressing Hit@3.",
    ]
    (root / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    cards = []
    for name, result in experiments.items():
        cards.append(
            f"""<article class="metric"><h3>{escape(name)}</h3><div class="big">{_pct(result["route_at_1"])}</div><p>Route@1</p><div class="sub">Hit@3 {_pct(result["hit_at_3"])} · answer assertions {_pct(result["answer_assertions"])}</div></article>"""
        )
    rows = []
    first_name = next(iter(experiments))
    for row in experiments[first_name]["cases"]:
        rows.append(
            "<tr>"
            f"<td><strong>{escape(row['name'])}</strong><br><span>{escape(row['job_id'])}</span></td>"
            f"<td>{escape(row['phrase'])}</td>"
            f"<td>{escape(', '.join(row['expected']))}</td>"
            f"<td>{escape(', '.join(row['suggested']))}</td>"
            f"<td class={'pass' if row['route_at_1'] else 'fail'}>{'PASS' if row['route_at_1'] else 'FAIL'}</td>"
            "</tr>"
        )
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Docs routing evals</title>
<style>:root{{--ink:#061314;--paper:#FBFFEA;--accent:#E520E9;--line:#dce3e1;--muted:#61706f}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 Inter,system-ui,sans-serif}}main{{max-width:1180px;margin:auto;padding:38px 28px}}h1{{font-size:38px;margin-bottom:8px}}.lead{{color:var(--muted);max-width:780px}}.gate{{margin:28px 0;padding:18px;border:1px solid var(--line);border-left:5px solid var(--accent);background:#fff;border-radius:10px}}.metrics{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}}.metric{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px}}.metric h3{{margin:0;font-size:14px}}.big{{font-size:34px;font-weight:800;margin-top:10px}}.metric p,.sub{{color:var(--muted);margin:0}}.sub{{font-size:12px;margin-top:8px}}table{{width:100%;border-collapse:collapse;background:#fff;margin-top:24px;border:1px solid var(--line)}}th,td{{padding:11px 12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}}th{{font-size:12px;text-transform:uppercase;color:var(--muted)}}td span{{font-size:12px;color:var(--muted)}}.pass{{color:#176b3a;font-weight:800}}.fail{{color:#a12c35;font-weight:800}}code{{background:#f3f5f4;padding:2px 5px;border-radius:5px}}</style></head>
<body><main><div style="color:#8c178f;font-weight:800;text-transform:uppercase;font-size:12px;letter-spacing:.08em">Pydantic Knowledge · Evals</div><h1>Does realtime AI earn its place?</h1><p class="lead">Jobs-to-be-Done example phrases become evaluation cases automatically. Every router gets the same inputs, expected documentation concepts, and answer assertions.</p><section class="gate"><strong>{escape(str(gate["decision"]))}</strong><p>{escape(str(gate.get("reason", "The AI experiment must beat the strongest deterministic baseline before it ships.")))}</p></section><section class="metrics">{"".join(cards)}</section><h2>Cases</h2><p class="lead">The table below shows the first deterministic experiment; switch experiments in the JSON output or run the native Pydantic Evals experiment for full evaluator detail.</p><table><thead><tr><th>Case</th><th>User phrase</th><th>Expected docs</th><th>Suggested docs</th><th>Route@1</th></tr></thead><tbody>{"".join(rows)}</tbody></table></main></body></html>"""
    (root / "dashboard.html").write_text(html, encoding="utf-8")
    return root
