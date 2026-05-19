import json
import urllib.request

def narrate(metrics, flags):
    prompt = f"""You are a system health analyst.

Metrics:
{json.dumps(metrics, indent=2)}

Flags:
{json.dumps(flags, indent=2)}

Write:
1. Overall Status
2. Issues Found
3. Recommended Actions

Be concise and direct."""

    data = json.dumps({
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }).encode()

    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read())
        return result["response"]

if __name__ == "__main__":
    from collector import collect_metrics
    from analyser import analyse, load_config
    metrics = collect_metrics()
    flags = analyse(metrics, load_config())
    print(narrate(metrics, flags))
