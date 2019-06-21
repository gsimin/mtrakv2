import sys
from PyQt5.QtWidgets import *

from dialog_mesaj import uyari_ver, dograma_veri_kontrol

# Doğrama oluşturmayı sağlayan arayüz
class DialogOlusturDograma(QDialog):
    def __init__(self, tip, depo):
        """
        Input:
        tip: (str) Doğrama tipi
        """
        super().__init__()
        self.tip = tip
        self.baslik = f"{self.tip} Oluştur"
        self.depo = depo
        self.init_ui()

    def init_ui(self):
        # etiket oluştur (QLabel)
        etiket_ad = QLabel(f"{self.tip} Adı")
        etiket_malzeme = QLabel("Malzemesi")
        etiket_en = QLabel("Eni (m)")
        etiket_boy = QLabel("Boyu (m)")

        # veri giriş alanlarını oluştur (QLineEdit)
        self.giris_ad = QLineEdit()
        self.giris_malzeme = QLineEdit()
        self.giris_en = QLineEdit()
        self.giris_boy = QLineEdit()

        # buton oluştur (QPushButton)
        buton_olustur = QPushButton("Oluştur")
        buton_kapat = QPushButton("Kapat")

        # layout oluştur
        layout_veri = QGridLayout()
        layout_buton = QHBoxLayout()
        self.layout = QVBoxLayout()

        # widget ekle
        layout_veri.addWidget(etiket_ad, 0, 0)
        layout_veri.addWidget(self.giris_ad, 0, 1)
        layout_veri.addWidget(etiket_malzeme, 1, 0)
        layout_veri.addWidget(self.giris_malzeme, 1, 1)
        layout_veri.addWidget(etiket_en, 0, 2)
        layout_veri.addWidget(self.giris_en, 0, 3)
        layout_veri.addWidget(etiket_boy, 1, 2)
        layout_veri.addWidget(self.giris_boy, 1, 3)

        layout_buton.addWidget(buton_olustur)
        layout_buton.addWidget(buton_kapat)

        self.layout.addLayout(layout_veri)
        self.layout.addLayout(layout_buton)

        # buton methodları
        buton_kapat.clicked.connect(self.close)
        buton_olustur.clicked.connect(self.olustur)

        # QDialog ayarları
        self.setWindowTitle(self.baslik)
        self.setLayout(self.layout)

    # yeni doğrama oluşturur
    def olustur(self):
        ad = self.giris_ad.text()
        malzeme = self.giris_malzeme.text()
        en = self.giris_en.text()
        boy = self.giris_boy.text()
        eklensin = dograma_veri_kontrol(ad, malzeme, en, boy)
        if eklensin:
            if self.depo.liste_uzunlugu_ver(self.tip) == 0:
                self.depo.yeni_dograma(ad, float(en), float(boy), malzeme, self.tip)
                self.temizle()
            else:
                kayitli = self.depo.kontrol_dograma_adi(self.tip, ad)
                if not kayitli:
                    self.depo.yeni_dograma(ad, float(en), float(boy), malzeme, self.tip)
                    self.temizle()
                else:
                    uyari_ver(f"{ad} mevcut.")

    # veri giriş alanlarını temizler
    def temizle(self):
        self.giris_ad.clear()
        self.giris_malzeme.clear()
        self.giris_en.clear()
        self.giris_boy.clear()

# test için
def main():
    app = QApplication(sys.argv)
    dialog = DialogOlusturDograma("Pencere")
    dialog.show()
    dialog.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
