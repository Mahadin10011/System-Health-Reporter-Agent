from collector import collect_metrics
from analyser import analyse, load_config
from narrator import narrate
from reporter import write_report, show_windows_popup

print("Collecting metrics...")
metrics = collect_metrics()

print("Analysing...")
flags = analyse(metrics, load_config())

print("Generating narrative...")
narrative = narrate(metrics, flags)

print("Writing report...")
path = write_report(narrative, metrics, flags)

show_windows_popup(flags, metrics, narrative)
print(f"Done. Report saved to {path}")
