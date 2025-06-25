import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def generate_graph():
    """
    CSVから体重と体脂肪率を読み込み、詳細な分析が可能な2段のグラフを生成する。
    - 7日 & 21日移動平均
    - 21日ボリンジャーバンド
    - トレンド線を強調したカラーリング
    """
    try:
        # --- 1. パラメータと色の設定 ---
        # 計算パラメータ
        window_short = 7   # 短期移動平均の期間
        window_long = 21   # 長期移動平均 & ボリンジャーバンドの期間
        num_std_dev = 2    # ボリンジャーバンドの標準偏差の倍数

        # カラー設定
        color_actual = 'lightgray'       # 実測値の色 (目立たなくする)
        color_ma_short = '#ff7f0e'       # 7日移動平均の色 (オレンジ系)
        color_ma_long = '#9467bd'        # 21日移動平均の色 (紫系)
        color_bollinger = 'gray'         # ボリンジャーバンドの塗りつぶし色

        # --- 2. データの読み込みと計算 ---
        df = pd.read_csv('Record.csv', parse_dates=['date'])
        df = df.sort_values(by='date')

        # 体重データの計算
        df['MA_weight_short'] = df['weight'].rolling(window=window_short).mean()
        df['MA_weight_long'] = df['weight'].rolling(window=window_long).mean()
        df['STD_weight'] = df['weight'].rolling(window=window_long).std()
        df['Upper_weight'] = df['MA_weight_long'] + (df['STD_weight'] * num_std_dev)
        df['Lower_weight'] = df['MA_weight_long'] - (df['STD_weight'] * num_std_dev)

        # 体脂肪率データの計算
        df['MA_fat_short'] = df['fat'].rolling(window=window_short).mean()
        df['MA_fat_long'] = df['fat'].rolling(window=window_long).mean()
        df['STD_fat'] = df['fat'].rolling(window=window_long).std()
        df['Upper_fat'] = df['MA_fat_long'] + (df['STD_fat'] * num_std_dev)
        df['Lower_fat'] = df['MA_fat_long'] - (df['STD_fat'] * num_std_dev)
        
        # --- 3. グラフの描画 ---
        fig, axs = plt.subplots(2, 1, figsize=(14, 12), sharex=True)
        fig.suptitle('Full Analysis: Weight & Body Fat', fontsize=20)

        # 上の段：体重グラフ
        axs[0].plot(df['date'], df['weight'], marker='.', linestyle='-', color=color_actual, label='Weight (kg)', zorder=1)
        axs[0].plot(df['date'], df['MA_weight_short'], linestyle='-', color=color_ma_short, label=f'{window_short}-Day MA', zorder=3)
        axs[0].plot(df['date'], df['MA_weight_long'], linestyle='--', color=color_ma_long, label=f'{window_long}-Day MA', zorder=4)
        axs[0].fill_between(df['date'], df['Lower_weight'], df['Upper_weight'], color=color_bollinger, alpha=0.2, label='Bollinger Bands')
        axs[0].set_ylabel('Weight (kg)')
        axs[0].grid(True, which='both', linestyle='--', linewidth=0.5)
        axs[0].legend()

        # 下の段：体脂肪率グラフ
        axs[1].plot(df['date'], df['fat'], marker='.', linestyle='-', color=color_actual, label='Body Fat (%)', zorder=1)
        axs[1].plot(df['date'], df['MA_fat_short'], linestyle='-', color=color_ma_short, label=f'{window_short}-Day MA', zorder=3)
        axs[1].plot(df['date'], df['MA_fat_long'], linestyle='--', color=color_ma_long, label=f'{window_long}-Day MA', zorder=4)
        axs[1].fill_between(df['date'], df['Lower_fat'], df['Upper_fat'], color=color_bollinger, alpha=0.2, label='Bollinger Bands')
        axs[1].set_ylabel('Body Fat (%)')
        axs[1].set_xlabel('Date')
        axs[1].grid(True, which='both', linestyle='--', linewidth=0.5)
        axs[1].legend()

        # --- 4. 仕上げ ---
        fig.autofmt_xdate()
        fig.tight_layout(rect=[0, 0.03, 1, 0.97])
        plt.savefig('weight_graph.png', bbox_inches='tight')
        
        print("高機能分析グラフが正常に生成されました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    generate_graph()
