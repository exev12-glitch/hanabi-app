import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="Hanabi Sim", layout="wide")
st.title("🎇 SHIN HANABI Simulator")

# --- Sidebar ---
with st.sidebar:
    st.header("Settings")
    setting = st.selectbox("Select Setting", ["Setting 1", "Setting 2", "Setting 5", "Setting 6"])
    games = st.slider("Total Games", 1000, 100000, 10000, step=1000)
    
    st.divider()
    executed = st.button("🚀 SIMULATE", use_container_width=True)
    st.write("Push to Start!")

# Spec Data
specs = {
    "Setting 1": {"big": 1/277.7, "reg": 1/356.2, "yield": 1.020},
    "Setting 2": {"big": 1/268.6, "reg": 1/334.3, "yield": 1.040},
    "Setting 5": {"big": 1/260.1, "reg": 1/315.1, "yield": 1.060},
    "Setting 6": {"big": 1/248.2, "reg": 1/287.4, "yield": 1.090},
}

if executed:
    s = specs[setting]
    diff, bc, rc = 0, 0, 0
    h_b, h_max, bh_b, bh_max = 0, 0, 0, 0
    history = [0]
    payback = (3 * s["yield"]) - (202 * s["big"]) - (112 * s["reg"])

    for _ in range(games):
        diff -= 3; h_b += 1; bh_b += 1
        v = random.random()
        if v < s["big"]:
            diff += 202; bc += 1
            h_max = max(h_max, h_b); bh_max = max(bh_max, bh_b)
            h_b = 0; bh_b = 0
        elif v < (s["big"] + s["reg"]):
            diff += 112; rc += 1
            h_max = max(h_max, h_b); h_b = 0
        else:
            diff += payback
        history.append(diff)

    i_bc, i_rc = games * s["big"], games * s["reg"]
    exp_diff = (games * 3 * s["yield"]) - (games * 3)

    # --- Result Display ---
    col1, col2 = st.columns([2, 1])

    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        color = "red" if "1" in setting else "blue" if "2" in setting else "green" if "5" in setting else "purple"
        
        # Plot Graph
        ax.plot(history, color=color, lw=2, label="Actual")
        ax.axhline(0, color="black", lw=1.5) # Zero Line
        ax.axhline(exp_diff, color="orange", ls="--", lw=1.5, label="Expected") # Target Line
        
        # Style
        ax.grid(True, which='both', linestyle='--', alpha=0.5) # 横線（グリッド）追加
        ax.set_xlabel("Games")
        ax.set_ylabel("Payout (Diff)")
        ax.legend()
        st.pyplot(fig)

    with col2:
        st.subheader("📊 Data")
        st.write(f"**BIG:** {bc} (1/{round(games/bc,1) if bc>0 else '---'})")
        st.write(f"**REG:** {rc} (1/{round(games/rc,1) if rc>0 else '---'})")
        st.write(f"**Total:** {bc+rc} (1/{round(games/(bc+rc),1) if bc+rc>0 else '---'})")
        
        st.divider()
        st.subheader("📈 Theory")
        st.write(f"**BIG:** {round(i_bc, 1)}")
        st.write(f"**REG:** {round(i_rc, 1)}")
        
        st.divider()
        st.subheader("⚠️ Max Hamari")
        st.write(f"**Bonus:** {h_max}G")
        st.write(f"**BIG-BIG:** {bh_max}G")
        
        st.divider()
        st.subheader("💰 Profit")
        st.metric("Total Diff", f"{int(diff)} 枚")
        st.write(f"Expected: +{int(exp_diff)} 枚")
        st.write(f"Luck: {int(diff-exp_diff)} 枚")
else:
    st.info("Set parameters and push the button to simulate!")
