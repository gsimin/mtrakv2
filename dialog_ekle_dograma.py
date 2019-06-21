import sys
from PyQt5.QtWidgets import *

from dialog_mesaj import uyari_ver
from dialog_listele import *

# Seçilen mahale doğrama eklemeyi sağlayan arayüz
class DialogEkleDograma(QDialog):
    def __init__(self, tip, depo):
        """
        Input:
        tip: (str) doğrama tipi
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
        etiket_dograma = QLabel(f"{self.tip} Adı")
        etiket_adet = QLabel(f"Adet")
        etiket_ekleme = QLabel("Toplam kapı adedine eklensin mi?")
        # seçim alanlarını oluştur (QComboBox - QSpinBox - QRadioButton)
        self.secim_kat = QComboBox()
        self.secim_mahal = QComboBox()
        self.secim_dograma = QComboBox()
        self.secim_adet = QSpinBox()
        self.secim_evet = QRadioButton("Evet")
        self.secim_hayir = QRadioButton("Hayır")

        # adet seçim (QSpinBox) ayarı
        self.secim_adet.setRange(1, 10)
        self.secim_adet.setValue(1)

        # RadioButton ayarları
        self.secim_evet.setChecked(True)

        # butonları oluştur
        buton_ekle = QPushButton("Ekle")
        buton_kapat = QPushButton("Kapat")

        # layout oluştur
        self.layout = QVBoxLayout()
        layout_buton = QHBoxLayout()
        layout_ekleme = QHBoxLayout()
        layout_secim = QGridLayout()

        # widget ekle
        layout_buton.addWidget(buton_ekle)
        layout_buton.addWidget(buton_kapat)

        layout_secim.addWidget(etiket_kat, 0, 0)
        layout_secim.addWidget(self.secim_kat, 0, 1)
        layout_secim.addWidget(etiket_mahal, 0, 2)
        layout_secim.addWidget(self.secim_mahal, 0, 3)
        layout_secim.addWidget(etiket_dograma, 1, 0)
        layout_secim.addWidget(self.secim_dograma, 1, 1)
        layout_secim.addWidget(etiket_adet, 1, 2)
        layout_secim.addWidget(self.secim_adet, 1, 3)

        layout_ekleme.addWidget(etiket_ekleme)
        layout_ekleme.addWidget(self.secim_evet)
        layout_ekleme.addWidget(self.secim_hayir)

        self.layout.addLayout(layout_secim)
        if self.tip == "Kapı":
            self.layout.addLayout(layout_ekleme)
        self.layout.addLayout(layout_buton)

        # seçim değerlerini oluştur
        dograma_listesi = self.depo.dograma_listesi[self.tip]
        self.secim_dograma.addItems(dograma_listesi)
        kat_listesi = self.depo.dolu_kat_listesi_dondur()
        self.secim_kat.addItems(kat_listesi)
        self.secim_olustur()
        self.secim_kat.currentTextChanged.connect(self.secim_olustur)

        # butona fonksiyon ekle
        buton_kapat.clicked.connect(self.close)
        buton_ekle.clicked.connect(self.ekle)
        buton_dograma_listesi.clicked.connect(self.dograma_listele)
        buton_mahal_listesi.clicked.connect(self.mahal_listele)

        # pencere özelliklerini ayarla
        self.setWindowTitle(self.baslik)
        self.setLayout(self.layout)

    # mahal seçim değerlerini oluşturur ve günceller
    def secim_olustur(self):
        self.secim_mahal.clear()
        secilen_kat = self.secim_kat.currentText()
        self.mahal_no_listesi, mahal_listesi = self.depo.mahal_listesi_dondur(secilen_kat)
        self.secim_mahal.addItems(mahal_listesi)

    # doğrama eklemek için verileri depo nesnesine gönderiri
    def ekle(self):
        mahal_index = self.secim_mahal.currentIndex()
        secilen_mahal = self.mahal_no_listesi[mahal_index]
        secilen_dograma = self.secim_dograma.currentText()
        adet = int(self.secim_adet.value())
        adet_ekle = True
        if self.tip == "Kapı":
            if self.secim_hayir.isChecked():
                adet_ekle = False
        sonuc = self.depo.ekle_dograma(secilen_mahal, self.tip, secilen_dograma, adet, adet_ekle)
        if sonuc:
            uyari_ver(f"{self.tip} mahale eklendi")
        else:
            uyari_ver(f"{secilen_dograma} önceden mahale eklenmiş.")

# test için
def main():
    app = QApplication(sys.argv)
    yeni = DialogEkleDograma("Kapı")
    yeni.show()
    yeni.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
