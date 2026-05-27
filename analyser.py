import json

def load_config():
    with open("config.json") as f:
        return json.load(f)

def analyse(metrics, config):
    flags = []
    if metrics["cpu"]["percent"] > config["cpu_warn"]:
        flags.append({"severity": "warning", "metric": "cpu", "value": metrics["cpu"]["percent"]})
    if metrics["memory"]["used_percent"] > config["mem_warn"]:
        flags.append({"severity": "critical", "metric": "memory", "value": metrics["memory"]["used_percent"]})
    for disk in metrics["disk"]:
        if disk["used_percent"] > config["disk_warn"]:
            flags.append({"severity": "warning", "metric": f"disk {disk['mount']}", "value": disk["used_percent"]})
    return flags

def report(flags):
    for flag in flags:
        print(f"{flag['severity']}: {flag['metric']} {flag['value']}")

if __name__ == "__main__":
    import json
    from collector import collect_metrics
    metrics = collect_metrics()
    flags = analyse(metrics, load_config())
    print(json.dumps(flags, indent=2))
    report(flags)
    print(json.dumps(metrics, indent=2))
