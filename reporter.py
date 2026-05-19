import pathlib, datetime, ctypes
from plyer import notification

def get_tips(flags):
    tips = []
    for flag in flags:
        metric = flag["metric"]

        if "memory" in metric:
            tips.append("RAM is high — try closing unused browser tabs or apps")
            tips.append("Check Task Manager for memory-hungry processes")
        
        if "cpu" in metric:
            tips.append("CPU is overloaded — avoid running heavy programs simultaneously")
            tips.append("Check for background processes consuming CPU in Task Manager")
        
        if "disk" in metric:
            tips.append(f"{metric} is filling up — delete temp files or empty Recycle Bin")
            tips.append("Run Disk Cleanup to free space quickly")
        
        if "temp" in metric:
            tips.append("System is overheating — reporting will resume once it cools down")
            tips.append("Make sure your vents are not blocked")

    return tips

def show_windows_popup(flags, metrics=None, narrative=None):
    lines = []

    # System metrics summary
    if metrics:
        lines.append("SYSTEM OVERVIEW:")
        lines.append(f"  CPU Usage    : {metrics['cpu']['percent']}%  ({100 - metrics['cpu']['percent']:.1f}% free)")
        lines.append(f"  RAM Usage    : {metrics['memory']['used_percent']}%  ({100 - metrics['memory']['used_percent']:.1f}% free)")
        if metrics['disk']:
            disk = metrics['disk'][0]
            lines.append(f"  Disk ({disk['mount']})  : {disk['used_percent']}%  ({100 - disk['used_percent']:.1f}% free)")
        lines.append("")

    # Flags
    if not flags:
        lines.append("STATUS: All systems healthy. No issues detected.")
    else:
        critical = [f for f in flags if f["severity"] == "critical"]
        warnings = [f for f in flags if f["severity"] == "warning"]

        if critical:
            lines.append("CRITICAL ISSUES:")
            for f in critical:
                lines.append(f"  - {f['metric']} is at {f['value']}%")

        if warnings:
            lines.append("WARNINGS:")
            for f in warnings:
                lines.append(f"  - {f['metric']} is at {f['value']}%")

        tips = get_tips(flags)
        if tips:
            lines.append("")
            lines.append("RECOMMENDED ACTIONS:")
            for tip in tips:
                lines.append(f"  - {tip}")

    # AI narrative
    if narrative:
        lines.append("")
        lines.append("AI REPORT:")
        clean = narrative.replace("**", "").replace("##", "").replace("*", "")
        for line in clean.strip().split("\n"):
            if line.strip():
                lines.append(f"  {line.strip()}")

    message = "\n".join(lines)
    icon = 0x40 | 0x1000

    if flags:
        critical = [f for f in flags if f["severity"] == "critical"]
        icon = (0x10 | 0x1000) if critical else (0x30 | 0x1000)

    ctypes.windll.user32.MessageBoxW(
        0,
        message,
        "System Health Reporter",
        icon
    )

def write_report(narrative, metrics, flags):
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    path = pathlib.Path("reports") / f"health_{ts}.md"
    path.parent.mkdir(exist_ok=True)

    tips = get_tips(flags)
    tips_section = ""
    if tips:
        tips_section = "\n## Recommended Actions\n"
        for tip in tips:
            tips_section += f"- {tip}\n"

    content = f"# System Health Report\n**Generated:** {ts}\n\n{narrative}{tips_section}"
    path.write_text(content, encoding="utf-8")
    print(f"Report written to {path}")
    return path

if __name__ == "__main__":
    from collector import collect_metrics
    from analyser import analyse, load_config
    metrics = collect_metrics()
    flags = analyse(metrics, load_config())
    narrative = "Test narrative."
    path = write_report(narrative, metrics, flags)
    show_windows_popup(flags)
