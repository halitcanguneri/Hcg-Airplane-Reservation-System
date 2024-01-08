import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox, simpledialog
import sqlite3

# Uçuşları Veritabanından Çekme
def fetch_flights():
    conn = sqlite3.connect('flight_db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Flight")
    flights = cursor.fetchall()
    conn.close()
    return flights

# Uçuşları Treeview'de Gösterme
def display_flights(tree):
    flights = fetch_flights()
    for flight in flights:
        tree.insert('', 'end', values=flight)

# Bilet Satın Alma İşlemi
def purchase_flight(tree):
    selected_item = tree.selection()
    if selected_item:
        selected_item = selected_item[0]
        flight_id = tree.item(selected_item)['values'][0]

        # Kullanıcıdan bilet tipi ve diğer bilgileri al
        ticket_type = simpledialog.askstring("Bilet Tipi", "Bilet Tipi (Ekonomi/Business):")
        if ticket_type not in ["Ekonomi", "Business"]:
            messagebox.showerror("Hata", "Geçersiz bilet tipi.")
            return

        name = simpledialog.askstring("Adı", "Adınız:")
        surname = simpledialog.askstring("Soyadı", "Soyadınız:")
        card_number = simpledialog.askstring("Kart Numarası", "Kart Numarası:")
        cvv = simpledialog.askstring("CVV", "CVV:")
        # ...

        # Satın alma onayı
        if messagebox.askyesno("Satın Alma Onayı", "Bilet satın almak istediğinize emin misiniz?"):
            purchase_ticket(flight_id, name, surname, ticket_type, card_number, cvv)

# Bilet Satın Alma Veritabanı İşlemleri
def purchase_ticket(flight_id, name, surname, ticket_type, card_number, cvv):
    conn = sqlite3.connect('flight_db')
    cursor = conn.cursor()

    # Uçuş ID'sine göre tablo oluşturma
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS Flight_{flight_id} (
                        Name TEXT, 
                        Surname TEXT,
                        TicketType TEXT,
                        CardNumber TEXT,
                        CVV TEXT
                        )''')

    # Bilet satın alma bilgilerini ekleme
    cursor.execute(f"INSERT INTO Flight_{flight_id} (Name, Surname, TicketType, CardNumber, CVV) VALUES (?, ?, ?, ?, ?)",
                   (name, surname, ticket_type, card_number, cvv))
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Başarılı", "Bilet satın alındı.")

# Kullanıcı Paneli Penceresi
def open_user_panel():
    user_window = tk.Toplevel()
    user_window.geometry("800x600")
    user_window.title("Kullanıcı Paneli")

    # Treeview Widget'ı
    columns = ('FlightID', 'Departure', 'Arrival', 'Duration', 'DepartureTime', 'Price')
    tree = ttk.Treeview(user_window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(expand=True, fill='both')

    display_flights(tree)

    # Satın Al Butonu
    purchase_button = tk.Button(user_window, text="Satın Al", command=lambda: purchase_flight(tree))
    purchase_button.pack(pady=10)

# Ana Pencere
root = tk.Tk()
root.geometry("800x600")
root.title("HCG Hava Yolları")
background_image = PhotoImage(file="arkaplan_admin.png")  # Resim dosyasının yolu
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Resmi tüm pencereye yay

# Kullanıcı Paneli Butonu
user_button = tk.Button(root, text="Kullanıcı Panelini Aç", command=open_user_panel)
user_button.pack(pady=20)

root.mainloop()
