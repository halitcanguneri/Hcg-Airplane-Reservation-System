import tkinter as tk
from tkinter import ttk
import tkinter.simpledialog as sd
import sqlite3
import subprocess
from tkinter import PhotoImage

def validate_login(username, password):
    conn = sqlite3.connect('flight_db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM airlines WHERE user_name = ? AND passw = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def admin_login():
    username = sd.askstring("Admin Girişi", "Kullanıcı Adı:")
    password = sd.askstring("Admin Girişi", "Şifre:", show="*")

    if username and password:
        if validate_login(username, password):
            open_admin_panel()
        else:
            tk.messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış.")

def open_admin_panel():
    subprocess.run(["python", "Admin.py"])

# Giriş yapma işlemi burada, örneğin bir butona tıklama ile open_admin_panel() çağrılır

def open_user_interface():
    # Kullanıcı arayüzü penceresini aç
    # ...
    user_window = tk.Toplevel(root)
    user_window.geometry("800x600")
    user_window.title("Kullanıcı Arayüzü")
    subprocess.run(["python", "UserPanel.py"])
    # Kullanıcı arayüzü widget'larını ve fonksiyonlarını burada tanımlayın

# Giriş penceresi
root = tk.Tk()
root.geometry("800x600")
root.title("Giriş Sayfası")

background_image = PhotoImage(file="arkaplan_user.png")  # Resim dosyasının yolu
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Resmi tüm pencereye yay

admin_button = tk.Button(root, text="Admin Paneli", command=admin_login)
user_button = tk.Button(root, text="Kullanıcı Arayüzü", command=open_user_interface)

admin_button.pack(pady=20)
user_button.pack(pady=20)

root.mainloop()
