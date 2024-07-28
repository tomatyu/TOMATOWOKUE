import streamlit as st
import pandas as pd
import random

# グローバル変数としてデータフレームを宣言
df = None
selected_country = None  # 現在の問題で選ばれている国名
min_latitude_country = None  # 最小の緯度を持つ国名
options = []  # 選択肢を保持するリスト

# 初期データの読み込み
def load_data():
    global df, min_latitude_country
    df = pd.read_excel("28.xlsx")
    min_latitude_country = df.loc[df['緯度'].idxmin(), '国名']  # 緯度が最小の国を初期設定

# 新しい問題を更新する関数
def update_question():
    global options

    # データから選択肢を設定
    unique_countries = df['国名'].unique()
    other_countries = random.sample([c for c in unique_countries if c != min_latitude_country], 3)
    options = [min_latitude_country] + other_countries
    random.shuffle(options)

    # 問題を更新したことを通知
    st.session_state.message = "新しい問題を更新しました！"
    st.session_state.correct = None  # リセットする

# ユーザーの回答をチェックする関数
def check_answer(answer):
    if answer == min_latitude_country:
        st.session_state.message = "正解！"
        st.session_state.correct = True
    else:
        st.session_state.message = "不正解…"
        st.session_state.correct = False

def main():
    global df, options

    # データがまだ読み込まれていない場合は初回読み込み
    if df is None:
        load_data()

    st.title('国名クイズ')

    # セッション状態にメッセージと正解フラグがない場合は初期化
    if 'message' not in st.session_state:
        st.session_state.message = ''
    if 'correct' not in st.session_state:
        st.session_state.correct = None

    # 問題更新のボタン
    if st.button("問題を更新"):
        update_question()

    # 選択肢がまだ設定されていない場合は初回設定
    if not options:
        update_question()

    # 問題の表示
    st.subheader('以下の国の中から、どれが最も緯度が低い国でしょう？')

    # ボタンを使って選択肢を表示
    cols = st.columns(2)
    for i, option in enumerate(options):
        with cols[i % 2]:
            if st.button(option):
                check_answer(option)

    # メッセージを表示
    if st.session_state.message:
        st.write(st.session_state.message)

if __name__ == '__main__':
    main()
