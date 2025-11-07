import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

def create_architecture_diagram():
    plt.figure(figsize=(11,7))
    ax = plt.gca()
    comps = {
        'ECU\n(Central Brain)': (0.5, 0.75),
        'CAN Bus\nNetwork': (0.5, 0.55),
        'Probe 0x100\nTemp': (0.2, 0.30),
        'Probe 0x101\nPressure': (0.5, 0.30),
        'Probe 0x102\nSpeed': (0.8, 0.30),
    }
    for name,(x,y) in comps.items():
        box = FancyBboxPatch((x-0.12,y-0.06),0.24,0.12, boxstyle="round,pad=0.02",
                             facecolor='lightgray', edgecolor='black')
        ax.add_patch(box)
        ax.text(x,y,name,ha='center',va='center')
    ax.plot([0.5,0.5],[0.69,0.61], 'k-', lw=2)
    ax.plot([0.5,0.2],[0.57,0.36],'k-', lw=2)
    ax.plot([0.5,0.5],[0.57,0.36],'k-', lw=2)
    ax.plot([0.5,0.8],[0.57,0.36],'k-', lw=2)
    ax.annotate('Nonce Broadcast', (0.5,0.62), xytext=(0.7,0.82),
                arrowprops=dict(arrowstyle='->', lw=2))
    ax.annotate('Authenticated Response', (0.3,0.40), xytext=(0.12,0.62),
                arrowprops=dict(arrowstyle='->', lw=2))
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_aspect('equal'); ax.axis('off')
    plt.title("System Architecture: Lightweight Authentication Protocol")
    plt.tight_layout(); plt.savefig("system_architecture.png", dpi=300)
    print("✅ Saved: system_architecture.png")

if __name__ == "__main__":
    create_architecture_diagram()
