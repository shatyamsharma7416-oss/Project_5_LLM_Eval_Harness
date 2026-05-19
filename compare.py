import argparse
import rich
import pathlib
import json
from rich.console import Console
from rich.table import Table

parser = argparse.ArgumentParser()
parser.add_argument("--baseline", required=True)
parser.add_argument("--new", required=True)

console = Console()
table = Table(title="Sample Table")

args = parser.parse_args()
print(args.baseline, args.new)

baseline_location = pathlib.Path(args.baseline)
with open(baseline_location, 'r') as f:
    baseline_summary = json.load(f)

new_location = pathlib.Path(args.baseline)
with open(new_location, 'r') as f:
    new_summary = json.load(f)




table.add_column("Metric", style="cyan")
table.add_column("Baseline", justify="right", style="magenta")
table.add_column("New", style="green")
table.add_column("Delta", style="green")

baseline_semantic_avg = baseline_summary["overall"]
new_semantic_avg = new_summary["overall"]
table.add_row(
    "semantic_avg", f"{baseline_semantic_avg["semantic_avg"]:.2f}", 
    f"{new_semantic_avg["semantic_avg"]:.2f}", 
    f"{(baseline_semantic_avg["semantic_avg"] - new_semantic_avg["semantic_avg"]):.2f}"
    )

table.add_row(
    "pass_rate", f"{baseline_semantic_avg["pass_rate"]:.2f}", 
    f"{new_semantic_avg["pass_rate"]:.2f}", 
    f"{(baseline_semantic_avg["pass_rate"] - new_semantic_avg["pass_rate"]):.2f}"
    )

table.add_row(
    "latency_p95", f"{baseline_summary["latency"]["p95_ms"]:.2f}ms", 
    f"{new_summary["latency"]["p95_ms"]:.2f}ms", 
    f"{(baseline_summary["latency"]["p95_ms"] - new_summary["latency"]["p95_ms"]):.2f}ms"
    )
console.print(table)
