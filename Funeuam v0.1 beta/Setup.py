import customtkinter as ctk
import time
import threading

# Cài đặt giao diện
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Trình cài đặt")
app.geometry("400x200")
app.resizable(False, False)

# Label thông báo
label = ctk.CTkLabel(app, text="Đang cài đặt...", font=("Arial", 18))
label.pack(pady=30)

# Progress bar (thanh loading)
progressbar = ctk.CTkProgressBar(app, width=300)
progressbar.set(0)
progressbar.pack(pady=10)

# Hàm chạy loading
def install_simulation():
    for i in range(101):
        time.sleep(0.05)  # Tốc độ cài đặt
        progressbar.set(i / 100)
    label.configure(text="✅ Cài đặt hoàn tất!")

# Chạy loading bằng luồng riêng để ko bị treo giao diện
threading.Thread(target=install_simulation, daemon=True).start()

app.mainloop()
