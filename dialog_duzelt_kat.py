import sys
from PyQt5.QtWidgets import *

from dialog_mesaj import uyari_ver, kat_veri_kontrol

# Seçilen katın özelliklerini değiştirmeyi sağlayan arayüz
class DialogDuzeltKat(QDialog):
    def __init__(self, depo):
        super().__init__()
        self.baslik = "Kat Düzelt"
        self.depo = depo
        self.gecici = {}
        self.init_ui()

    def init_ui(self):
        # etiketleri oluştur
        etiket_kat = QLabel("Kat")
        etiket_ozellik = QLabel("Özellikler :")
        etiket_kod = QLabel("Kat Kodu")
        etiket_ad = QLabel("Kat Adı")
        etiket_bosluk = QLabel(" ")

        # veri giriş alanlarını oluştur
        self.giris_kat = QComboBox()
        self.giris_kod = QLineEdit()
        self.giris_ad = QLineEdit()

        # butonları oluştur
        buton_duzelt = QPushButton("Düzelt")
        buton_kapat = QPushButton("Kapat")
        buton_sec = QPushButton("Seç")

        # layout oluştur
        self.layout = QVBoxLayout()
        layout_buton = QHBoxLayout()
        layout_giris = QGridLayout()

        # widgetları ekle
        layout_giris.addWidget(etiket_kat, 0, 0)
        layout_giris.addWidget(self.giris_kat, 0, 1)
        layout_giris.addWidget(buton_sec, 0, 2)
        layout_giris.addWidget(etiket_bosluk, 1, 0)
        layout_giris.addWidget(etiket_ozellik, 2, 0)
        layout_giris.addWidget(etiket_kod, 3, 0)
        layout_giris.addWidget(self.giris_kod, 3, 1)
        layout_giris.addWidget(etiket_ad, 3, 2)
        layout_giris.addWidget(self.giris_ad, 3, 3)

        layout_buton.addWidget(buton_duzelt)
        layout_buton.addWidget(buton_kapat)

        self.layout.addLayout(layout_giris)
        self.layout.addLayout(layout_buton)

        # kat listesini ekle
        self.giris_kat.addItems(self.depo.kat_listesi_dondur())

        # buton fonksiyonları
        buton_kapat.clicked.connect(self.close)
        buton_sec.clicked.connect(self.kat_sec)
        buton_duzelt.clicked.connect(self.duzelt)

        # pencere ayarları
        self.setWindowTitle(self.baslik)
        self.setLayout(self.layout)

    # kat seçiminin yapılmasını sağlar
    def kat_sec(self):
        secilen_kat_adi = self.giris_kat.currentText()
        veriler = self.depo.kat_verilerini_dondur(secilen_kat_adi)
        kod, ad = veriler["Kod"], veriler["Ad"]
        self.giris_kod.setText(kod)
        self.giris_ad.setText(ad)
        self.gecici["Ad"] = ad
        self.gecici["Kod"] = kod

    # seçilen kat verilerini düzeltir
    def duzelt(self):
        yeni_ad = self.giris_ad.text()
        yeni_kod = self.giris_kod.text()
        duzeltilsin = kat_veri_kontrol(yeni_kod, yeni_ad)
        if duzeltilsin:
            islem = False
            if self.gecici["Ad"] != yeni_ad:
                if not self.depo.kontrol_kat_adi(yeni_ad):
                    self.depo.duzelt_kat(self.gecici["Ad"], "Ad", yeni_ad)
                    self.giris_kat.clear()
                    self.giris_kat.addItems(self.depo.kat_listesi_dondur())
                    islem = True
                else:
                    uyari_ver(f"{yeni_ad} mevcut.")
            if self.gecici["Kod"] != yeni_kod:
                if not self.depo.kontrol_kat_kodu(yeni_kod):
                    self.depo.duzelt_kat(yeni_ad, "Kod", yeni_kod)
                    islem = True
                else:
                    uyari_ver(f"{yeni_kod} mevcut.")
            if islem:
                self.temizle()

    # veri giriş alanlarını temizler
    def temizle(self):
        self.giris_kod.clear()
        self.giris_ad.clear()

# test için
def main():
    app = QApplication(sys.argv)
    kat = DialogDuzeltKat()
    kat.show()
    kat.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
