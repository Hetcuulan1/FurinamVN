import customtkinter as ctk
import os
import webbrowser
import configparser
from tkinter import messagebox
import psutil
import threading
import time
from tkinter import filedialog

# ------------------ Giao diện chính ------------------ #
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Funeuam App")
app.geometry("480x480")
app.resizable(False, False)
app.iconbitmap("Assest\\icon.ico")

title_label = ctk.CTkLabel(app, text="Funeuam client", font=("HYWenHei 85W", 20))
title_label.pack(pady=15)

# ------------------ Đọc file INI ------------------ #
config = configparser.ConfigParser()
config.read("Data\\Data.ini")

def get_game_path():
    return config.get("Game", "PathGame", fallback=None)

# ------------------ Theo dõi process ------------------ #
def is_game_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == "GenshinImpact.exe":
            return True
    return False

# ------------------ Tạo cửa sổ đang chạy ------------------ #
def show_loading_window():
    loading_win = ctk.CTkToplevel()
    loading_win.title("Đang chạy Game")
    loading_win.geometry("250x100")
    loading_win.resizable(False, False)
    ctk.CTkLabel(loading_win, text="Đang chạy Game...", font=("HYWenHei 85W", 16)).pack(pady=30)
    loading_win.protocol("WM_DELETE_WINDOW", lambda: None)  # Vô hiệu hóa nút đóng

    # Thread theo dõi
    def monitor_process():
        while True:
            time.sleep(1)
            if is_game_running():
                loading_win.destroy()
                break

    threading.Thread(target=monitor_process, daemon=True).start()

# ------------------ Khởi động game ------------------ #
def run_game():
    game_path = get_game_path()
    print("Đường dẫn kiểm tra:", game_path)
    if not game_path or not os.path.exists(game_path):
        messagebox.showerror("Lỗi", "Không thấy đường dẫn đến Game, vui lòng kiểm tra lại.")
        
        # Mở bảng chọn file
        selected_file = filedialog.askopenfilename(
            title="Chọn file thực thi của Game",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if selected_file:
            # Cập nhật file INI
            config.set("Game", "PathGame", selected_file)
            with open("Data\\Data.ini", "w") as configfile:
                config.write(configfile)
            messagebox.showinfo("Thông báo", "Đã lưu đường dẫn mới.")
            # Chạy game luôn
            show_loading_window()
            os.startfile(selected_file)
    else:
        show_loading_window()
        os.startfile(game_path)

# ------------------ Tabs giao diện ------------------ #
def create_notebook(app):
    notebook = ctk.CTkTabview(app, width=400, height=250)
    notebook.pack(pady=10, padx=10, expand=True, fill="both")

    notebook.add("Khởi động Game")
    ctk.CTkButton(
        notebook.tab("Khởi động Game"),
        text="Khởi động game",
        command=run_game
    ).pack(pady=10)

    notebook.add("Web truy cập")
    notebook.add("Thông tin")
    textbox = ctk.CTkTextbox(
        notebook.tab("Thông tin"),
        font=("HYWenHei 85W", 15),
        width=960,
        height=200
    )
    textbox.insert("0.0",
        "Funeuam client v0.0.1 beta - Release: 4/7/2025\n"
        "Info:\n"
        "Facebook: Phùng Hoàng Thiên Tân\n"
        "Discord: https://discord.gg/Pth7keKyJ5\n"
        "Gmail: hetcuulan1@gmail.com\n"
        "Donate me pls:\n"
        "Viettel Money - 0970833152"
    )
    textbox.configure(state="disabled", wrap="word")
    textbox.place(x=5, y=5)
    textbox.tag_add("discord", "4.9", "4.39")
    textbox.tag_config("discord", foreground="blue", underline=1)
    textbox.tag_bind("discord", "<Button-1>", open_discord_link)

def open_discord_link(event=None):
    webbrowser.open("https://discord.gg/Pth7keKyJ5")

create_notebook(app)
app.mainloop()
