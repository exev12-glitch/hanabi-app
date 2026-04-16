import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np

# --- ページ設定 ---
st.set_page_config(page_title="新ハナビ シミュレーター", layout="wide")
st.title("🎇 新ハナビ シミュレーター")

# --- フォントの文字化け対策（日本語対応） ---
# Streamlitの標準環境で日本語を表示するための設定
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans'] # 標準フォントを使用

# --- サイドバー設定 ---
with st.sidebar:
    st.header("設定項目")
    setting = st.selectbox("設定を選択", ["設定1", "設定2", "設定5", "設定6"])
    games = st.slider("試行ゲーム数", 1000, 100000, 10000, step=1000)
    
    st.divider()
    # --- 実行ボタン ---
    executed = st.button("🚀 シミュレート実行", use_container_width=True)
    st.write("ボタンを押すと計算を開始します")

# スペックデータ
specs = {
    "設定1": {"big": 1/277.7, "reg": 1/356.2, "yield": 1.020},
    "設定2": {"big": 1/268.6, "reg": 1/334.3, "yield": 1.040},
    "設定5": {"big": 1/260.1, "reg": 1/315.1, "yield": 1.060},
    "設定6": {"big": 1/248.2, "reg": 1/287.4, "yield": 1.090},
}

# ボタンが押されたときだけ実行
if executed:
    s = specs[setting]
    diff, bc, rc = 0, 0, 0
    h_b, h_max, bh_b, bh_max = 0, 0, 0, 0
    history = [0]
    # 出玉率から逆算した小役等のベース
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
    exp_diff = (games * 3 * s["yield"]) - (games * 3)

    # --- 画面表示 ---
    col1, col2 = st.columns([2, 1])

    with col1:
        # グラフ作成
        fig, ax = plt.subplots(figsize=(10, 6))
        color = "red" if "1" in setting else "blue" if "2" in setting else "green" if "5" in
