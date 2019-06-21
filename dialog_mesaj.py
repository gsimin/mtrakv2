import sys
from PyQt5.QtWidgets import *

# Uyarı mesajları için arayüz
class DialogMesaj(QDialog):
    def __init__(self, mesaj):
        super().__init__()
        """
        Input:
        mesaj: (str) uyarı mesajı
        """
        # uyarı etiketini oluştur (QLabel)
        self.etiket_mesaj = QLabel(mesaj)

        buton_kapat = QPushButton("Kapat")

        self.layout = QVBoxLayout()
        layout_buton = QHBoxLayout()

        layout_buton.addStretch()
        layout_buton.addWidget(buton_kapat)

        self.layout.addWidget(self.etiket_mesaj)
        self.layout.addLayout(layout_buton)

        buton_kapat.clicked.connect(self.close)

        self.setLayout(self.layout)


# Yardımcı Fonksiyonlar
# uyarı kutusu oluşturur
def uyari_ver(uyari):
    """
    Input:
    uyari: (str) uyarı mesajı yazısı
    """
    uyari = DialogMesaj(uyari)
    uyari.exec_()

# float veri girişinin doğruluğunu kontrol eder
def float_kontrol(str_sayi):
    """
    Input:
    str_sayi: (str) float a dönüştürülecek sayi teksti
    Output:
    sayi: (float) sayının float versiyonu | -1
    """
    sayi = -1
    try:
        yeni_sayi = float(str_sayi)
        if yeni_sayi > 0:
            sayi = 1
    except ValueError:
        pass
    if sayi == -1:
        uyari_ver("Pozitif sayı girin.")
    return sayi

# kat için girilen verileri kontrol eder
def kat_veri_kontrol(kod, ad):
    if ad != "" and kod != "":
        return True
    else:
        uyari_ver("Tüm değerleri giriniz.")
        return False

# mahal için girilen verileri kontrol eder
def mahal_veri_kontrol(no, ad, alan, cevre, yukseklik):
    """
    Input:
    no: (str) mahal no
    ad: (str) mahal adı
    alan: (str) mahal alanı
    cevre: (str) mahal çevresi
    yukseklik: (str) mahal yüksekliği
    Output: (bool) verilerin geçerlilik durumu
    """
    if no != "" and ad != "" and alan != "" and cevre != "" and yukseklik != "":
        alan = float_kontrol(alan)
        if alan == 1:
            cevre = float_kontrol(cevre)
            if cevre == 1:
                yukseklik = float_kontrol(yukseklik)
                if yukseklik == 1:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        uyari_ver("Tüm değerleri giriniz.")
        return False

# doğrama için girilen verileri kontrol eder
def dograma_veri_kontrol(ad, malzeme, en, boy):
    """
    Input:
    ad: (str) oluşturulacak doğramanın adı
    malzeme: (str) oluşturulacak doğramanın malzemesi
    en : (str) oluşturulacak doğramanın eni
    boy: (str) oluşturulacak doğramanın boyu
    Output: (bool) verilerin geçerlilik durumu
    """
    if ad != "" and malzeme != "" and en != "" and boy != "":
        en = float_kontrol(en)
        if en == 1:
            boy = float_kontrol(boy)
            if boy == 1:
                return True
            else:
                return False
        else:
            return False
    else:
        uyari_ver("Tüm değerleri giriniz.")
        return False

# test içi
def main():
    app = QApplication(sys.argv)
    yeni = DialogMesaj("Mahalin eklenebileceği bir kat mevcut değil.\nÖnce kat oluşturun.")
    yeni.show()
    yeni.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
