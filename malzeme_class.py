class Malzeme():

    def __init__(self, ad, tip):
         """
         Input:
	     ad: (str) malzeme adı
         tip: (str) malzeme tipi
         """
         self.ad = ad
         self.tip = tip
         self.birim = "m2"
         self.mahal_listesi = []
         self.miktar = 0
         self.birim_kontrol()

    # süpürgelik için birim ayarı yapar
    def birim_kontrol(self):
        if self.tip == "Süpürgelik":
            self.birim = "mt"

    # malzeme verilerini listeler
    def listele(self):
        """
        Output: (list) malzeme verileri
        """
        return [self.ad, str(self.miktar), self.birim]

    # malzeme eklenen mahalin kaydini oluşturur
    def mahal_ekle(self, mahal_no, miktar):
        """
        Input:
        mahal_no: (str) malzemenin eklendiği mahal nosu
        miktar: (float) eklenecek malzeme miktarı
        """
        self.mahal_listesi.append(mahal_no)
        self.miktar_ekle(miktar)


    # malzeme mahalden çıkartıldığında kaydını siler
    def mahal_kaldir(self, mahal_no, miktar):
        """
        Input:
        mahal_no: (str) malzemenin çıkartıldığı mahal no
        miktar: (float) çıkartılacak malzeme miktarı (< 0)
        """
        self.mahal_listesi.remove(mahal_no)
        self.miktar_ekle(miktar)

    # malzeme miktarına ekler
    def miktar_ekle(self, miktar):
        """
        Input: (float) eklenecek malzeme miktarı
        """
        self.miktar += miktar
        self.miktar = round(self.miktar, 3)

    # Düzeltme İşlemleri
    # malzemenin adını düzeltir
    def duzelt_ad(self, yeni_ad):
        """
        Input:
        yeni_ad: (str) malzemenin düzeltilmiş adı
        Output: (list) malzemenin kayıtlı olduğu mahal noları
        """
        self.ad = yeni_ad
        return self.mahal_listesi

    # mahal no değişikliğini uygular
    def duzelt_mahal_no(self, eski_mahal_no, yeni_mahal_no):
        self.mahal_listesi.remove(eski_mahal_no)
        self.mahal_listesi.append(yeni_mahal_no)

    # Dosya İşlemleri
    # malzeme verilerini aktarır
    def kayit_aktar(self):
        """
        Output: (dict) malzeme verileri
        """
        return {"Tip": self.tip, "Ad": self.ad, "Birim": self.birim,
                "Miktar": self.miktar, "Mahal": self.mahal_listesi}

    # kayitli malzeme verilerini yukler
    def yukle(self, veriler):
        """
        Input:
        veriler: (dict) kayıtlı malzeme verileri
        """
        self.mahal_listesi = veriler["Mahal"]
        self.miktar = veriler["Miktar"]

    # cls dosyası için malzeme verilerini aktarır
    def aktar(self):
        return {"": "", "Ad": self.ad, "Miktar": self.miktar, "Birim": self.birim}
