import sys
from PyQt5.QtWidgets import *

from dialog_mesaj import uyari_ver

# malzeme oluşturmayı sağlayan arayüz
class DialogOlusturMalzeme(QDialog):
    def __init__(self, tip, depo):
        super().__init__()
        self.tip = tip
        self.baslik = f"{self.tip} Oluştur"
        self.depo = depo
        self.init_ui()

    def init_ui(self):
        # etiketleri oluştur (QLabel)
        etiket_ad = QLabel(f"{self.tip} Adı")

        # veri giriş alanlarını oluştur
        self.giris_ad = QLineEdit()

        # butonları oluştur
        buton_olustur = QPushButton("Oluştur")
        buton_kapat = QPushButton("Kapat")

        # layout oluştur
        self.layout = QVBoxLayout()
        layout_buton = QHBoxLayout()
        layout_giris = QHBoxLayout()

        # widgetları ekle
        layout_giris.addWidget(etiket_ad)
        layout_giris.addWidget(self.giris_ad)

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

    # yeni malzeme oluşturur
    def olustur(self):
        ad = self.giris_ad.text()
        if ad != "":
            if self.depo.liste_uzunlugu_ver(self.tip) == 0:
                self.depo.yeni_malzeme(ad, self.tip)
            else:
                kayitli = self.depo.kontrol_malzeme_adi(self.tip, ad)
                if not kayitli:
                    self.depo.yeni_malzeme(ad, self.tip)
                else:
                    uyari_ver(f"{ad} mevcut.")
            self.giris_ad.clear()
        else:
            uyari_ver("Tüm değerleri giriniz.")

# test için
def main():
    app = QApplication(sys.argv)
    yeni = DialogOlusturMalzeme("Süpürgelik")
    yeni.show()
    yeni.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
