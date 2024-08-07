import tkinter as tk
import math
import random

class Top:
    def __init__(self, master):
        self.master = master
        self.master.title("Köpek ve Kemik")
        self.canvas = tk.Canvas(master, width=1920, height=1080)
        self.canvas.pack()

        # Arka plan resmi
        self.arka_plan_image = tk.PhotoImage(file="arkaplan.png")  # Arka plan resmi
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.arka_plan_image)

        # Resimleri yükle
        self.kemik_image = tk.PhotoImage(file="kemik.png").subsample(2)  # Kemik resmi
        self.kopek_image = tk.PhotoImage(file="kopek.png").subsample(2)  # Köpek resmi

        # Kemik başlangıç konumu (sağda)
        self.kemik_x = 1720  
        self.kemik_y = 540
        self.kemik = self.canvas.create_image(self.kemik_x, self.kemik_y, image=self.kemik_image)

        # Köpek başlangıç konumu (solda)
        self.kopek_x = 200  
        self.kopek_y = 540
        self.hiz = 3

        # Köpek resmini oluştur
        self.top = self.canvas.create_image(self.kopek_x, self.kopek_y, image=self.kopek_image)

        # Skor
        self.skor = 0
        self.skor_label = self.canvas.create_text(50, 20, text=f"Skor: {self.skor}", font=("Arial", 24), fill="black")

        # Daireler
        self.daireler = []
        for _ in range(10):  # Başlangıçta 10 daire oluştur
            self.daire_ekle()

        # Kemik sürüklenebilir
        self.canvas.tag_bind(self.kemik, "<ButtonPress-1>", self.kemik_suru)
        self.canvas.tag_bind(self.kemik, "<B1-Motion>", self.kemik_hareket)

        # Hız artırma butonu
        self.hiz_artir_button = tk.Button(master, text="▲", command=self.hiz_artir, font=("Arial", 24))
        self.hiz_artir_button.place(x=1800, y=20)

        # Hız azaltma butonu
        self.hiz_dusur_button = tk.Button(master, text="▼", command=self.hiz_dusur, font=("Arial", 24))
        self.hiz_dusur_button.place(x=1800, y=60)

        self.hareket()

    def daire_ekle(self):
        x = random.randint(25, 1895)
        y = random.randint(25, 1055)
        daire = self.canvas.create_oval(x, y, x + 25, y + 25, fill="blue")
        self.daireler.append(daire)

    def kemik_suru(self, event):
        self.offset_x = event.x - self.kemik_x
        self.offset_y = event.y - self.kemik_y

    def kemik_hareket(self, event):
        self.kemik_x = event.x - self.offset_x
        self.kemik_y = event.y - self.offset_y
        self.canvas.coords(self.kemik, self.kemik_x, self.kemik_y)

    def hareket(self):
        dx = self.kemik_x - self.kopek_x
        dy = self.kemik_y - self.kopek_y
        mesafe = math.hypot(dx, dy)
        if mesafe > 0:
            dx /= mesafe
            dy /= mesafe
            self.kopek_x += dx * self.hiz
            self.kopek_y += dy * self.hiz

        # Kenarlara çarpma kontrolü
        if self.kopek_x >= 1920:
            self.kopek_x = 1920
        elif self.kopek_x <= 0:
            self.kopek_x = 0
        if self.kopek_y >= 1080:
            self.kopek_y = 1080
        elif self.kopek_y <= 0:
            self.kopek_y = 0

        self.canvas.coords(self.top, self.kopek_x, self.kopek_y)

        # Kemikle çarpışma kontrolü
        if self.kemik_kontrol():
            self.oyun_bitti()

        # Daireler ile çarpışma kontrolü
        for daire in self.daireler[:]:
            if self.daire_kontrol(daire):
                self.skor += 1
                self.canvas.itemconfig(self.skor_label, text=f"Skor: {self.skor}")
                self.canvas.delete(daire)
                self.daireler.remove(daire)
                self.daire_ekle()  # Yeni daire ekle

        self.master.after(20, self.hareket)

    def daire_kontrol(self, daire):
        daire_coords = self.canvas.coords(daire)
        daire_x = (daire_coords[0] + daire_coords[2]) / 2
        daire_y = (daire_coords[1] + daire_coords[3]) / 2
        mesafe = math.hypot(daire_x - self.kopek_x, daire_y - self.kopek_y)
        return mesafe < 50

    def kemik_kontrol(self):
        if self.kemik:  # Kemik nesnesinin varlığını kontrol et
            kemik_coords = self.canvas.coords(self.kemik)
            if len(kemik_coords) == 4:  # Dört eleman var mı kontrol et
                kemik_x = (kemik_coords[0] + kemik_coords[2]) / 2
                kemik_y = (kemik_coords[1] + kemik_coords[3]) / 2
                mesafe = math.hypot(kemik_x - self.kopek_x, kemik_y - self.kopek_y)
                return mesafe < 100  # 100 piksel mesafe
        return False

    def oyun_bitti(self):
        self.canvas.delete("all")
        self.canvas.create_text(960, 540, text="Oyun bitti! Kemik alındı.", font=("Arial", 24), fill="red")

    def hiz_artir(self):
        self.hiz += 1

    def hiz_dusur(self):
        if self.hiz > 1:
            self.hiz -= 1

    def cikis(self, event=None):
        self.master.quit()  # Oyundan çık

if __name__ == "__main__":
    root = tk.Tk()
    top = Top(root)
    root.mainloop()