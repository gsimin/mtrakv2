import sys
from PyQt5.QtWidgets import *
from depo_class import *

from dialog_mesaj import uyari_ver, mahal_veri_kontrol

# Seçilen mahalde düzeltme yapmayı sağlayan arayüz
class DialogDuzeltMahal(QDialog):
    def __init__(self, depo):
        """
        Input:
        depo: (Depo) depo nesnesi
        """
        super().__init__()
        self.baslik = "Mahal Düzelt"
        self.depo = depo
        self.gecici = {}
        self.init_ui()

    def init_ui(self):
        # etiket oluştur
        etiket_kat = QLabel("Bulunduğu Kat")
        etiket_mahal = QLabel("Mahal")
        etiket_ozellik = QLabel("Özellikler :")
        etiket_no = QLabel("Mahal No")
        etiket_ad = QLabel("Mahal Adı")
        etiket_alan = QLabel("Alan (m2)")
        etiket_cevre = QLabel("Çevre (m)")
        etiket_yukseklik = QLabel("Yükseklik (m)")
        etiket_pencere = QLabel("Pencereler")
        etiket_kapi = QLabel("Kapılar")
        etiket_malzeme = QLabel("Malzemeler")

        # seçim alanlarını oluştur
        self.secim_kat = QComboBox()
        self.secim_mahal = QComboBox()
        self.secim_pencere = QComboBox()
        self.secim_kapi = QComboBox()
        self.secim_malzeme = QComboBox()

        # veri giriş alanlarını oluştur
        self.giris_no = QLineEdit()
        self.giris_ad = QLineEdit()
        self.giris_alan = QLineEdit()
        self.giris_cevre = QLineEdit()
        self.giris_yukseklik = QLineEdit()

        # buton oluştur
        buton_sec = QPushButton("Seç")
        buton_duzelt = QPushButton("Düzelt")
        buton_kapat = QPushButton("Kapat")
        buton_kaldir_pencere = QPushButton("Kaldır")
        buton_kaldir_kapi = QPushButton("Kaldır")
        buton_kaldir_malzeme = QPushButton("Kaldır")

        # layout oluştur
        layout_veri = QGridLayout()
        self.layout = QVBoxLayout()

        #seçim listelerini oluştur
        kat_listesi = self.depo.dolu_kat_listesi_dondur()
        self.secim_kat.addItems(kat_listesi)
        self.secim_olustur()
        self.secim_kat.currentTextChanged.connect(self.secim_olustur)

        # widget ekle
        layout_veri.addWidget(etiket_kat, 0, 0)
        layout_veri.addWidget(self.secim_kat, 0, 1)
        layout_veri.addWidget(etiket_mahal, 0, 2)
        layout_veri.addWidget(self.secim_mahal, 0, 3)
        layout_veri.addWidget(buton_sec, 1, 3)
        layout_veri.addWidget(etiket_ozellik, 2, 0)
        layout_veri.addWidget(etiket_no, 3, 0)
        layout_veri.addWidget(self.giris_no, 3, 1)
        layout_veri.addWidget(etiket_cevre, 3, 2)
        layout_veri.addWidget(self.giris_cevre, 3, 3)
        layout_veri.addWidget(etiket_ad, 4, 0)
        layout_veri.addWidget(self.giris_ad, 4, 1)
        layout_veri.addWidget(etiket_yukseklik, 4, 2)
        layout_veri.addWidget(self.giris_yukseklik, 4, 3)
        layout_veri.addWidget(etiket_alan, 5, 0)
        layout_veri.addWidget(self.giris_alan, 5, 1)
        layout_veri.addWidget(buton_duzelt, 6, 3)
        layout_veri.addWidget(QLabel(""), 7, 0)
        layout_veri.addWidget(etiket_pencere, 8, 0)
        layout_veri.addWidget(self.secim_pencere, 8, 1)
        layout_veri.addWidget(buton_kaldir_pencere, 8, 2)
        layout_veri.addWidget(QLabel(""), 9, 0)
        layout_veri.addWidget(etiket_kapi, 10, 0)
        layout_veri.addWidget(self.secim_kapi, 10, 1)
        layout_veri.addWidget(buton_kaldir_kapi, 10, 2)
        layout_veri.addWidget(QLabel(""), 11, 0)
        layout_veri.addWidget(etiket_malzeme, 12, 0)
        layout_veri.addWidget(self.secim_malzeme, 12, 1)
        layout_veri.addWidget(buton_kaldir_malzeme, 12, 2)
        layout_veri.addWidget(QLabel(""), 13, 0)
        layout_veri.addWidget(buton_kapat, 14, 3)

        self.layout.addLayout(layout_veri)

        # buton fonksiyonlarını ekle
        buton_kapat.clicked.connect(self.close)
        buton_sec.clicked.connect(self.sec)
        buton_duzelt.clicked.connect(self.duzelt)
        buton_kaldir_pencere.clicked.connect(self.kaldir_pencere)
        buton_kaldir_kapi.clicked.connect(self.kaldir_kapi)
        buton_kaldir_malzeme.clicked.connect(self.kaldir_malzeme)

        # pencere özelliklerini ayarla
        self.setWindowTitle(self.baslik)
        self.setLayout(self.layout)

    def secim_olustur(self):
        self.secim_mahal.clear()
        secilen_kat = self.secim_kat.currentText()
        self.mahal_no_listesi, mahal_listesi = self.depo.mahal_listesi_dondur(secilen_kat)
        self.secim_mahal.addItems(mahal_listesi)

    def sec(self):
        index = self.secim_mahal.currentIndex()
        self.mahal_no = self.mahal_no_listesi[index]
        self.gecici = self.depo.mahal_listesi[self.mahal_no].kayit_aktar()
        no = self.gecici["Kat No"]
        ad = self.gecici["Ad"]
        alan = str(self.gecici["Alan"])
        cevre = str(self.gecici["Çevre"])
        yukseklik = str(self.gecici["Yükseklik"])
        self.giris_no.setText(no)
        self.giris_ad.setText(ad)
        self.giris_alan.setText(alan)
        self.giris_cevre.setText(cevre)
        self.giris_yukseklik.setText(yukseklik)
        self.pencere_listesi_olustur()
        self.kapi_listesi_olustur()
        self.malzeme_listesi_olustur()

    def pencere_listesi_olustur(self):
        self.secim_pencere.clear()
        pencere_listesi = self.gecici["Doğramalar"]["Pencere"].keys()
        if len(pencere_listesi) > 0:
            self.secim_pencere.addItems(pencere_listesi)

    def kapi_listesi_olustur(self):
        self.secim_kapi.clear()
        kapi_listesi = self.gecici["Doğramalar"]["Kapı"].keys()
        if len(kapi_listesi) > 0:
            self.secim_kapi.addItems(kapi_listesi)

    def malzeme_listesi_olustur(self):
        self.secim_malzeme.clear()
        malzeme_listesi = [malzeme for malzeme in self.gecici["Malzemeler"].keys() if len(self.gecici["Malzemeler"][malzeme]) > 0 ]
        if len(malzeme_listesi) > 0:
            self.secim_malzeme.addItems(malzeme_listesi)

    def duzelt(self):
        yeni_no = self.giris_no.text()
        yeni_ad = self.giris_ad.text()
        yeni_alan = self.giris_alan.text()
        yeni_cevre = self.giris_cevre.text()
        yeni_yukseklik = self.giris_yukseklik.text()
        duzeltilsin = mahal_veri_kontrol(yeni_no, yeni_ad, yeni_alan, yeni_cevre, yeni_yukseklik)
        if duzeltilsin:
            islem = False
            index = self.secim_mahal.currentIndex()
            if yeni_no != self.gecici["Kat No"]:
                kayitli = self.depo.kontrol_mahal_no(yeni_no, self.secim_kat.currentText())
                if not kayitli:
                    kat_adi = self.secim_kat.currentText()
                    kat_kod = self.depo.kat_kod_dondur(kat_adi)
                    self.depo.duzelt_kat_no(self.mahal_no, kat_adi, kat_kod, yeni_no)
                    self.mahal_no = kat_kod + "-" + yeni_no
                    islem = True
                else:
                    uyari_ver(f"{yeni_no} kayıtlı.")
            mahal = self.depo.mahal_listesi[self.mahal_no]
            if yeni_ad != self.gecici["Ad"]:
                mahal.duzelt_mahal_ad(yeni_ad)
                islem = True
            if float(yeni_alan) != self.gecici["Alan"]:
                mahal.duzelt_alan(float(yeni_alan), self.depo)
                islem = True
            if float(yeni_cevre) != self.gecici["Çevre"]:
                mahal.duzelt_cevre(float(yeni_cevre), self.depo)
                islem = True
            if float(yeni_yukseklik) != self.gecici["Yükseklik"]:
                mahal.duzelt_yukseklik(float(yeni_yukseklik), self.depo)
                islem = True
            if islem:
                self.gecici = self.depo.mahal_listesi[self.mahal_no].kayit_aktar()
                self.secim_olustur()
                uyari_ver("Düzeltildi.")


    def kaldir_pencere(self):
        secim = self.secim_pencere.currentText()
        self.depo.mahal_listesi[self.mahal_no].kaldir_pencere(secim, self.depo)
        self.pencere_listesi_olustur()

    def kaldir_kapi(self):
        secim = self.secim_kapi.currentText()
        self.depo.mahal_listesi[self.mahal_no].kaldir_kapi(secim, self.depo)
        self.kapi_listesi_olustur()

    def kaldir_malzeme(self):
        secim = self.secim_malzeme.currentText()
        self.depo.mahal_listesi[self.mahal_no].kaldir_malzeme(secim, self.depo)
        self.malzeme_listesi_olustur()


# test için
def main():
    depo = Depo()
    app = QApplication(sys.argv)
    yeni = DialogDuzeltMahal(depo)
    yeni.show()
    yeni.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
