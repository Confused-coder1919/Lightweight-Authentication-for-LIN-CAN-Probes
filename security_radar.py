import numpy as np
import matplotlib.pyplot as plt

def create_security_radar():
    cats = ['Replay', 'Spoofing', 'Integrity', 'Freshness', 'Eavesdrop']
    your = [100,100,100,100,85]
    std  = [90,85,95,80,70]
    none = [0,0,15,0,0]

    labels = cats + [cats[0]]
    def close(vals): return vals + [vals[0]]

    angles = np.linspace(0, 2*np.pi, len(labels))

    plt.figure(figsize=(8,8))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, close(your), linewidth=2)
    ax.fill(angles, close(your), alpha=0.2)
    ax.plot(angles, close(std), linewidth=2)
    ax.plot(angles, close(none), linewidth=2)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(cats)
    ax.set_ylim(0,100)
    plt.title("Security Feature Comparison")
    plt.tight_layout()
    plt.savefig("security_radar.png", dpi=300)
    print("✅ Saved: security_radar.png")

if __name__ == "__main__":
    create_security_radar()
