
class Kat:
    def __init__(self, kod, ad):
        """
        Input:
        kod: (str) kat kodu
        ad: (str) kat adı
        """
        self.kod = kod
        self.ad = ad
        self.mahal_listesi = []

    # kat adını günceller
    def duzelt_ad(self, yeni_ad):
        self.ad = yeni_ad

    # kat kodunu günceller
    def duzelt_kod(self, yeni_kod):
        self.kod = yeni_kod

    # Dosya İşlemleri
    # kat verilerini aktarır
    def kayit_aktar(self):
        """
        Output: (dict) kat verileri
        """
        return {"Kod": self.kod, "Ad": self.ad, "Mahal": self.mahal_listesi}
