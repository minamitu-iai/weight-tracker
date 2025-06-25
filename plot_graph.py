import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def generate_graph():
    """
    CSVファイルから体重データを読み込み、グラフを生成して画像として保存する関数
    """
    try:
        # CSVファイルを読み込む
        # 'date'列を日付として解釈するように指定
        df = pd.read_csv('Record.csv', parse_dates=['date'])

        # データを日付で並べ替える（念のため）
        df = df.sort_values(by='date')

        # グラフのプロット設定
        fig, ax = plt.subplots(figsize=(10, 6))

        # 折れ線グラフをプロット
        ax.plot(df['date'], df['weight'], marker='o', linestyle='-', color='b')

        # グラフの装飾
        ax.set_title('Weight Fluctuation', fontsize=16)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Weight (kg)', fontsize=12)
        ax.grid(True)

        # X軸の日付フォーマットを設定
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        fig.autofmt_xdate() # 日付が重ならないように自動調整

        # グラフを画像ファイルとして保存する
        # bbox_inches='tight'は、タイトルやラベルが画像外に切れないようにする設定
        plt.savefig('weight_graph.png', bbox_inches='tight')

        print("グラフが正常に生成され、'weight_graph.png'として保存されました。")

    except FileNotFoundError:
        print("エラー: 'weight.csv'が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    generate_graph()
