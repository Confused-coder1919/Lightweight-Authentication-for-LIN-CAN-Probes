import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, ConnectionPatch

def protocol_flow():
    fig, ax = plt.subplots(figsize=(12,8))
    ax.set_title("Lightweight Authentication Protocol Flow")
    ecu = (0.5,0.8); bus = (0.5,0.6); probes = [(0.2,0.3),(0.5,0.3),(0.8,0.3)]
    def box(x,y,w=0.24,h=0.12,label=""):
        b = FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02",
                           facecolor="lightgray", edgecolor="black")
        ax.add_patch(b); ax.text(x,y,label,ha='center',va='center')
    box(*ecu,label="Central ECU\n(Security Master)")
    ax.plot([0.1,0.9],[bus[1],bus[1]],'k-',lw=3); ax.text(0.5,bus[1]+0.025,"CAN Bus",ha='center')
    for i,(x,y) in enumerate(probes):
        box(x,y,label=f"Sensor {i}\nID: 0x10{i}")
    arr = ConnectionPatch((0.5,0.75),(0.5,0.65),"data","data",
                          arrowstyle="->", mutation_scale=20, lw=1.5)
    ax.add_patch(arr); ax.text(0.52,0.72,"Nonce Broadcast")
    arr2 = ConnectionPatch((0.3,0.35),(0.3,0.55),"data","data",
                           arrowstyle="->", mutation_scale=20, lw=1.5)
    ax.add_patch(arr2); ax.text(0.18,0.46,"Auth Message")
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_aspect('equal'); ax.axis('off')
    plt.tight_layout(); plt.savefig("protocol_flow_detailed.png", dpi=300)
    print("✅ Saved: protocol_flow_detailed.png")

def attack_prevention():
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(14,6))
    fig.suptitle("Attack Prevention Mechanisms")

    ax1.set_title("Replay Attack Prevention"); ax1.axis('off')
    ax1.text(0.5,0.8,"Replay Old Message",ha='center',va='center',
             bbox=dict(boxstyle="round", fc="lightgray"))
    ax1.arrow(0.5,0.7,0,-0.2, head_width=0.03, length_includes_head=True)
    ax1.text(0.5,0.4,"ECU checks sequence\nMESSAGE REJECTED",
             ha='center',va='center', bbox=dict(boxstyle="round", fc="lightgray"))

    ax2.set_title("Spoofing Attack Prevention"); ax2.axis('off')
    ax2.text(0.5,0.8,"Fake Message",ha='center',va='center',
             bbox=dict(boxstyle="round", fc="lightgray"))
    ax2.arrow(0.5,0.7,0,-0.2, head_width=0.03, length_includes_head=True)
    ax2.text(0.5,0.4,"ECU verifies MAC\nINVALID → REJECTED",
             ha='center',va='center', bbox=dict(boxstyle="round", fc="lightgray"))

    plt.tight_layout(); plt.savefig("attack_prevention.png", dpi=300)
    print("✅ Saved: attack_prevention.png")

if __name__ == "__main__":
    protocol_flow()
    attack_prevention()
