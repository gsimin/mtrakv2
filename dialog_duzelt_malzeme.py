import sys
from PyQt5.QtWidgets import *

from dialog_mesaj import uyari_ver

# seçilen malzeme özelliklerini düzeltmeyi sağlayan arayüz
class DialogDuzeltMalzeme(QDialog):
    def __init__(self, tip, depo):
        super().__init__()
        self.tip = tip
        self.baslik = f"{self.tip} Düzelt"
        self.depo = depo
        self.init_ui()

    def init_ui(self):
        # etiketleri oluştur (QLabel)
        etiket_malzeme = QLabel(f"{self.tip}")
        etiket_ozellik = QLabel("Özellikler :")
        etiket_ad = QLabel(f"{self.tip} Adı")
        etiket_bosluk = QLabel(" ")

        # veri giriş alanlarını oluştur (QLineEdit - QCombobox)
        self.giris_malzeme = QComboBox()
        self.giris_ad = QLineEdit()

        # butonları oluştur (QPushButton)
        buton_sec = QPushButton("Seç")
        buton_duzelt = QPushButton("Düzelt")
        buton_kapat = QPushButton("Kapat")

        # layout oluştur
        self.layout = QVBoxLayout()
        layout_buton = QHBoxLayout()
        layout_giris = QGridLayout()

        # widgetları ekle
        layout_giris.addWidget(etiket_malzeme, 0, 0)
        layout_giris.addWidget(self.giris_malzeme, 0, 1)
        layout_giris.addWidget(buton_sec, 0, 2)
        layout_giris.addWidget(etiket_bosluk, 1, 0)
        layout_giris.addWidget(etiket_ozellik, 2, 0)
        layout_giris.addWidget(etiket_ad, 3, 0)
        layout_giris.addWidget(self.giris_ad, 3, 1)

        layout_buton.addWidget(buton_duzelt)
        layout_buton.addWidget(buton_kapat)

        self.layout.addLayout(layout_giris)
        self.layout.addLayout(layout_buton)

        # malzeme seçeneklerinin oluşturulması
        self.giris_malzeme.addItems(self.depo.malzeme_listesi_dondur(self.tip))

        # buton fonksiyonları
        buton_kapat.clicked.connect(self.close)
        buton_sec.clicked.connect(self.sec)
        buton_duzelt.clicked.connect(self.duzelt)

        # pencere ayarları
        self.setWindowTitle(self.baslik)
        self.setLayout(self.layout)

    # düzeltilecek malzemeyi seçer ve mevcut verileri yükler
    def sec(self):
        self.eski_ad = self.giris_malzeme.currentText()
        self.giris_ad.setText(self.eski_ad)

    # yeni girilen değerlere göre malzemede değişiklik yapar
    def duzelt(self):
        yeni_ad = self.giris_ad.text()
        if yeni_ad != "":
            if self.giris_malzeme.findText(yeni_ad) == -1:
                self.depo.duzelt_malzeme(self.tip, self.eski_ad, yeni_ad)
                self.giris_ad.setText("")
                self.giris_malzeme.clear()
                self.giris_malzeme.addItems(self.depo.malzeme_listesi_dondur(self.tip))
            else:
                uyari_ver(f"{yeni_ad} mevcut.")
        else:
            uyari_ver("Değer giriniz.")
# test için
def main():
    app = QApplication(sys.argv)
    yeni = DialogDuzeltMalzeme("Tavan Kaplaması")
    yeni.show()
    yeni.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
