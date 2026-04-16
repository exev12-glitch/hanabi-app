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
    executed = st.button("🚀 シミュレート実行", use_container_width=True)

# 詳細スペック（画像解析値）
specs = {
    "設定1": {"big": 1/277.7, "reg": 1/356.2, "bell": 1/7.7, "ice": 1/51.2, "cherry": 1/16.4, "replay": 1/7.3, "yield": 1.02},
    "設定2": {"big": 1/268.6, "reg": 1/334.3, "bell": 1/7.6, "ice": 1/51.8, "cherry": 1/15.3, "replay": 1/7.3, "yield": 1.04},
    "設定5": {"big": 1/260.1, "reg": 1/315.1, "bell": 1/7.5, "ice": 1/48.2, "cherry": 1/16.1, "replay": 1/7.3, "yield": 1.06},
    "設定6": {"big": 1/248.2, "reg": 1/287.4, "bell": 1/7.3, "ice": 1/49.3, "cherry": 1/15.6, "replay": 1/7.3, "yield": 1.09}
}

if executed:
    s = specs[setting]
    diff, bc, rc = 0, 0, 0
    h_b, h_max, bh_b, bh_max = 0, 0, 0, 0
    history = [0]

    for _ in range(games):
        diff -= 3  # 3枚投入
        h_b += 1; bh_b += 1
        v = random.random()
        
        # 1. ボーナス抽選
        if v < s["big"]:
            diff += 202 + 40 # BIG + RT期待値
            bc += 1
            h_max = max(h_max, h_b); bh_max = max(bh_max, bh_b)
            h_b = 0; bh_b = 0
        elif v < (s["big"] + s["reg"]):
            diff += 112 # REG
            rc += 1
            h_max = max(h_max, h_b); h_b = 0
        # 2. 小役抽選
        elif v < (s["big"] + s["reg"] + s["bell"]):
            diff += 8
        elif v < (s["big"] + s["reg"] + s["bell"] + s["ice"]):
            diff += 8
        elif v < (s["big"] + s["reg"] + s["bell"] + s["ice"] + s["cherry"]):
            diff += 4
        elif v < (s["big"] + s["reg"] + s["bell"] + s["ice"] + s["cherry"] + s["replay"]):
            diff += 3 # リプレイ
            
        history.append(diff)

    # 理論値の算出
    i_bc, i_rc = games * s["big"], games * s["reg"]
    i_total = i_bc + i_rc
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
        st.write(f"BIG: {round(i_bc, 1)}回 (1/{round(1/s['big'], 1)})")
        st.write(f"REG: {round(i_rc, 1)}回 (1/{round(1/s['reg'], 1)})")
        st.write(f"合算: {round(i_total, 1)}回 (1/{round(p_total, 1)})")
        
        st.subheader("【ハマり記録】")
        st.write(f"最大ハマり: {h_max}G")
        st.write(f"最大BIG間: {bh_max}G")
        
        st.subheader("【収支】")
        st.metric("現在の差枚", f"{int(diff)} 枚", f"{int(diff-exp_diff)} 枚 (余剰/欠損)")
        st.write(f"期待枚数: +{int(exp_diff)} 枚")

else:
    st.info("設定を確認してシミュレート開始！")
