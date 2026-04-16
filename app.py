import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np

# --- ページ設定 ---
st.set_page_config(page_title="新ハナビ シミュレーター", layout="wide")
st.title("🎇 新ハナビ シミュレーター")

# --- サイドバー設定 ---
with st.sidebar:
    st.header("設定項目")
    setting = st.selectbox("設定を選択", ["設定1", "設定2", "設定5", "設定6"])
    games = st.slider("試行ゲーム数", 1000, 100000, 10000, step=1000)
    
    st.divider()
    # 実行ボタン
    executed = st.button("🚀 シミュレート実行", use_container_width=True)
    st.write("ボタンを押すと計算を開始します")

# スペックデータ
specs = {
    "設定1": {"big": 1/277.7, "reg": 1/356.2, "yield": 1.020},
    "設定2": {"big": 1/268.6, "reg": 1/334.3, "yield": 1.040},
    "設定5": {"big": 1/260.1, "reg": 1/315.1, "yield": 1.060},
    "設定6": {"big": 1/248.2, "reg": 1/287.4, "yield": 1.090},
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

    # 理論値の算出
    i_bc = games * s["big"]
    i_rc = games * s["reg"]
    i_total = i_bc + i_rc
    # 理論値の確率（分母）
    p_big = 1 / s["big"]
    p_reg = 1 / s["reg"]
    p_total = 1 / (s["big"] + s["reg"])
    
    exp_diff = (games * 3 * s["yield"]) - (games * 3)

    # --- 画面表示 ---
    col1, col2 = st.columns([2, 1])

    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        color = "red" if "1" in setting else "blue" if "2" in setting else "green" if "5" in setting else "purple"
        ax.plot(history, color=color, lw=1.5)
        ax.axhline(0, color="black", lw=1)
        ax.axhline(exp_diff, color="orange", ls="--", lw=1.2)
        ax.set_xlabel("Games")
        ax.set_ylabel("Diff")
        ax.grid(True, which='both', linestyle='--', alpha=0.5)
        st.pyplot(fig)

    with col2:
        st.subheader("【実戦データ】")
        st.write(f"BIG: {bc}回 (1/{round(games/bc, 1) if bc>0 else '---'})")
        st.write(f"REG: {rc}回 (1/{round(games/rc, 1) if rc>0 else '---'})")
        st.write(f"合算: {bc+rc}回 (1/{round(games/(bc+rc), 1) if bc+rc>0 else '---'})")
        
        st.subheader("【理論値】")
        # --- ここに確率表記を追加 ---
        st.write(f"BIG: {i_bc:.1f}回 (1/{round(p_big, 1)})")
        st.write(f"REG: {i_rc:.1f}回 (1/{round(p_reg, 1)})")
        st.write(f"合算: {i_total:.1f}回 (1/{round(p_total, 1)})")
        
        st.subheader("【ハマり記録】")
        st.write(f"最大ハマり: {h_max}G")
        st.write(f"最大BIG間: {bh_max}G")
