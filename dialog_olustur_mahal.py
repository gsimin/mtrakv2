import sys
from PyQt5.QtWidgets import *

from dialog_mesaj import uyari_ver, mahal_veri_kontrol

# Mahal oluşturmayı sağlayan arayüz
class DialogOlusturMahal(QDialog):
    def __init__(self, depo):
        """
        depo : (Depo) 
        """
        super().__init__()
        self.baslik = "Mahal Oluştur"
        self.depo = depo
        self.init_ui()

    def init_ui(self):
        # etiket oluştur
        etiket_kat = QLabel("Bulunduğu Kat")
        etiket_no = QLabel("Mahal No")
        etiket_ad = QLabel("Mahal Adı")
        etiket_alan = QLabel("Alanı (m2)")
        etiket_cevre = QLabel("Çevresi (m)")
        etiket_yukseklik = QLabel("Tavan Yüksekliği (m)")

        # veri giriş alanlarını oluştur
        self.giris_no = QLineEdit()
        self.giris_ad = QLineEdit()
        self.giris_alan = QLineEdit()
        self.giris_cevre = QLineEdit()
        self.giris_yukseklik = QLineEdit()

        # secim alanı oluştur
        self.secim_kat = QComboBox()

        # buton oluştur
        buton_olustur = QPushButton("Oluştur")
        buton_kapat = QPushButton("Kapat")

        # layout oluştur
        layout_veri = QGridLayout()
        layout_buton = QHBoxLayout()
        self.layout = QVBoxLayout()

        # widget ekle
        layout_veri.addWidget(etiket_kat, 0, 0)
        layout_veri.addWidget(self.secim_kat, 0, 1)
        layout_veri.addWidget(etiket_no, 1, 0)
        layout_veri.addWidget(self.giris_no, 1, 1)
        layout_veri.addWidget(etiket_ad, 2, 0)
        layout_veri.addWidget(self.giris_ad, 2, 1)
        layout_veri.addWidget(etiket_alan, 0, 2)
        layout_veri.addWidget(self.giris_alan, 0, 3)
        layout_veri.addWidget(etiket_cevre, 1, 2)
        layout_veri.addWidget(self.giris_cevre, 1, 3)
        layout_veri.addWidget(etiket_yukseklik, 2, 2)
        layout_veri.addWidget(self.giris_yukseklik, 2, 3)

        layout_buton.addWidget(buton_olustur)
        layout_buton.addStretch()
        layout_buton.addWidget(buton_kapat)

        self.layout.addLayout(layout_veri)
        self.layout.addLayout(layout_buton)

        # kat listesini ekle
        self.secim_kat.addItems(self.depo.kat_listesi_dondur())

        # buton methodları
        buton_kapat.clicked.connect(self.close)
        buton_olustur.clicked.connect(self.olustur)

        # QDialog ayarları
        self.setWindowTitle(self.baslik)
        self.setLayout(self.layout)

    # yeni mahal oluşturur
    def olustur(self):
        kat = self.secim_kat.currentText()
        no = self.giris_no.text()
        ad = self.giris_ad.text()
        alan = self.giris_alan.text()
        cevre = self.giris_cevre.text()
        yukseklik = self.giris_yukseklik.text()
        eklensin = mahal_veri_kontrol(no, ad, alan, cevre, yukseklik)
        if eklensin:
            if self.depo.liste_uzunlugu_ver("Mahal") == 0:
                self.depo.yeni_mahal(kat, no, ad, float(alan), float(cevre), float(yukseklik))
                self.temizle()
            else:
                kayitli = self.depo.kontrol_mahal_no(no, kat)
                if not kayitli:
                    self.depo.yeni_mahal(kat, no, ad, float(alan), float(cevre), float(yukseklik))
                    self.temizle()
                else:
                    uyari_ver(f"{no} kat içinde mevcut.")

    # veri giriş alanlarını temizler
    def temizle(self):
        self.giris_no.clear()
        self.giris_ad.clear()
        self.giris_alan.clear()
        self.giris_cevre.clear()
        self.giris_yukseklik.clear()

# test için
def main():
    app = QApplication(sys.argv)
    dialog = DialogOlusturMahal()
    dialog.show()
    dialog.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
