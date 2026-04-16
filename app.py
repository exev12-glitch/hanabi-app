import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np

# --- ページ設定 ---
st.set_page_config(page_title="新ハナビ シミュレーター", layout="wide")
st.title("🎇 新ハナビ シミュレーター")

# 計算結果を保存する箱を作る
if 'results' not in st.session_state:
    st.session_state.results = None

# --- サイドバー設定 ---
with st.sidebar:
    st.header("設定項目")
    setting = st.selectbox("設定を選択", ["設定1", "設定2", "設定5", "設定6"])
    games = st.slider("試行ゲーム数", 1000, 100000, 10000, step=1000)
    st.divider()
    if st.button("🚀 シミュレート実行", use_container_width=True):
        # ボタンが押されたら計算を実行し、結果をsession_stateに保存
        s = {"設定1": {"big": 1/277.7, "reg": 1/356.2, "bell": 1/7.7, "ice": 1/51.2, "cherry": 1/16.4, "replay": 1/7.3, "yield": 1.02},
             "設定2": {"big": 1/268.6, "reg": 1/334.3, "bell": 1/7.6, "ice": 1/51.8, "cherry": 1/15.3, "replay": 1/7.3, "yield": 1.04},
             "設定5": {"big": 1/260.1, "reg": 1/315.1, "bell": 1/7.5, "ice": 1/48.2, "cherry": 1/16.1, "replay": 1/7.3, "yield": 1.06},
             "設定6": {"big": 1/248.2, "reg": 1/287.4, "bell": 1/7.3, "ice": 1/49.3, "cherry": 1/15.6, "replay": 1/7.3, "yield": 1.09}}[setting]
        
        diff, bc, rc, h_b, h_max, bh_b, bh_max, history = 0, 0, 0, 0, 0, 0, 0, [0]
        for _ in range(games):
            diff -= 3; h_b += 1; bh_b += 1
            v = random.random()
            if v < s["big"]: diff += 242; bc += 1; h_max=max(h_max, h_b); bh_max=max(bh_max, bh_b); h_b=0; bh_b=0
            elif v < (s["big"] + s["reg"]): diff += 112; rc += 1; h_max=max(h_max, h_b); h_b=0
            elif v < (s["big"] + s["reg"] + s["bell"]): diff += 8
            elif v < (s["big"] + s["reg"] + s["bell"] + s["ice"]): diff += 8
            elif v < (s["big"] + s["reg"] + s["bell"] + s["ice"] + s["cherry"]): diff += 4
            elif v < (s["big"] + s["reg"] + s["bell"] + s["ice"] + s["cherry"] + s["replay"]): diff += 3
            history.append(diff)
            
        st.session_state.results = {
            "setting": setting, "games": games, "diff": diff, "bc": bc, "rc": rc, 
            "h_max": h_max, "bh_max": bh_max, "history": history, "s": s
        }

# --- 画面表示（保存されたデータがあれば表示） ---
if st.session_state.results:
    res = st.session_state.results
    s, bc, rc, diff = res["s"], res["bc"], res["rc"], res["diff"]
    i_bc, i_rc = res["games"] * s["big"], res["games"] * s["reg"]
    exp_diff = (res["games"] * 3 * s["yield"]) - (res["games"] * 3)

    col1, col2 = st.columns([2, 1])
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(res["history"], lw=1.5)
        ax.axhline(0, color="black", lw=1); ax.axhline(exp_diff, color="orange", ls="--", lw=1.2)
        ax.grid(True, linestyle='--', alpha=0.5); st.pyplot(fig)
    with col2:
        st.subheader("【実戦データ】")
        st.write(f"BIG: {bc}回 (1/{round(res['games']/bc, 1) if bc>0 else '---'})")
        st.write(f"REG: {rc}回 (1/{round(res['games']/rc, 1) if rc>0 else '---'})")
        st.write(f"合算: {bc+rc}回 (1/{round(res['games']/(bc+rc), 1) if bc+rc>0 else '---'})")
        st.subheader("【理論値】")
        st.write(f"BIG: {round(i_bc, 1)}回 (1/{round(1/s['big'], 1)})")
        st.write(f"REG: {round(i_rc, 1)}回 (1/{round(1/s['reg'], 1)})")
        st.write(f"合算: {round(i_total, 1)}回 (1/{round(p_total, 1)})")
        st.subheader("【収支】")
        st.metric("現在の差枚", f"{int(diff)} 枚", f"{int(diff-exp_diff)} 枚 (余剰/欠損)")
else:
    st.info("サイドバーで設定を選び「シミュレート実行」ボタンを押してください。")
