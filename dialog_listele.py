import sys
from PyQt5.QtWidgets import *

# metraj listelemek için arayüz
class DialogListele(QDialog):
    def __init__(self, liste_tipi, depo):
        super().__init__()
        """
        Input:
        liste_tipi: (str) neyin listeleneceğini belirtir (doğrama, mahal, malzeme)
        depo : (Depo) mtrak uygulaması içinde oluşturulan Depo sınıfına ait nesne
        """
        self.liste_tipi = liste_tipi
        self.baslik = f"{self.liste_tipi} Listesi"
        self.depo = depo

        # buton oluştur
        buton_kapat = QPushButton("Kapat")

        # layout oluştur
        layout_buton = QHBoxLayout()
        self.layout = QVBoxLayout()

        # liste tipine göre verileri ekle
        if self.liste_tipi == "Mahal":
            self.listele_mahal()
        elif self.liste_tipi == "Doğrama":
            self.listele_dograma()
        elif self.liste_tipi == "Malzeme":
            self.listele_malzeme()

        # widget ekle
        layout_buton.addStretch()
        layout_buton.addWidget(buton_kapat)
        self.layout.addLayout(layout_buton)

        # buton fonksiyonları
        buton_kapat.clicked.connect(self.close)

        # pencere ayarları
        self.setWindowTitle(self.baslik)
        self.setLayout(self.layout)

    def listele_mahal(self):
        liste_kat_adi = self.depo.kat_listesi.keys()
        for kat_adi in liste_kat_adi:
            if self.depo.kat_mahal_sayisi(kat_adi) > 0:
                self.mahal_listesi_olustur(kat_adi)

    def mahal_listesi_olustur(self, kat_adi):
        liste_baslik = ["No", "Mahal Adı", "Zemin Kap.", "Miktar(m2)",                        "Duvar Kap.", "Miktar(m2)", "Tavan Kap.",
                        "Miktar(m2)", "Süpürgelik", "Miktar(mt)",
                        "Pencere", "Adet", "Kapı", "Adet"]

        layout_liste = QGridLayout()
        layout_liste.setHorizontalSpacing(15)
        layout_liste.setVerticalSpacing(15)
        self.baslik_olustur(liste_baslik, layout_liste)
        mahal_no_listesi = self.depo.kat_listesi[kat_adi].mahal_listesi
        mahal_listesi = [self.depo.mahal_listesi[mahal_no] for mahal_no in mahal_no_listesi]
        self.veri_listesi_olustur(mahal_listesi, layout_liste)
        self.layout_ekle(kat_adi, layout_liste)

    def listele_dograma(self):
        for tip in self.depo.dograma_listesi.keys():
            if self.depo.liste_uzunlugu_ver(tip) > 0:
                self.dograma_listesi_olustur(tip)

    def dograma_listesi_olustur(self, tip):
        liste_baslik = ["Ad", "Ölçü(m)", "Adet", "Malzeme"]
        layout_liste = QGridLayout()
        layout_liste.setHorizontalSpacing(15)
        layout_liste.setVerticalSpacing(15)
        self.baslik_olustur(liste_baslik, layout_liste)
        dograma_listesi = self.depo.dograma_listesi[tip].values()
        self.veri_listesi_olustur(dograma_listesi, layout_liste)
        self.layout_ekle(f"{tip} Listesi", layout_liste)

    def listele_malzeme(self):
        for tip in self.depo.malzeme_listesi.keys():
            if self.depo.liste_uzunlugu_ver(tip) > 0:
                self.malzeme_listesi_olustur(tip)

    def malzeme_listesi_olustur(self, tip):
        liste_baslik = ["Ad", "Miktar", "Birim"]
        layout_liste = QGridLayout()
        layout_liste.setHorizontalSpacing(15)
        layout_liste.setVerticalSpacing(15)
        self.baslik_olustur(liste_baslik, layout_liste)
        malzeme_listesi = self.depo.malzeme_listesi[tip].values()
        self.veri_listesi_olustur(malzeme_listesi, layout_liste)
        self.layout_ekle(f"{tip} Listesi", layout_liste)

    def baslik_olustur(self, liste_baslik, layout):
        sutun = 0
        for baslik in liste_baslik:
            layout.addWidget(QLabel(baslik), 0, sutun)
            sutun += 1

    def veri_listesi_olustur(self, liste, layout):
        satir = 1
        sutun = 0
        for nesne in liste:
            nesne_verileri = nesne.listele()
            for veri in nesne_verileri:
                layout.addWidget(QLabel(veri), satir, sutun)
                sutun += 1
            satir += 1
            sutun = 0

    def layout_ekle(self, etiket, liste_layout):
        self.layout.addWidget(QLabel(etiket))
        self.layout.addLayout(liste_layout)
        self.layout.addWidget(QLabel(""))





# test içi
def main():
    app = QApplication(sys.argv)
    yeni = DialogListele("Mahal")
    yeni.show()
    yeni.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
