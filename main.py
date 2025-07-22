import tkinter as tk
from tkinter import ttk
import datetime

class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Current time")
        self.root.geometry("640x480")

        # 見た目の設定
        style = ttk.Style()
        style.configure("TLabel", font=("D-DIN-Bold", 128), background="black", foreground="white")

        # 時刻表示用のラベル
        self.time_label = ttk.Label(root, text="", style="TLabel", anchor="center")
        self.time_label.pack(expand=True, fill="both")

        # ウィンドウを中央に配置
        self.center_window()

        # 1秒おきに時刻を更新
        self.update_time()

    def update_time(self):

        # 現在時刻を取得して整形
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")

        # ラベルのテキストを更新
        self.time_label.config(text=current_time)

        # 1秒後に再びこの関数を呼ぶ
        self.root.after(1000, self.update_time)

    def center_window(self):
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

