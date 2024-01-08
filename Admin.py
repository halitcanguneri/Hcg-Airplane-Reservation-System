import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk
import sqlite3
from tkinter import simpledialog


def add_flight():
    # Yeni uçuş ekleme penceresi
    top = tk.Toplevel(root)
    top.geometry("800x600")
    top.title("Yeni Uçuş Ekle")
    

    # Input alanları
    flight_id_label = tk.Label(top, text="Uçuş ID:")
    flight_id_entry = tk.Entry(top)
    departure_label = tk.Label(top, text="Kalkiş Havaalani:")
    departure_entry = tk.Entry(top)
    arrival_label = tk.Label(top, text="Variş Havaalani:")
    arrival_entry = tk.Entry(top)
    flight_duration_label = tk.Label(top, text="Uçuş Süresi:")
    flight_duration_entry = tk.Entry(top)
    departure_time_label = tk.Label(top, text="Kalkiş Saati:")
    departure_time_entry = tk.Entry(top)
    # Diğer gerekli alanlar...

    
    flight_id_label.pack()
    flight_id_entry.pack()
    departure_label.pack()
    departure_entry.pack()
    arrival_label.pack()
    arrival_entry.pack()
    flight_duration_label.pack()
    flight_duration_entry.pack()
    departure_time_label.pack()
    departure_time_entry.pack()
    # Diğer alanlar için pack()...

    def add_flight_to_db(flight_id, departure, arrival, flight_duration, departure_time):
        conn = sqlite3.connect('flight_db')  # Veritabanına bağlan
        cursor = conn.cursor()

        # Veritabanında 'Flight' tablosu yoksa oluştur
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Flight (
                FlightID TEXT PRIMARY KEY, 
                DepartureAirport TEXT, 
                ArrivalAirport TEXT,
                FlightDuration TEXT,
                DepartureTime TEXT

                )
            ''')

    # Yeni uçuşu ekle
        cursor.execute("INSERT INTO Flight (FlightID, DepartureAirport, ArrivalAirport, FlightDuration, DepartureTime) VALUES (?, ?, ?, ?, ?)",
                    (flight_id, departure, arrival, flight_duration, departure_time))
        
        conn.commit()  # Değişiklikleri kaydet
        conn.close()  # Bağlantıyı kapat

    def submit_flight():
        # Uçuş bilgilerini al ve veritabanına ekle
        flight_id = flight_id_entry.get()
        departure = departure_entry.get()
        arrival = arrival_entry.get()
        departure_time=departure_time_entry.get()
        flight_duration=flight_duration_entry.get()

        # Diğer alanlardan veri al...
        
        # Veritabanına ekleme işlemi burada (sqlite3 kullanarak)
        # ...
        add_flight_to_db(flight_id, departure, arrival, flight_duration, departure_time)
        

        top.destroy()  # Pencereyi kapat

    submit_button = tk.Button(top, text="Uçuş Ekle", command=submit_flight)
    submit_button.pack()

def delete_flight_from_db(flight_id):
        conn = sqlite3.connect('flight_db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Flight WHERE FlightID = ?", (flight_id,))
        
        conn.commit()
        conn.close()

def delete_flight():
        top = tk.Toplevel(root)
        top.geometry("800x600")
        top.title("Uçuş Sil")

        flight_id_label = tk.Label(top, text="Silinecek Uçuş ID:")
        flight_id_entry = tk.Entry(top)

        flight_id_label.pack()
        flight_id_entry.pack()

        def submit_delete():
            flight_id = flight_id_entry.get()
            delete_flight_from_db(flight_id)
            top.destroy()

        delete_button = tk.Button(top, text="Uçuş Sil", command=submit_delete)
        delete_button.pack()

def update_flight():

    top = tk.Toplevel(root)
    top.geometry("800x600")
    top.title("Uçuş Güncelle")

    # Uçuş ID'si için giriş alanı
    flight_id_label = tk.Label(top, text="Güncellenecek Uçuş ID:")
    flight_id_entry = tk.Entry(top)
    flight_id_label.pack()
    flight_id_entry.pack()

    # Kalkış ve varış yerleri için giriş alanları
    departure_label = tk.Label(top, text="Yeni Kalkiş Yeri:")
    departure_entry = tk.Entry(top)
    departure_label.pack()
    departure_entry.pack()

    arrival_label = tk.Label(top, text="Yeni Variş Yeri:")
    arrival_entry = tk.Entry(top)
    arrival_label.pack()
    arrival_entry.pack()

    # Kalkış ve varış yerleri için giriş alanları
    departure_time_label = tk.Label(top, text="Kalkiş Saati:")
    departure_time_entry = tk.Entry(top)
    departure_time_label.pack()
    departure_time_entry.pack()

    # Kalkış ve varış yerleri için giriş alanları
    flight_duration_label = tk.Label(top, text="Uçuş Süresi:")
    flight_duration_entry = tk.Entry(top)
    flight_duration_label.pack()
    flight_duration_entry.pack()


    # Güncelleme fonksiyonu
    def submit_update():
        flight_id = flight_id_entry.get()
        new_departure = departure_entry.get()
        new_arrival = arrival_entry.get()
        new_departure_time=departure_time_entry.get()
        new_flight_duration=flight_duration_entry.get()

        # Veritabanında güncelleme yap
        update_flight_in_db(flight_id, new_departure, new_arrival,new_departure_time,new_flight_duration)
        top.destroy()

    update_button = tk.Button(top, text="Uçuşu Güncelle", command=submit_update)
    update_button.pack()

def update_flight_in_db(flight_id, new_departure, new_arrival, new_departure_time, new_flight_duration):
    conn = sqlite3.connect('flight_db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Flight
        SET DepartureAirport = ?, ArrivalAirport = ?, DepartureTime = ?, FlightDuration = ?
        WHERE FlightID = ?""",
        (new_departure, new_arrival, new_departure_time, new_flight_duration, flight_id))
    
    conn.commit()
    conn.close()

def fetch_flights():
    conn = sqlite3.connect('flight_db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Flight")
    flight = cursor.fetchall()
    conn.close()
    return flight

def fetch_filtered_flights(destination):
    conn = sqlite3.connect('flight_db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Flight WHERE ArrivalAirport = ?", (destination,))
    flight = cursor.fetchall()
    conn.close()
    return flight

def display_all_flights():
    flight = fetch_flights()
    display_flights(flight)

def display_filtered_flights():
    
    destination = destination_entry.get()
    flight = fetch_filtered_flights(destination)
    display_flights(flight)
     # Treeview'i temizle
    for i in tree.get_children():
        tree.delete(i)
    # Filtrelenmiş uçuşları ekle
    for flight in flight:
        tree.insert('', 'end', values=flight)

def display_flights(flight):
    for flight in fetch_flights():
        tree.insert('', 'end', values=flight)

def show_passengers(flight_id):
    conn = sqlite3.connect('flight_db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Flight_{flight_id}")
    passengers = cursor.fetchall()
    conn.close()

    # Satın alan kişileri göstermek için yeni bir pencere
    passenger_window = tk.Toplevel()
    passenger_window.title(f"Uçuş {flight_id} - Yolcu Listesi")
    passenger_window.geometry("800x600")

    # Yolcu bilgilerini göstermek için Treeview
    columns = ("Name", "Surname", "TicketType", "CardNumber", "CVV")
    tree = ttk.Treeview(passenger_window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(expand=True, fill='both')

    for passenger in passengers:
        tree.insert('', 'end', values=passenger)

def ask_flight_id_and_show():
    flight_id = simpledialog.askstring("Uçuş ID", "Uçuşun ID'sini girin:")
    if flight_id:
        show_passengers(flight_id)




# Ana pencere
root = tk.Tk()
root.geometry("800x600")
root.title("Admin Paneli")
background_image = PhotoImage(file="arkaplan_user.png")  # Resim dosyasının yolu
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Resmi tüm pencereye yay

# Treeview widget'ı oluşturma
columns = ('FlightID', 'Departure', 'Arrival', 'Duration', 'DepartureTime')
tree = ttk.Treeview(root, columns=columns, show='headings')

style = ttk.Style()
style.theme_use("default")

# Treeview renklerini değiştirme
style.configure("Treeview",
                background="silver",  # Arka plan rengi
                fieldbackground="lightgrey",  # Alan arka plan rengi
                rowheight=25)  # Satır yüksekliği

# Seçili satır rengini değiştirme
style.map('Treeview', background=[('selected', 'darkgrey')])

# Sütun başlıklarını tanımlama
for col in columns:
    tree.heading(col, text=col)

tree.pack(expand=True, fill='both')

destination_label = tk.Label(root, text="Variş Yeri:")
destination_entry = tk.Entry(root)
filter_button = tk.Button(root, text="Filtrele", command=display_filtered_flights)


destination_label.pack()
destination_entry.pack()
filter_button.pack()



add_button = tk.Button(root, text="Yeni Uçuş Ekle", command=add_flight)
add_button.pack(pady=10)

# Silme butonu ana pencerede
delete_button = tk.Button(root, text="Uçuş Sil", command=delete_flight)
delete_button.pack(pady=10)

# Güncelleme butonu ana pencerede
update_button = tk.Button(root, text="Uçuş Güncelle", command=update_flight)
update_button.pack(pady=5)

# Uçuşları listelemek için listbox
# listbox = tk.Listbox(root, width=50, height=10)
# listbox.pack()

show_button = tk.Button(root, text="Uçuşlari Göster", command=display_all_flights)
show_button.pack(pady=10)

show_passenger_button = tk.Button(root, text="Uçuşu Satın Alanları Göster", command=ask_flight_id_and_show)
show_passenger_button.pack(pady=10)

# Program başladığında tüm uçuşları göster
display_all_flights()

root.mainloop()
