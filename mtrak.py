import sys
import os
import json
import csv

from PyQt5.QtWidgets import *

# Uygulama arayüz sınıfları
from dialog_olustur_kat import *
from dialog_olustur_mahal import *
from dialog_olustur_dograma import *
from dialog_olustur_malzeme import *

from dialog_duzelt_kat import *
from dialog_duzelt_mahal import *
from dialog_duzelt_dograma import *
from dialog_duzelt_malzeme import *

from dialog_ekle_dograma import *
from dialog_ekle_malzeme import *

from dialog_listele import *
from dialog_mesaj import uyari_ver as uyari_ver

# Veri saklamayı ve kullanıcı ile program arasındaki koordinasyonu sağlayan sınıf
from depo_class import *

# Uygulama Arayüzü
class MtrakWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.depo = Depo()
        self.init_ui()

    def init_ui(self):
        # ComoboBox için listeler
        olustur_duzelt_listesi = ["Kat", "Mahal", "Pencere", "Kapı",
                                  "Zemin Kaplaması", "Duvar Kaplaması",
                                  "Tavan Kaplaması", "Süpürgelik"]
        listele_listesi = ["Mahal", "Doğrama", "Malzeme"]
        ekle_listesi = ["Pencere", "Kapı", "Zemin Kaplaması",
                        "Tavan Kaplaması", "Duvar Kaplaması",
                        "Süpürgelik"]
        # etiket olustur
        etiket_baslik = QLabel("Yapmak istediğiniz işlemi seçin")
        etiket_bosluk = QLabel("")

        # secim alanlarını oluştur
        self.secim_olustur = QRadioButton("Oluştur")
        self.olustur_secenek = QComboBox()
        self.secim_duzelt = QRadioButton("Düzelt")
        self.duzelt_secenek = QComboBox()
        self.secim_ekle = QRadioButton("Mahale Ekle")
        self.ekle_secenek = QComboBox()
        self.secim_listele = QRadioButton("Listele")
        self.listele_secenek = QComboBox()

        # seçim alanı ayarları
        self.secim_olustur.setChecked(True)
        self.olustur_secenek.addItems(olustur_duzelt_listesi)
        self.duzelt_secenek.addItems(olustur_duzelt_listesi)
        self.ekle_secenek.addItems(ekle_listesi)
        self.listele_secenek.addItems(listele_listesi)

        # buton oluştur
        buton_sec = QPushButton("Seç")

        # layout oluştur
        layout_secim = QGridLayout()
        layout_buton = QHBoxLayout()
        self.layout = QVBoxLayout()

        # widget ekle
        layout_secim.addWidget(self.secim_olustur, 0, 0)
        layout_secim.addWidget(self.olustur_secenek, 0, 1)
        layout_secim.addWidget(etiket_bosluk, 1, 0)
        layout_secim.addWidget(self.secim_duzelt, 2, 0)
        layout_secim.addWidget(self.duzelt_secenek, 2, 1)
        layout_secim.addWidget(etiket_bosluk, 3, 0)
        layout_secim.addWidget(self.secim_ekle, 4, 0)
        layout_secim.addWidget(self.ekle_secenek, 4, 1)
        layout_secim.addWidget(etiket_bosluk, 5, 0)
        layout_secim.addWidget(self.secim_listele, 6, 0)
        layout_secim.addWidget(self.listele_secenek, 6, 1)

        layout_buton.addStretch()
        layout_buton.addWidget(buton_sec)

        self.layout.addWidget(etiket_baslik)
        self.layout.addLayout(layout_secim)
        self.layout.addWidget(etiket_bosluk)
        self.layout.addLayout(layout_buton)

        # butona fonksiyon ekle
        buton_sec.clicked.connect(lambda: self.sec(self.secim_olustur.isChecked(),
                                                   self.secim_duzelt.isChecked(),
                                                   self.secim_ekle.isChecked(),
                                                   self.secim_listele.isChecked()))
        # pencere ayarları
        self.setWindowTitle("MtraK")
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.menu_olustur()

    def sec(self, olustur, duzelt, ekle, listele):
        if olustur:
            secim = self.olustur_secenek.currentText()
            self.sec_olustur(secim)
        elif duzelt:
            secim = self.duzelt_secenek.currentText()
            self.sec_duzelt(secim)
        elif ekle:
            secim = self.ekle_secenek.currentText()
            self.sec_ekle(secim)

        elif listele:
            secim = self.listele_secenek.currentText()
            self.sec_listele(secim)

    def sec_olustur(self, secim):
        if secim == "Kat":
            kat_olustur_dialog = DialogOlusturKat(self.depo)
            kat_olustur_dialog.exec_()
        elif secim == "Mahal":
            if self.depo.liste_uzunlugu_ver("Kat") > 0:
                mahal_olustur_dialog = DialogOlusturMahal(self.depo)
                mahal_olustur_dialog.exec_()
            else:
                uyari_ver("Mahalin eklenebileceği bir kat mevcut değil.\nÖnce kat oluşturun.")
        elif secim in ["Pencere", "Kapı"]:
            dograma_olustur_dialog = DialogOlusturDograma(secim, self.depo)
            dograma_olustur_dialog.exec_()
        elif secim in ["Zemin Kaplaması", "Duvar Kaplaması", "Tavan Kaplaması", "Süpürgelik"]:
            malzeme_olustur_dialog = DialogOlusturMalzeme(secim, self.depo)
            malzeme_olustur_dialog.exec_()

    def sec_duzelt(self, secim):
        if secim == "Kat":
            if self.depo.liste_uzunlugu_ver("Kat") > 0:
                kat_duzelt_dialog = DialogDuzeltKat(self.depo)
                kat_duzelt_dialog.exec_()
            else:
                uyari_ver("Henüz kat oluşturulmamış.")
        elif secim == "Mahal":
            if self.depo.liste_uzunlugu_ver("Mahal") > 0:
                mahal_duzelt_dialog = DialogDuzeltMahal(self.depo)
                mahal_duzelt_dialog.exec_()
            else:
                uyari_ver("Henüz mahal oluşturulmamış.")
        elif secim in ["Pencere", "Kapı"]:
            if self.depo.liste_uzunlugu_ver(secim) > 0:
                dograma_duzelt_dialog = DialogDuzeltDograma(secim, self.depo)
                dograma_duzelt_dialog.exec_()
            else:
                uyari_ver(f"{secim} henüz oluşturulmamış.")
        elif secim in ["Zemin Kaplaması", "Duvar Kaplaması", "Tavan Kaplaması", "Süpürgelik"]:
            if self.depo.liste_uzunlugu_ver(secim) > 0:
                malzeme_duzelt_dialog = DialogDuzeltMalzeme(secim, self.depo)
                malzeme_duzelt_dialog.exec_()
            else:
                uyari_ver(f"{secim} henüz oluşturulmamış.")

    def sec_ekle(self, secim):
        if self.depo.liste_uzunlugu_ver(secim) > 0:
            if self.depo.liste_uzunlugu_ver("Mahal") > 0:
                if secim in ["Pencere", "Kapı"]:
                    dograma_ekle_dialog = DialogEkleDograma(secim, self.depo)
                    dograma_ekle_dialog.exec_()
                elif secim in ["Zemin Kaplaması", "Duvar Kaplaması", "Tavan Kaplaması", "Süpürgelik"]:
                    malzeme_ekle_dialog = DialogEkleMalzeme(secim, self.depo)
                    malzeme_ekle_dialog.exec_()
            else:
                uyari_ver("Henüz mahal oluşturulmamış.")
        else:
            uyari_ver(f"{secim} henüz oluşturulmamış.")

    def sec_listele(self, secim):
        if secim == "Mahal":
            if self.depo.liste_uzunlugu_ver("Mahal") > 0:
                mahal_listele_dialog = DialogListele(secim, self.depo)
                mahal_listele_dialog.exec_()
            else:
                uyari_ver("Mahal henüz eklenmemiş.")
        elif secim == "Doğrama":
            if self.depo.liste_uzunlugu_ver("Pencere") > 0 or self.depo.liste_uzunlugu_ver("Kapı") > 0:
                dograma_listele_dialog = DialogListele(secim, self.depo)
                dograma_listele_dialog.exec_()
            else:
                uyari_ver("Doğrama henüz eklenmemiş.")
        elif secim == "Malzeme":
            if self.depo.liste_uzunlugu_ver("Zemin Kaplaması") > 0 or self.depo.liste_uzunlugu_ver("Tavan Kaplaması") > 0 or self.depo.liste_uzunlugu_ver("Duvar Kaplaması") > 0 or self.depo.liste_uzunlugu_ver("Süpürgelik"):
                malzeme_listele_dialog = DialogListele(secim, self.depo)
                malzeme_listele_dialog.exec_()
            else:
                uyari_ver("Malzeme henüz eklenmemiş.")

    def menu_olustur(self):
        menubar = self.menuBar()

        # Dosya menüsünü oluştur
        dosya = menubar.addMenu("Dosya")

        # Dosya menüsü seçeneklerini oluştur
        dosya_ac = QAction("Aç", self)
        dosya_kaydet = QAction("Kaydet", self)
        disa_aktar = QAction("Dışa Aktar", self)
        cikis = QAction("Çıkış", self)

        # Kısayolları ayarla
        dosya_ac.setShortcut("Ctrl+O")
        dosya_kaydet.setShortcut("Ctrl+S")
        disa_aktar.setShortcut("Ctrl+A")
        cikis.setShortcut("Ctrl+Q")

        # Dosya menüsü aksiyonlarını ekle
        dosya.addAction(dosya_ac)
        dosya.addAction(dosya_kaydet)
        dosya.addAction(disa_aktar)
        dosya.addAction(cikis)

        dosya.triggered.connect(self.yanit)

    def yanit(self, aksiyon):
        if aksiyon.text() == "Aç":
            self.dosya_ac()
        elif aksiyon.text() == "Kaydet":
            self.dosya_kaydet()
        elif aksiyon.text() == "Dışa Aktar":
            self.disa_aktar()
        elif aksiyon.text() == "Çıkış":
            self.close()

    # kayıtlı dosyayı açar
    def dosya_ac(self):
        dosya_ismi = QFileDialog.getOpenFileName(self, "Dosya Aç",os.getenv("HOME"))
        with open(dosya_ismi[0], "r") as dosya:
            kayit = json.load(dosya)
            self.depo.sifirla()
            self.depo.yukle(kayit)
        dosya.close()


    # dosya kaydeder
    def dosya_kaydet(self):
        kayit = self.depo.k_kayit_al()
        dosya_ismi = QFileDialog.getSaveFileName(self, "Dosya Kaydet", os.getenv("HOME"))
        with open(dosya_ismi[0], "w") as dosya:
            json.dump(kayit, dosya)
        dosya.close()

    # verileri cls dosyasına kaydeder
    def disa_aktar(self):
        kayit = self.depo.dis_kayit_al()
        listeler = ["Mahal Listesi", "Zemin Kaplaması Listesi", "Tavan Kaplaması Listesi", "Duvar Kaplaması Listesi",
                    "Süpürgelik Listesi", "Kapı Listesi", "Pencere Listesi"]
        ozellik_listesi = {"Mahal": ["", "Mahal No", "Mahal Adı", "Zemin Kap.", "Miktar (Z)",
	                                 "Duvar Kap.", "Miktar (D)", "Tavan Kap.",
	                                 "Miktar (T)", "Süpürgelik", "Miktar (S)", "Pencere",
	                                 "Adet (P)", "Kapı", "Adet (K)"],
	                       "Dograma": ["", "Ad", "En", "Boy", "Malzeme", "Adet"],
	                       "Malzeme": ["", "Ad", "Miktar", "Birim"]}
        dosya_listesi = QFileDialog.getSaveFileName(self, "Dışa Aktar", os.getenv("HOME"))
        dosya_adi = dosya_listesi[0] + ".csv"
        self.bos_sayfa_olustur(dosya_adi)

        for liste in listeler:
            self.baslik_ekle(dosya_adi, [liste])
            if liste == "Mahal Listesi":
                for kat_adi in kayit["Mahal Listesi"]:
                    self.baslik_ekle(dosya_adi, [kat_adi])
                    if len(kayit["Mahal Listesi"][kat_adi]) > 0:
                        self.mahal_aktar(dosya_adi, ozellik_listesi["Mahal"], kat_adi, kayit)
            elif liste == "Kapı Listesi" or liste == "Pencere Listesi":
                if len(kayit[liste]) > 0:
                    self.dog_mal_aktar(dosya_adi, ozellik_listesi["Dograma"], liste, kayit)
            else:
                if len(kayit[liste]) > 0:
                    self.dog_mal_aktar(dosya_adi, ozellik_listesi["Malzeme"], liste, kayit)

    def bos_sayfa_olustur(self, dosya_adi):
        with open(dosya_adi, "w", newline="") as csvfile:
            satir = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            satir.writerow([""])

    def baslik_ekle(self, dosya_adi, baslik):
        with open(dosya_adi, "a", newline="") as csvfile:
            satir = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            satir.writerow(baslik)

    def mahal_aktar(self, dosya_adi, ozellik, kat_adi, kayit):
        with open(dosya_adi, "a", newline="") as csvfile:
            yazici = csv.DictWriter(csvfile, fieldnames=ozellik)
            yazici.writeheader()
            for mahal in kayit["Mahal Listesi"][kat_adi]:
                yazici.writerow(mahal)
        self.baslik_ekle(dosya_adi, [""])

    def dog_mal_aktar(self, dosya_adi, ozellik, baslik, kayit):
        with open(dosya_adi, "a", newline="") as csvfile:
            yazici = csv.DictWriter(csvfile, fieldnames=ozellik)
            yazici.writeheader()
            for metraj in kayit[baslik]:
                yazici.writerow(metraj)
        self.baslik_ekle(dosya_adi, [""])

# test için
def main():
   mtrak_app = QApplication(sys.argv)
   mtrak_pencere= MtrakWindow()
   mtrak_pencere.show()
   mtrak_pencere.raise_()
   mtrak_app.exec_()

if __name__ == "__main__":
    main()
