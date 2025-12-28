#quick test of drift metrics
from pathlib import Path
from ashwam_monitor.io.loader import load_parser_outputs
from ashwam_monitor.metrics.comparator import run_drift_analysis

baseline, _ = load_parser_outputs(Path("data/parser_outputs_day0.jsonl"))
current, _ = load_parser_outputs(Path("data/parser_outputs_day1.jsonl"))

print(f"baseline: {len(baseline)} journals")
print(f"current: {len(current)} journals")

report = run_drift_analysis(baseline, current, "day0", "day1")

print(f"\n=== DRIFT REPORT ===")
for m in report.metrics:
    print(f"{m.name}: {m.baseline_value} -> {m.current_value} ({m.change_pct:+.1f}%) [{m.status.value}]")
    if m.js_divergence:
        print(f"  JSD: {m.js_divergence}")

print(f"\nAlerts ({len(report.alerts)}):")
for a in report.alerts:
    print(f"  {a}")
