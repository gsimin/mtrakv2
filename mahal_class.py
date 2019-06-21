class Mahal():
    def __init__(self, kat_adi, kat_no, mahal_no, ad, alan, cevre, yukseklik ):
        self.kat_adi = kat_adi
        self.kat_no = kat_no
        self.mahal_no = mahal_no
        self.ad = ad
        self.alan = alan
        self.cevre = cevre
        self.yukseklik = yukseklik
        self.duvar_alan = round(cevre * yukseklik, 3)
        self.supurgelik_uzunluk = cevre
        self.malzeme_listesi = {"Zemin Kaplaması": [], "Duvar Kaplaması": [], "Tavan Kaplaması": [], "Süpürgelik": []}
        self.dograma_listesi = {"Pencere": {}, "Kapı": {}}


    # malzeme ve doğrama ekleme işlemleri
    # tipine göre mahale malzeme ekler
    def ekle_malzeme(self, tip, malzeme_adi):
        """
        Input:
        tip: (str) eklenecek malzeme tipi
        malzeme_adi: (str) eklenecek malzeme adi
        Output:
        miktar: (float) eklenen malzeme miktarı
        """
        miktar = self.miktar_bul(tip)
        self.malzeme_listesi[tip] = [malzeme_adi, miktar]
        return miktar

    def malzeme_bos(self, tip):
        if self.malzeme_listesi[tip] == []:
            return True
        else:
            return False

    # tipine göre mahale dograma ekler
    def ekle_dograma(self, tip, dograma_adi, adet, adet_ekle, olcu, depo):
        """
        Input:
        tip: (str) eklenecek dograma tipi
        dograma_adi: (str) eklenecek dograma adi
        adet: (int) eklenecek dograma miktari
        adet_ekle: (bool) doğramama adedinin genel adede eklenip eklenmediği bilgisi
        olcu: (list) eklenecek doğramanın en ve boy ölçüleri
        depo: (Depo) program içinde oluşturulan Depo nesnesi
        Output: (bool) doğramanın mahale eklenip eklenmediği bilgisi
        """
        if dograma_adi not in self.dograma_listesi[tip]:
            self.dograma_listesi[tip][dograma_adi] = [adet, adet_ekle]
            self.duvar_hesap(olcu, adet, depo)
            if tip == "Kapı":
                self.supurgelik_hesap(olcu[0], adet, depo)
            return True
        else:
            return False

    # Düzeltme İşlemleri
    # kat adı değişikliğini uygular
    def duzelt_alan(self, yeni_alan, depo):
        alan_fark = yeni_alan - self.alan
        self.alan = yeni_alan
        for tip in ["Zemin Kaplaması", "Tavan Kaplaması"]:
            if self.malzeme_listesi[tip] != []:
                malzeme_adi = self.malzeme_listesi[tip][0]
                self.malzeme_listesi[tip][1] = self.alan
                depo.malzeme_listesi[tip][malzeme_adi].miktar_ekle(alan_fark)

    def duzelt_cevre(self, yeni_cevre, depo):
        cevre_fark = yeni_cevre - self.cevre
        self.cevre = yeni_cevre
        duvar_alan_fark = cevre_fark * self.yukseklik
        self.duvar_alan += duvar_alan_fark
        self.duvar_alan = round(self.duvar_alan, 3)
        self.supurgelik_uzunluk += cevre_fark
        self.supurgelik_uzunluk = round(self.supurgelik_uzunluk, 3)
        for tip in ["Duvar Kaplaması", "Süpürgelik"]:
            if self.malzeme_listesi[tip] != []:
                malzeme_adi = self.malzeme_listesi[tip][0]
                if tip == "Duvar Kaplaması":
                    self.malzeme_listesi[tip][1] = self.duvar_alan
                    depo.malzeme_listesi[tip][malzeme_adi].miktar_ekle(duvar_alan_fark)
                elif tip == "Süpürgelik":
                    self.malzeme_listesi[tip][1] = self.supurgelik_uzunluk
                    depo.malzeme_listesi[tip][malzeme_adi].miktar_ekle(cevre_fark)

    def duzelt_yukseklik(self, yeni_yukseklik, depo):
        yukseklik_fark = yeni_yukseklik - self.yukseklik
        self.yukseklik = yeni_yukseklik
        duvar_alan_fark = self.cevre * yukseklik_fark
        self.duvar_alan += duvar_alan_fark
        self.duvar_alan = round(self.duvar_alan, 3)
        if self.malzeme_listesi["Duvar Kaplaması"] != []:
            malzeme_adi = self.malzeme_listesi["Duvar Kaplaması"][0]
            self.malzeme_listesi["Duvar Kaplaması"][1] = self.duvar_alan
            depo.malzeme_listesi["Duvar Kaplaması"][malzeme_adi].miktar_ekle(duvar_alan_fark)

    def duzelt_mahal_ad(self, yeni_ad):
        self.ad = yeni_ad

    def duzelt_kat_no(self, kat_kod, yeni_no):
        eski_mahal_no = self.mahal_no
        self.kat_no = yeni_no
        self.mahal_no = kat_kod + "-" + yeni_no
        return self.duzelt_mahal_no(eski_mahal_no)

    def duzelt_kat_ad(self, yeni_kat_adi):
        """
        Input:
        yeni_kat_adi: mahalin bulunduğu katın yeni adı
        """
        self.kat_adi = yeni_kat_adi

    def duzelt_kat_kod(self, yeni_kod):
        eski_mahal_no = self.mahal_no
        self.mahal_no = yeni_kod + "-" + self.kat_no
        return self.duzelt_mahal_no(eski_mahal_no)

    def duzelt_mahal_no(self, eski_mahal_no):
        dograma_listesi = {}
        malzeme_listesi = {}
        for tip in self.dograma_listesi:
            if len(self.dograma_listesi[tip]) > 0:
                dograma_listesi[tip] = self.dograma_listesi[tip].keys()
        for tip in self.malzeme_listesi:
            if len(self.malzeme_listesi[tip]) > 0:
                malzeme_listesi[tip] = self.malzeme_listesi[tip][0]
        return [dograma_listesi, malzeme_listesi, eski_mahal_no, self.mahal_no]

    # malzeme adı değişikliğini uygular
    def duzelt_malzeme_ad(self, tip, yeni_ad):
        """
        Input:
        tip: (str) malzeme tipi
        yeni_ad: (str) malzemenin yeni adı
        """
        self.malzeme_listesi[tip][0] = yeni_ad

    # doğrama adı değişikliğini uygular
    def duzelt_dograma_ad(self, tip, ad, yeni_ad):
        """
        Input:
        tip: (str) doğrama tipi
        ad: (str) doğrama adı
        yeni_ad: (str) doğramanın yeni adı
        """
        dograma_veri = self.dograma_listesi[tip].pop(ad)
        self.dograma_listesi[tip][yeni_ad] = dograma_veri

    # malzeme en ölçüsünü değiştirir
    def duzelt_dograma_en(self, tip, ad, olcu, yeni_en, depo):
        en = float(yeni_en) - olcu[0]
        round(en, 3)
        boy = olcu[1]
        adet = self.dograma_listesi[tip][ad][0]
        self.duvar_hesap([en, boy], adet, depo)
        if tip == "Kapı":
            self.supurgelik_hesap(en, adet, depo)

    # malzemenin boy ölçüsünü değiştirir
    def duzelt_dograma_boy(self, tip, ad, olcu, yeni_boy, depo):
        boy = float(yeni_boy) - olcu[1]
        en = olcu[0]
        adet = self.dograma_listesi[tip][ad][0]
        self.duvar_hesap([en, boy], adet, depo)


    def kaldir_pencere(self, ad, depo):
        adet = self.dograma_listesi["Pencere"][ad][0]
        pencere = depo.dograma_listesi["Pencere"][ad]
        olcu = pencere.olcu_dondur()
        # pencerede kaldırma değişikliklerini uygula
        pencere.ekle_adet(adet * -1)
        pencere.kaldir_mahal(self.mahal_no)
        # mahalde kaldırma değişikliklerini uygula
        self.duvar_hesap(olcu, adet * -1, depo)
        self.dograma_listesi["Pencere"].pop(ad)

    def kaldir_kapi(self, ad, depo):
        adet = self.dograma_listesi["Kapı"][ad][0]
        adet_eklendi = self.dograma_listesi["Kapı"][ad][1]
        kapi = depo.dograma_listesi["Kapı"][ad]
        olcu = kapi.olcu_dondur()
        # kapıda kaldırma değişikliklerini uygula
        if adet_eklendi:
            kapi.ekle_adet(adet * -1)
        kapi.kaldir_mahal(self.mahal_no)
        # mahalde kaldırma değişikliklerini uygula
        self.duvar_hesap(olcu, adet * -1, depo)
        self.supurgelik_hesap(olcu[0], adet * -1, depo)
        self.dograma_listesi["Kapı"].pop(ad)

    def kaldir_malzeme(self, tip, depo):
        malzeme_adi = self.malzeme_listesi[tip][0]
        miktar = self.malzeme_listesi[tip][1]
        malzeme = depo.malzeme_listesi[tip][malzeme_adi]
        # malzemede kaldırma değişikliğini uygula
        malzeme.mahal_kaldir(self.mahal_no, miktar * -1)
        # mahalde kaldırma değişikliklerini uygula
        self.malzeme_listesi[tip] = []


    # Hesaplama İşlemleri
    # doğrama eklendikçe duvar kaplaması alanını hesaplar
    def duvar_hesap(self, olcu, adet, depo):
        """
        Input:
        olcu: (list) doğramanın en ve boy ölçüleri
        adet: (int) doğrama adedi
        depo: (Depo) program içinde oluşturulan Depo nesnesi
        """
        en, boy = olcu
        alan = en * boy * adet
        self.duvar_alan -= alan
        self.duvar_alan = round(self.duvar_alan, 3)
        if len(self.malzeme_listesi["Duvar Kaplaması"]) > 0:
            ad = self.malzeme_listesi["Duvar Kaplaması"][0]
            duvar = depo.malzeme_listesi["Duvar Kaplaması"][ad]
            duvar.miktar_ekle(-1 * alan)
            self.malzeme_listesi["Duvar Kaplaması"][1] = self.duvar_alan

    # kapı eklendikçe süpürgelik miktarını hesaplar
    def supurgelik_hesap(self, en, adet, depo):
        """
        Input:
        en: (float) kapı genişliği
        adet: (int) kapı adedi
        depo: (Depo) program içinde oluşturulan Depo nesnesi
        """
        toplam_uzunluk = en * adet
        self.supurgelik_uzunluk -= toplam_uzunluk
        self.supurgelik_uzunluk = round(self.supurgelik_uzunluk, 3)
        if len(self.malzeme_listesi["Süpürgelik"]) > 0:
            ad = self.malzeme_listesi["Süpürgelik"][0]
            supurgelik = depo.malzeme_listesi["Süpürgelik"][ad]
            supurgelik.miktar_ekle(-1 * toplam_uzunluk)
            self.malzeme_listesi["Süpürgelik"][1] = self.supurgelik_uzunluk


    # malzemeye göre eklenecek miktarı belirler
    def miktar_bul(self, tip):
        """
        Input:
        tip: (str) malzeme tipi
        """
        miktar = self.alan
        if tip == "Süpürgelik":
            miktar = self.supurgelik_uzunluk
        elif tip == "Duvar Kaplaması":
            miktar = self.duvar_alan
        return miktar


    # mahal verilerini listeler
    def listele(self):
        """
        Output: (list) mahal verileri
        """
        malzeme = self.malzeme_listele()
        dograma = self.dograma_listele()
        veriler = [self.mahal_no, self.ad]
        veriler.extend(malzeme)
        veriler.extend(dograma)
        return veriler

    # mahal içindeki doğrama verilerini listeler
    def dograma_listele(self):
        """
        Output: (list) mahal içindeki doğrama verileri
        """
        pencere_ad = self.dograma_listesi["Pencere"].keys()
        pencere_adet = [str(self.dograma_listesi["Pencere"][ad][0]) for ad in pencere_ad]
        kapi_ad = self.dograma_listesi["Kapı"].keys()
        kapi_adet = [str(self.dograma_listesi["Kapı"][ad][0]) for ad in kapi_ad]
        pencere_ad_str = "/".join(pencere_ad)
        pencere_adet_str = "/".join(pencere_adet)
        kapi_ad_str = "/".join(kapi_ad)
        kapi_adet_str = "/".join(kapi_adet)
        return [pencere_ad_str, pencere_adet_str, kapi_ad_str, kapi_adet_str]

    # mahal içindeki malzeme verilerini listeler
    def malzeme_listele(self):
        """
        Output: (list) mahal içindeki malzeme verileri
        """
        malzeme_str = []
        tipler = self.malzeme_listesi.keys()
        for tip in tipler:
            if len(self.malzeme_listesi[tip]) > 0:
                malzeme = self.malzeme_listesi[tip][0]
                miktar = str(self.malzeme_listesi[tip][1])
            else:
                malzeme = ""
                miktar = ""
            malzeme_str.extend([malzeme, miktar])
        return malzeme_str

    # Dosya İşlemleri
    # mahal verilerini aktarır
    def kayit_aktar(self):
        """
        Output: (dict) mahal verileri
        """
        return {"Kat Adı": self.kat_adi, "Kat No": self.kat_no, "Mahal No": self.mahal_no,
                "Ad": self.ad, "Alan": self.alan, "Çevre": self.cevre, "Yükseklik": self.yukseklik,
                "Duvar Alan": self.duvar_alan, "Süpürgelik Uzunluk": self.supurgelik_uzunluk,
                "Malzemeler": self.malzeme_listesi, "Doğramalar": self.dograma_listesi}

    # kayıtlı mahal verilerini yükler
    def yukle(self, veriler):
        """
        Input:
        veriler: (dict) kayıtlı mahal verileri
        """
        self.duvar_alan = veriler["Duvar Alan"]
        self.supurgelik_uzunluk = veriler["Süpürgelik Uzunluk"]
        self.malzeme_listesi = veriler["Malzemeler"]
        self.dograma_listesi = veriler["Doğramalar"]

    # cls dosyası için mahal verilerini aktarır
    def aktar(self):
        malz = self.malzeme_listele()
        dog = self.dograma_listele()
        return {"": "", "Mahal No": self.mahal_no, "Mahal Adı": self.ad, "Zemin Kap.": malz[0],
		 "Miktar (Z)": malz[1], "Duvar Kap.": malz[2], "Miktar (D)": malz[3],
		 "Tavan Kap.": malz[4], "Miktar (T)": malz[5], "Süpürgelik": malz[6], "Miktar (S)": malz[7],
		 "Pencere": dog[0], "Adet (P)": dog[1], "Kapı": dog[2], "Adet (K)": dog[3]}
