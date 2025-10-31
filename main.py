import tkinter as tk
from tkinter import ttk
from tkinter import font
import datetime

class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown")
        self.root.geometry("700x520")

        self.bg_color = "#0d1117"
        self.fg_color = "#fdfeff"
        self.primary_color = "#60a5fa"
        self.secondary_color = "#a1a1aa"

        root.config(bg=self.bg_color)

        # 1. ヘッダーラベル (LabelFrameの上)
        self.header_label = tk.Label(
            root,
            text="卒業論文の提出期限まで",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.primary_color,
            pady=10  # 上下のパディングを追加
        )
        self.header_label.pack(pady=(20, 4))

        # 飾り枠 (中央のカウントダウン表示を囲む LabelFrame)
        # reliefをraisedに変更し、背景色を時刻と同じ色にして時刻を際立たせる
        frame = tk.LabelFrame(
            root,
            borderwidth=4,
            relief="raised",
            bg=self.bg_color,
            fg=self.fg_color,
            labelanchor="n" # LabelFrameのラベルを上部に配置
        )
        # fill=tk.BOTHとexpand=Trueで中央のスペースを最大限に利用
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10) 
        
        # 見た目の設定 (時刻表示用)
        style = ttk.Style()
        style.configure(
            "TLabel", 
            font=("Arial", 72, "bold"), 
            background=self.bg_color, 
            foreground=self.fg_color
        )

        # 時刻表示用のラベル
        self.time_label = ttk.Label(frame, text="", style="TLabel", anchor="center")
        self.time_label.pack(expand=True, fill="both")

        # 2. フッターラベル (LabelFrameの下)
        self.footer_label = tk.Label(
            root,
            text="皆様の新たなご知見に触れられますことを心待ちにしております。",
            font=("Arial", 16, "italic"),
            bg=self.bg_color,
            fg=self.secondary_color,
            pady=10 # 上下のパディングを追加
        )
        self.footer_label.pack(pady=(4, 20))


        # ウィンドウを中央に配置
        self.center_window()

        # 1秒おきに時刻を更新
        self.update_time()

    def update_time(self):

        # 現在時刻を取得
        now = datetime.datetime.now()
        # 目標締め切り時刻を設定
        tgt = datetime.datetime(2026, 1, 30, 17, 00, 00) # 例: 2026年1月30日 17:00:00

        if now <= tgt:
            # 締め切りと現在時刻の差を計算 (timedelta)
            td = tgt - now

            # 表示に使う値を計算
            days = td.days
            # .secondsは24時間未満の秒数なので、日数に換算された後の残り時間を計算する
            total_seconds_in_rest = td.seconds
            
            seconds = total_seconds_in_rest % 60
            minutes = (total_seconds_in_rest // 60) % 60
            hours = (total_seconds_in_rest // 3600)

            # ラベルのテキストを更新
            # 日数と時間:分:秒を2行に分けて表示
            self.time_label.config(text=f"{days}日\n{hours:02d}:{minutes:02d}:{seconds:02d}")

            # 1秒後に再びこの関数を呼ぶ
            self.root.after(1000, self.update_time)

        else:
            # 締め切りが過ぎた場合
            self.time_label.config(text="締切!")

    def center_window(self):
        """ウィンドウを画面中央に配置する"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == "__main__":
    root = tk.Tk()
    app = ClockApp(root)
    root.mainloop()
