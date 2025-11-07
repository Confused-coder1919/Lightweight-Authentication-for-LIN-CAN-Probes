import matplotlib.pyplot as plt
import numpy as np

def bar_with_labels(title, ylabel, cats, vals, yscale=None, fmt=None, outfile="out.png"):
    plt.figure(figsize=(8,6))
    x = np.arange(len(cats))
    bars = plt.bar(x, vals)
    if yscale: plt.yscale(yscale)
    for i,b in enumerate(bars):
        h = b.get_height()
        label = f"{h:.3f}{fmt}" if fmt else (f"{h:.0f}" if h>=10 else f"{h}")
        plt.text(b.get_x()+b.get_width()/2, h, label, ha="center", va="bottom")
    plt.xticks(x, cats, rotation=10)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outfile, dpi=300)

def create_all():
    cats = ['Your Solution', 'Automotive Req', 'Traditional Crypto']
    latency = [0.048, 10, 5.2]              # ms
    throughput = [481132, 4000, 85000]      # msg/s
    security_score = [100, 100, 95]         # %
    cost_impact = [0, 0, 0.50]              # $

    bar_with_labels("Authentication Latency (lower is better)", "ms", cats, latency,
                    yscale="log", fmt="ms", outfile="performance_latency.png")
    bar_with_labels("Message Throughput (higher is better)", "msg/s", cats, throughput,
                    yscale="log", outfile="performance_throughput.png")
    bar_with_labels("Security Score", "%", cats, security_score,
                    outfile="performance_security.png")
    bar_with_labels("Hardware Cost Impact (lower is better)", "$/probe", cats, cost_impact,
                    outfile="performance_cost.png")
    print("✅ Saved: performance_latency.png, performance_throughput.png, performance_security.png, performance_cost.png")

if __name__ == "__main__":
    create_all()
