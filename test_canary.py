#quick test of canary evaluation
from pathlib import Path
from ashwam_monitor.io.loader import load_parser_outputs, load_gold_labels
from ashwam_monitor.canary.runner import run_canary_evaluation

# load day0 outputs for canary journals
outputs, _ = load_parser_outputs(Path("data/parser_outputs_day0.jsonl"))
gold, _ = load_gold_labels(Path("data/canary/gold.jsonl"))

print(f"parser outputs: {len(outputs)} journals")
print(f"gold labels: {len(gold)} journals")

# filter outputs to only canary journals
canary_ids = {g.journal_id for g in gold}
canary_outputs = [o for o in outputs if o.journal_id in canary_ids]
print(f"canary outputs: {len(canary_outputs)} journals")

report = run_canary_evaluation(canary_outputs, gold)

print(f"\n=== CANARY REPORT ===")
print(f"Precision: {report.precision:.1%}")
print(f"Recall: {report.recall:.1%}")
print(f"F1: {report.f1:.1%}")
print(f"Evidence match rate: {report.evidence_match_rate:.1%}")
print(f"\nMatched: {report.matched_count}, Missed: {report.missed_count}, Extra: {report.extra_count}")
print(f"\nAction: {report.action.value}")
print(f"Reason: {report.action_reason}")

print(f"\nPer journal:")
for j in report.per_journal:
    print(f"  {j.journal_id}: gold={j.gold_count}, parser={j.parser_count}, matched={j.matched}")
