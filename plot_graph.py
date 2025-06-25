import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def generate_graph():
    """
    CSVファイルから体重データを読み込み、ボリンジャーバンド付きのグラフを生成して
    画像として保存する関数
    """
    try:
        # CSVファイルを読み込む (前回の手順でファイル名は修正済みと仮定)
        # もしファイル名が違う場合は、 'Record.csv' の部分を修正してください
        df = pd.read_csv('Record.csv', parse_dates=['date'])
        df = df.sort_values(by='date')

        # --- ボリンジャーバンドの計算 ---
        # パラメータ設定 (自由に変更可能です)
        window = 20  # 移動平均の期間
        num_std_dev = 2  # 標準偏差の倍数

        # 移動平均 (MA) を計算
        df['MA'] = df['weight'].rolling(window=window).mean()
        # 標準偏差 (STD) を計算
        df['STD'] = df['weight'].rolling(window=window).std()

        # アッパーバンドとロワーバンドを計算
        df['Upper'] = df['MA'] + (df['STD'] * num_std_dev)
        df['Lower'] = df['MA'] - (df['STD'] * num_std_dev)
        # -----------------------------

        # グラフのプロット設定
        fig, ax = plt.subplots(figsize=(12, 7))

        # --- グラフの描画 ---
        # 1. 体重の折れ線グラフ (メインのデータ)
        ax.plot(df['date'], df['weight'], marker='o', linestyle='-', color='blue', label='Weight', zorder=3)
        
        # 2. 移動平均線
        ax.plot(df['date'], df['MA'], linestyle='--', color='orange', label=f'{window}-Day MA', zorder=4)

        # 3. ボリンジャーバンド
        #    アッパーバンドとロワーバンドの間を塗りつぶす
        ax.fill_between(df['date'], df['Lower'], df['Upper'], color='gray', alpha=0.3, label='Bollinger Bands')
        # -----------------------------

        # グラフの装飾
        ax.set_title('Weight Fluctuation with Bollinger Bands', fontsize=16)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Weight (kg)', fontsize=12)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend() # 凡例を表示

        # X軸の日付フォーマットを設定
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        fig.autofmt_xdate()

        # グラフを画像ファイルとして保存する
        plt.savefig('weight_graph.png', bbox_inches='tight')

        print("ボリンジャーバンド付きのグラフが正常に生成され、'weight_graph.png'として保存されました。")

    except FileNotFoundError:
        print("エラー: CSVファイルが見つかりません。ファイル名を確認してください。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    generate_graph()
