import sys
from PyQt5.QtWidgets import *

from dialog_mesaj import uyari_ver, kat_veri_kontrol

# kat oluşturmayı sağlayan arayüz
class DialogOlusturKat(QDialog):
    def __init__(self, depo):
        super().__init__()
        self.baslik = "Kat Oluştur"
        self.depo = depo
        self.init_ui()

    def init_ui(self):
        # etiketleri oluştur (QLabel)
        etiket_kod = QLabel("Kat Kodu")
        etiket_ad = QLabel("Kat Adı")

        # veri giriş alanlarını oluştur (QLineEdit)
        self.giris_kod = QLineEdit()
        self.giris_ad = QLineEdit()

        # butonları oluştur (QPushButton)
        buton_olustur = QPushButton("Oluştur")
        buton_kapat = QPushButton("Kapat")

        # layout oluştur
        self.layout = QVBoxLayout()
        layout_buton = QHBoxLayout()
        layout_giris = QGridLayout()

        # widgetları ekle
        layout_giris.addWidget(etiket_kod, 0, 0)
        layout_giris.addWidget(self.giris_kod, 0, 1)
        layout_giris.addWidget(etiket_ad, 1, 0)
        layout_giris.addWidget(self.giris_ad, 1, 1)

        layout_buton.addWidget(buton_olustur)
        layout_buton.addWidget(buton_kapat)

        self.layout.addLayout(layout_giris)
        self.layout.addLayout(layout_buton)

        # buton fonksiyonları
        buton_kapat.clicked.connect(self.close)
        buton_olustur.clicked.connect(self.olustur)

        # pencere ayarları
        self.setWindowTitle(self.baslik)
        self.setLayout(self.layout)

    # yeni kat oluşturur
    def olustur(self):
        kod = self.giris_kod.text()
        ad = self.giris_ad.text()
        eklensin = kat_veri_kontrol(kod, ad)
        if eklensin:
            if self.depo.liste_uzunlugu_ver("Kat") == 0:
                self.depo.yeni_kat(kod, ad)
                self.temizle()
            else:
                ad_kayitli = self.depo.kontrol_kat_adi(ad)
                kod_kayitli = self.depo.kontrol_kat_kodu(kod)
                if not ad_kayitli:
                    if not kod_kayitli:
                        self.depo.yeni_kat(kod, ad)
                        self.temizle()
                    else:
                        uyari_ver(f"{kod} mevcut.")
                else:
                    uyari_ver(f"{ad} mevcut.")

    # veri giriş alanlarını temizler
    def temizle(self):
        self.giris_kod.clear()
        self.giris_ad.clear()

# test için
def main():
    app = QApplication(sys.argv)
    kat = DialogOlusturKat()
    kat.show()
    kat.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
