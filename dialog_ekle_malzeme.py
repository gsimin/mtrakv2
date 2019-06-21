import sys
from PyQt5.QtWidgets import *

from dialog_mesaj import uyari_ver

# Seçilen mahale malzeme eklemeyi sağlayan arayüz
class DialogEkleMalzeme(QDialog):
    def __init__(self, tip, depo):
        """
        Input:
        tip: (str) malzeme tipi
        """
        super().__init__()
        self.tip = tip
        self.baslik = f"Mahale {self.tip} Ekle"
        self.depo = depo
        self.init_ui()

    def init_ui(self):
        # etiketleri oluştur (QLabel)
        etiket_kat = QLabel("Bulunduğu Kat")
        etiket_mahal = QLabel("Mahal")
        etiket_malzeme = QLabel(f"{self.tip} Adı")

        # seçim alanlarını oluştur (QComboBox - QSpinBox - QRadioButton)
        self.secim_kat = QComboBox()
        self.secim_mahal = QComboBox()
        self.secim_malzeme = QComboBox()

        # butonları oluştur
        buton_ekle = QPushButton("Ekle")
        buton_kapat = QPushButton("Kapat")

        # layout oluştur
        self.layout = QVBoxLayout()
        layout_buton = QHBoxLayout()
        layout_secim = QGridLayout()

        # widget ekle
        layout_buton.addWidget(buton_ekle)
        layout_buton.addWidget(buton_kapat)

        layout_secim.addWidget(etiket_kat, 0, 0)
        layout_secim.addWidget(self.secim_kat, 0, 1)
        layout_secim.addWidget(etiket_mahal, 0, 2)
        layout_secim.addWidget(self.secim_mahal, 0, 3)
        layout_secim.addWidget(etiket_malzeme, 1, 0)
        layout_secim.addWidget(self.secim_malzeme, 1, 1)

        self.layout.addLayout(layout_secim)
        self.layout.addLayout(layout_buton)

        # seçim değerlerini oluştur
        malzeme_listesi = self.depo.malzeme_listesi[self.tip]
        self.secim_malzeme.addItems(malzeme_listesi)
        kat_listesi = self.depo.dolu_kat_listesi_dondur()
        self.secim_kat.addItems(kat_listesi)
        self.secim_olustur()
        self.secim_kat.currentTextChanged.connect(self.secim_olustur)

        # butona fonksiyon ekle
        buton_kapat.clicked.connect(self.close)
        buton_ekle.clicked.connect(self.ekle)

        # pencere özelliklerini ayarla
        self.setWindowTitle(self.baslik)
        self.setLayout(self.layout)

    # mahal seçim değerlerini oluşturur ve günceller
    def secim_olustur(self):
        self.secim_mahal.clear()
        secilen_kat = self.secim_kat.currentText()
        self.mahal_no_listesi, mahal_listesi = self.depo.malzemesiz_mahal_listesi_dondur(secilen_kat, self.tip)
        self.secim_mahal.addItems(mahal_listesi)

    # malzeme eklemek için verileri depo nesnesine gönderir
    def ekle(self):
        mahal_index = self.secim_mahal.currentIndex()
        secilen_mahal = self.mahal_no_listesi[mahal_index]
        secilen_malzeme = self.secim_malzeme.currentText()
        self.depo.ekle_malzeme(secilen_mahal, self.tip, secilen_malzeme)
        uyari_ver(f"{secilen_malzeme} mahale eklendi.")
        self.secim_olustur()

# test için
def main():
    app = QApplication(sys.argv)
    yeni = DialogEkleMalzeme("Duvar Kaplaması")
    yeni.show()
    yeni.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
