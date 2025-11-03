import tkinter as tk
from tkinter import ttk
from tkinter import font
import datetime

class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown")
        self.root.geometry("720x720") 

        self.bg_color = "#0d1117"
        self.fg_color = "#fdfeff"
        self.primary_color = "#60a5fa"
        self.secondary_color = "#a1a1aa"

        root.config(bg=self.bg_color)

        # ヘッダーラベル
        self.header_label = tk.Label(
            root,
            text="卒業論文の提出期限まで",
            font=("Arial", 28, "bold"), 
            bg=self.bg_color,
            fg=self.primary_color,
            pady=15
        )
        self.header_label.pack(pady=(30, 8))

        # 中央のカウントダウン表示エリア (Canvas)
        self.canvas = tk.Canvas(
            root,
            bg=self.bg_color,
            highlightthickness=0
        )
        # fill=tk.BOTHとexpand=Trueで中央のスペースを最大限に利用
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=50, pady=10) 
        
        # キャンバスのサイズ変更時に図形を再描画
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        
        # カスタムシェイプ描画用の変数
        self.scallop_radius = 50
        self.text_window_id = None
        
        # 見た目の設定 (時刻表示用)
        style = ttk.Style()
        # カウントダウンのちらつきを防ぐため、等幅フォントを設定
        self.countdown_font = ("Courier New", 72, "bold")
        style.configure(
            "TLabel", 
            font=self.countdown_font, 
            background=self.bg_color, 
            foreground=self.fg_color
        )

        # 時刻表示用のラベル
        self.time_label = ttk.Label(self.canvas, text="", style="TLabel", anchor="center")
        # ラベルは一旦packせず、create_windowで中央に配置します

        # 2. フッターラベル
        self.footer_label = tk.Label(
            root,
            text="皆様の新たなご知見に触れられますことを心待ちにしております。",
            font=("Arial", 16, "italic"),
            bg=self.bg_color,
            fg=self.secondary_color,
            pady=15
        )
        self.footer_label.pack(pady=(8, 30))


        # ウィンドウを中央に配置
        self.center_window()

        # 飾り枠を描画
        self.root.after(100, self._draw_scalloped_rectangle)

        # 1秒おきに時刻を更新
        self.update_time()

    def _draw_scalloped_rectangle(self):
        """キャンバスに凹角の四角形を描画し、ラベルを中央に配置する"""
        
        # 既存の図形を全て削除
        self.canvas.delete("scallop_shape")
        
        # キャンバスの現在のサイズを取得
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        r = self.scallop_radius
        
        # 描画エリア (x1, y1) - (x2, y2)
        x1, y1 = 2, 2
        x2, y2 = w - 2, h - 2

        outline_color = self.primary_color
        line_width = 4

        # メインの矩形部分を描画

        self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.bg_color, outline="", tags="scallop_shape")
        
        # 4つの角に背景色と同じ色の円弧 (PIESLICE) を描画し、矩形の角を削り取ります
        bg_fill_color = self.root['bg']
        
        # Bounding Box: (x_start, y_start) to (x_end, y_end)
        
        # 左上 (Center: x1, y1 + r) - 穴の中心
        self.canvas.create_arc(
            x1, y1, x1 + 2*r, y1 + 2*r, 
            start=180, extent=90, 
            style=tk.PIESLICE, 
            fill=bg_fill_color, 
            outline=bg_fill_color, 
            tags="scallop_shape"
        )
        
        # 右上
        self.canvas.create_arc(
            x2 - 2*r, y1, x2, y1 + 2*r,
            start=270, extent=90, 
            style=tk.PIESLICE, 
            fill=bg_fill_color, 
            outline=bg_fill_color, 
            tags="scallop_shape"
        )
        
        # 右下
        self.canvas.create_arc(
            x2 - 2*r, y2 - 2*r, x2, y2,
            start=0, extent=90, 
            style=tk.PIESLICE, 
            fill=bg_fill_color, 
            outline=bg_fill_color, 
            tags="scallop_shape"
        )
        
        # 左下
        self.canvas.create_arc(
            x1, y2 - 2*r, x1 + 2*r, y2,
            start=90, extent=90, 
            style=tk.PIESLICE, 
            fill=bg_fill_color, 
            outline=bg_fill_color, 
            tags="scallop_shape"
        )


        # 境界線を描画
        
        # 4辺の直線
        self.canvas.create_line(x1 + r, y1, x2 - r, y1, fill=outline_color, width=line_width, tags="scallop_shape") # 上
        self.canvas.create_line(x2, y1 + r, x2, y2 - r, fill=outline_color, width=line_width, tags="scallop_shape") # 右
        self.canvas.create_line(x2 - r, y2, x1 + r, y2, fill=outline_color, width=line_width, tags="scallop_shape") # 下
        self.canvas.create_line(x1, y2 - r, x1, y1 + r, fill=outline_color, width=line_width, tags="scallop_shape") # 左
        
        # 4つの角の凹面 (Concave Arcs) - 角度を修正
        # 円弧の中心は角の座標(x1, y1, x2, y2)、半径r
        
        # 左上
        self.canvas.create_arc(
            x1 - r, y1 - r, x1 + r, y1 + r,
            start=270, extent=90, style=tk.ARC, outline=outline_color, width=line_width, tags="scallop_shape"
        )

        # 右上
        self.canvas.create_arc(
            x2 - r, y1 - r, x2 + r, y1 + r,
            start=180, extent=90, style=tk.ARC, outline=outline_color, width=line_width, tags="scallop_shape"
        )
        
        # 右下
        self.canvas.create_arc(
            x2 - r, y2 - r, x2 + r, y2 + r,
            start=90, extent=90, style=tk.ARC, outline=outline_color, width=line_width, tags="scallop_shape"
        )
        
        # 左下
        self.canvas.create_arc(
            x1 - r, y2 - r, x1 + r, y2 + r,
            start=0, extent=90, style=tk.ARC, outline=outline_color, width=line_width, tags="scallop_shape"
        )

        # ラベルをキャンバスの中央に配置または再配置
        if self.text_window_id:
            # 既存の場合は座標を更新
            self.canvas.coords(self.text_window_id, w/2, h/2)
        else:
            # 初回の場合は作成
            self.text_window_id = self.canvas.create_window(
                w/2, h/2, window=self.time_label, anchor="center"
            )

    def _on_canvas_resize(self, event):
        """キャンバスがリサイズされたときに図形を再描画する"""
        # ちらつきを抑える
        self.root.after(10, self._draw_scalloped_rectangle)

    def update_time(self):

        # 現在時刻を取得
        now = datetime.datetime.now()
        # 目標締め切り時刻を設定
        # 2026年1月30日 17:00:00 (元の設定を維持)
        tgt = datetime.datetime(2026, 1, 30, 17, 00, 00) 

        if now <= tgt:
            # 締め切りと現在時刻の差を計算 (timedelta)
            td = tgt - now

            # 表示に使う値を計算
            days = td.days
            # .secondsは24時間未満の秒数なので、日数に換算された後の残り時間を計算する
            total_seconds_in_rest = td.seconds
            
            seconds = total_seconds_in_rest % 60
            minutes = (total_seconds_in_rest // 60) % 60
            hours = (total_seconds_in_rest // 3600) # 総時間を計算 (24時間を超える)

            # ラベルのテキストを更新
            # 日数と時分秒の間にスペースを空けることで、視認性を高めます
            self.time_label.config(text=f"{days}日\n{hours:02d}:{minutes:02d}:{seconds:02d}")

            # 1秒後に再びこの関数を呼ぶ
            self.root.after(1000, self.update_time)

        else:
            # 締め切りが過ぎた場合
            self.time_label.config(text="締切!", foreground="#ff5555")
            # 飾り枠の色を赤に変更
            self.canvas.itemconfig("scallop_shape", outline="#ff5555")

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
