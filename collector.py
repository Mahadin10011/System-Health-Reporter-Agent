import psutil, datetime

def collect_metrics():
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "cpu": {
            "percent": psutil.cpu_percent(interval=1),
            "count": psutil.cpu_count(),
            "freq_mhz": psutil.cpu_freq().current
        },
        "memory": {
            "total_gb": round(psutil.virtual_memory().total / 1e9, 2),
            "used_percent": psutil.virtual_memory().percent
        },
        "disk": [
            {
                "mount": p.mountpoint,
                "used_percent": psutil.disk_usage(p.mountpoint).percent
            }
            for p in psutil.disk_partitions() if p.fstype
        ],
        "top_processes": [
            {"name": p.info["name"], "cpu": p.info["cpu_percent"], "ram_mb": round(p.info["memory_info"].rss / 1e6, 1)}
            for p in sorted(psutil.process_iter(["name","cpu_percent","memory_info"]),
                            key=lambda p: p.info["cpu_percent"] or 0, reverse=True)[:5]
        ]
    }

if __name__ == "__main__":
    import json
    print(json.dumps(collect_metrics(), indent=2))
