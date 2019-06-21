import sys
from PyQt5.QtWidgets import *

from dialog_mesaj import uyari_ver, dograma_veri_kontrol

# Seçilen doğramada düzeltme yapmayı sağlayan arayüz
class DialogDuzeltDograma(QDialog):
    def __init__(self, tip, depo):
        """
        Input:
        tip: (str) Doğrama tipi
        """
        super().__init__()
        self.tip = tip
        self.baslik = f"{self.tip} Düzelt"
        self.depo = depo
        self.gecici = {}
        self.init_ui()

    def init_ui(self):

        #etiket oluştur (QLabel)
        etiket_dograma = QLabel(f"{self.tip}")
        etiket_ozellik = QLabel("Özellikleri :")
        etiket_ad = QLabel(f"{self.tip} Adı")
        etiket_malzeme = QLabel("Malzemesi")
        etiket_en = QLabel("Eni (m)")
        etiket_boy = QLabel("Boyu (m)")
        etiket_bosluk = QLabel(" ")

        # veri giriş alanlarını oluştur (QLineEdit - QCombobox)
        self.giris_dograma = QComboBox()
        self.giris_ad = QLineEdit()
        self.giris_malzeme = QLineEdit()
        self.giris_en = QLineEdit()
        self.giris_boy = QLineEdit()

        # buton oluştur (QPushButton)
        buton_sec = QPushButton("Seç")
        buton_kapat = QPushButton("Kapat")
        buton_duzelt = QPushButton("Düzelt")

        # layout oluştur
        layout_veri = QGridLayout()
        layout_buton = QHBoxLayout()
        self.layout = QVBoxLayout()

        # widget ekle
        layout_veri.addWidget(etiket_dograma, 0, 0)
        layout_veri.addWidget(self.giris_dograma, 0, 1)
        layout_veri.addWidget(buton_sec, 0, 2)
        layout_veri.addWidget(etiket_bosluk, 1, 0)
        layout_veri.addWidget(etiket_ozellik, 2, 0)
        layout_veri.addWidget(etiket_ad, 3, 0)
        layout_veri.addWidget(self.giris_ad, 3, 1)
        layout_veri.addWidget(etiket_malzeme, 4, 0)
        layout_veri.addWidget(self.giris_malzeme, 4, 1)
        layout_veri.addWidget(etiket_en, 3, 2)
        layout_veri.addWidget(self.giris_en, 3, 3)
        layout_veri.addWidget(etiket_boy, 4, 2)
        layout_veri.addWidget(self.giris_boy, 4, 3)

        layout_buton.addWidget(buton_duzelt)
        layout_buton.addWidget(buton_kapat)

        self.layout.addLayout(layout_veri)
        self.layout.addLayout(layout_buton)

        # doğrama seçeneklerinin oluşturulması
        self.giris_dograma.addItems(self.depo.dograma_listesi[self.tip].keys())

        # buton fonksiyonları
        buton_kapat.clicked.connect(self.close)
        buton_sec.clicked.connect(self.sec)
        buton_duzelt.clicked.connect(self.duzelt)

        # pencere ayarları
        self.setWindowTitle(self.baslik)
        self.setLayout(self.layout)

    # seçilen doğramanın verilerini aktarır
    def sec(self):
        secim = self.giris_dograma.currentText()
        self.gecici = self.depo.dograma_verilerini_dondur(secim, self.tip)
        self.giris_ad.setText(self.gecici["Ad"])
        self.giris_malzeme.setText(self.gecici["Malzeme"])
        self.giris_en.setText(str(self.gecici["En"]))
        self.giris_boy.setText(str(self.gecici["Boy"]))

    # seçilen dograma verilerini duzeltir
    def duzelt(self):
        yeni_ad = self.giris_ad.text()
        yeni_malzeme = self.giris_malzeme.text()
        yeni_en = self.giris_en.text()
        yeni_boy = self.giris_boy.text()
        duzeltilsin = dograma_veri_kontrol(yeni_ad, yeni_malzeme, yeni_en, yeni_boy)
        if duzeltilsin:
            islem = False
            if self.giris_dograma.findText(yeni_ad) == 1 and yeni_ad != self.gecici["Ad"]:
                uyari_ver(f"{yeni_ad} mevcut")
            else:
                if self.giris_dograma.findText(yeni_ad) == -1:
                    self.depo.duzelt_dograma(self.tip, self.gecici["Ad"], "Ad", yeni_ad)
                    self.giris_dograma.clear()
                    self.giris_dograma.addItems(self.depo.dograma_listesi[self.tip].keys())
                    islem = True
                if self.gecici["Malzeme"] != yeni_malzeme:
                    self.depo.duzelt_dograma(self.tip, yeni_ad, "Malzeme", yeni_malzeme)
                    islem = True
                if str(self.gecici["En"]) != yeni_en:
                    self.depo.duzelt_dograma(self.tip, yeni_ad, "En", yeni_en)
                    islem = True
                if str(self.gecici["Boy"]) != yeni_boy:
                    self.depo.duzelt_dograma(self.tip, yeni_ad, "Boy", yeni_boy)
                    islem = True
                if islem:
                    self.temizle()

    def temizle(self):
        self.giris_ad.clear()
        self.giris_malzeme.clear()
        self.giris_en.clear()
        self.giris_boy.clear()

# test için
def main():
    app = QApplication(sys.argv)
    dialog = DialogDuzeltDograma("Pencere")
    dialog.show()
    dialog.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
