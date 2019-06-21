"""
Metraj verilerini depolar ve arayüz ile metraj verileri arasındaki kordinasyonu sağlar
"""
from kat_class import Kat
from mahal_class import Mahal
from dograma_class import Dograma
from malzeme_class import Malzeme

class Depo:
    def __init__(self):
        self.dograma_listesi = {"Pencere": {}, "Kapı": {}}
        self.malzeme_listesi = {"Zemin Kaplaması": {},
                                "Duvar Kaplaması": {},
                                "Tavan Kaplaması": {},
                                "Süpürgelik": {}}
        self.kat_listesi = {}
        self.mahal_listesi = {}

    # Dosya İşlemleri
    # yeni dosya açıldığında eski verileri siler
    def sifirla(self):
        self.dograma_listesi = {"Pencere": {}, "Kapı": {}}
        self.malzeme_listesi = {"Zemin Kaplaması": {},
                                "Duvar Kaplaması": {},
                                "Tavan Kaplaması": {},
                                "Süpürgelik": {}}
        self.kat_listesi = {}
        self.mahal_listesi = {}

    # Dosya İşlemleri
    # kaydedilecek dosya verilerini toplar
    def k_kayit_al(self):
        """
        Output: (dict) kayıtlı veriler
        """
        kayit = {"Kat": [], "Mahal": [], "Doğrama": {"Pencere": [], "Kapı": []},
                 "Malzeme": {"Zemin Kaplaması": [], "Tavan Kaplaması": [], "Duvar Kaplaması": [], "Süpürgelik": []}}

        # kat kayıtları
        for kat in self.kat_listesi.values():
            veri = kat.kayit_aktar()
            kayit["Kat"].append(veri)

        # mahal kayıtları
        for mahal in self.mahal_listesi.values():
            veri = mahal.kayit_aktar()
            kayit["Mahal"].append(veri)

        # doğrama kayıtları
        for tip in self.dograma_listesi:
            for dograma in self.dograma_listesi[tip].values():
                veri = dograma.kayit_aktar()
                kayit["Doğrama"][tip].append(veri)

        # malzeme kayıtları
        for tip in self.malzeme_listesi:
            for malzeme in self.malzeme_listesi[tip].values():
                veri = malzeme.kayit_aktar()
                kayit["Malzeme"][tip].append(veri)

        return kayit

    # kayıtlı verileri yükler
    def yukle(self, kayit):
        """
        Input:
        kayit: (dict) kayıtlı metraj verileri
        """
        # kat verileri
        for veri in kayit["Kat"]:
            self.yeni_kat(veri["Kod"], veri["Ad"])

        # mahal verileri
        for veri in kayit["Mahal"]:
            self.yeni_mahal(veri["Kat Adı"], veri["Kat No"], veri["Ad"], veri["Alan"], veri["Çevre"], veri["Yükseklik"])
            mahal_no = veri["Mahal No"]
            self.mahal_listesi[mahal_no].yukle(veri)

        # doğrama verileri (self, ad, en, boy, malzeme, tip)
        for tip in kayit["Doğrama"]:
            for veri in kayit["Doğrama"][tip]:
                self.yeni_dograma(veri["Ad"], veri["En"], veri["Boy"], veri["Malzeme"], veri["Tip"])
                self.dograma_listesi[veri["Tip"]][veri["Ad"]].yukle(veri)

        # malzeme verileri (self, ad, tip)
        for tip in kayit["Malzeme"]:
            for veri in kayit["Malzeme"][tip]:
                self.yeni_malzeme(veri["Ad"], veri["Tip"])
                self.malzeme_listesi[veri["Tip"]][veri["Ad"]].yukle(veri)

    # cls dosyası için verileri toplar
    def dis_kayit_al(self):
        """
        Output:
        kayit: (dict) metraj verileri
        """
        kayit = {"Mahal Listesi": {}, "Zemin Kaplaması Listesi": [],
                 "Duvar Kaplaması Listesi": [], "Tavan Kaplaması Listesi": [],
                 "Süpürgelik Listesi": [], "Kapı Listesi": [], "Pencere Listesi": []}

        for kat in self.kat_listesi.values():
            kat_adi = kat.ad
            mahal_no_listesi = kat.mahal_listesi
            kayit["Mahal Listesi"][kat_adi] = []
            for mahal_no in mahal_no_listesi:
                veriler = self.mahal_listesi[mahal_no].aktar()
                kayit["Mahal Listesi"][kat_adi].append(veriler)
        self.malzeme_dograma_kayit_al(self.malzeme_listesi, "Zemin Kaplaması", "Zemin Kaplaması Listesi", kayit)
        self.malzeme_dograma_kayit_al(self.malzeme_listesi, "Tavan Kaplaması", "Tavan Kaplaması Listesi", kayit)
        self.malzeme_dograma_kayit_al(self.malzeme_listesi, "Duvar Kaplaması", "Duvar Kaplaması Listesi", kayit)
        self.malzeme_dograma_kayit_al(self.malzeme_listesi, "Süpürgelik", "Süpürgelik Listesi", kayit)
        self.malzeme_dograma_kayit_al(self.dograma_listesi, "Pencere", "Pencere Listesi", kayit)
        self.malzeme_dograma_kayit_al(self.dograma_listesi, "Kapı", "Kapı Listesi", kayit)

        return kayit

    # malzeme ve dograma verilerini toplar
    def malzeme_dograma_kayit_al(self, sozluk, tip, kayit_yeri, kayit):
        for malz_dog in sozluk[tip].values():
            veriler = malz_dog.aktar()
            kayit[kayit_yeri].append(veriler)

    # liste uzunluklarını döndürür
    def liste_uzunlugu_ver(self, liste_adi):
        """
        Input:
        liste_adi: (str) liste ismi
        Output: (int) liste uzunluğu
        """
        if liste_adi == "Kat":
            return len(self.kat_listesi)
        elif liste_adi == "Mahal":
            return len(self.mahal_listesi)
        elif liste_adi in ["Pencere", "Kapı"]:
            return len(self.dograma_listesi[liste_adi])
        elif liste_adi in ["Zemin Kaplaması", "Duvar Kaplaması", "Tavan Kaplaması", "Süpürgelik"]:
            return len(self.malzeme_listesi[liste_adi])

    # Kat İşlemleri
    # yeni kat oluşturur
    def yeni_kat(self, kod, ad):
        """
        Input:
        kod: (str) oluşturulacak katın kodu
        ad: (str) oluşturulacak katın adı
        """
        kat = Kat(kod, ad)
        self.kat_listesi[ad] = kat

    # kayıtlı kat isimlerini döndürür
    def kat_listesi_dondur(self):
        """
        Output: (list) kayıtlı kat isim listesi
        """
        liste_kat_adi = self.kat_listesi.keys()
        return liste_kat_adi

    def kat_kod_listesi_dondur(self):
        """
        Output: (list) kayıtlı kat kodları listesi
        """
        liste_kod = [value.kod for value in self.kat_listesi.values()]
        return liste_kod

    def dolu_kat_listesi_dondur(self):
        return [kat for kat in self.kat_listesi.keys() if len(self.kat_listesi[kat].mahal_listesi) > 0]

    # seçilen kat verilerini döndürür
    def kat_verilerini_dondur(self, kat_adi):
        """
        Input:
        kat_adi: (str) verileri istenen katın ismi
        Output: (dict) kat verileri
        """
        return {"Kod": self.kat_listesi[kat_adi].kod, "Ad": self.kat_listesi[kat_adi].ad}

    def kat_kod_dondur(self, kat_adi):
        return self.kat_listesi[kat_adi].kod

    # kat isminin kat listesinde olup olmadığını kontrol eder
    def kontrol_kat_adi(self, kat_adi):
        """
        Input:
        kat_adi = (str) kontrol edilecek kat adi
        Output: (bool) katın listede olup olmadığı bilgisi
        """
        return kat_adi in self.kat_listesi_dondur()

    # kat kodunun kat listesinde olup olmadığını kontrol eder
    def kontrol_kat_kodu(self, kat_kodu):
        """
        Input:
        kat_kodu: (str) kontrol edilecek kat kodu
        Output: (bool) kat kodunun mevcut olup olmadığının bilgisi
        """
        liste_kod = self.kat_kod_listesi_dondur()
        if kat_kodu in liste_kod:
            return True
        else:
            return False

    def kat_mahal_sayisi(self, kat_adi):
        return len(self.kat_listesi[kat_adi].mahal_listesi)

    # kat verilerindeki değişikliklerin yapılmasını sağlar
    def duzelt_kat(self, kat_adi, degisiklik, yeni_veri):
        """
        Input:
        kat_adi: (str) digisiklik yapılacaj katın ismi
        degisiklik: (str) katın değiştirilecek özelliği
        yeni_veri: (str) değiştirilecek özelliğin yeni verisi
        """
        if degisiklik == "Ad":
            self.kat_listesi[kat_adi].duzelt_ad(yeni_veri)
            kat = self.kat_listesi[kat_adi]
            self.kat_listesi.pop(kat_adi)
            self.kat_listesi[yeni_veri] = kat
            for mahal_no in kat.mahal_listesi:
                self.mahal_listesi[mahal_no].duzelt_kat_ad(kat.ad)
        elif degisiklik == "Kod":
            self.kat_listesi[kat_adi].duzelt_kod(yeni_veri)
            kat = self.kat_listesi[kat_adi]
            liste_gecici = []
            for mahal_no in kat.mahal_listesi:
                dograma_listesi, malzeme_listesi, eski_mahal_no, yeni_mahal_no = self.mahal_listesi[mahal_no].duzelt_kat_kod(yeni_veri)
                mahal = self.mahal_listesi.pop(eski_mahal_no)
                self.mahal_listesi[yeni_mahal_no] = mahal
                liste_gecici.append(yeni_mahal_no)
                kat.mahal_listesi = liste_gecici
                for tip in dograma_listesi:
                    for dograma_adi in dograma_listesi[tip]:
                        self.dograma_listesi[tip][dograma_adi].duzelt_mahal_no(eski_mahal_no, yeni_mahal_no)
                for tip in malzeme_listesi:
                    malzeme_adi = malzeme_listesi[tip]
                    self.malzeme_listesi[tip][malzeme_adi].duzelt_mahal_no(eski_mahal_no, yeni_mahal_no)


    # Mahal İşlemleri
    # yeni mahal oluştur
    def yeni_mahal(self, kat_adi, kat_no, mahal_adi, alan, cevre, yukseklik ):
        kat_kodu = self.kat_listesi[kat_adi].kod
        mahal_no = kat_kodu + "-" + kat_no
        mahal = Mahal(kat_adi, kat_no, mahal_no, mahal_adi, alan, cevre, yukseklik)
        self.mahal_listesi[mahal_no] = mahal
        self.kat_listesi[kat_adi].mahal_listesi.append(mahal_no)

    # mahal nosunun kat içinde kayıtlı olup olmadığını kontrol eder
    def kontrol_mahal_no(self, no, kat_adi):
        """
        Input:
        no: (str) mahalin kat içindeki nosu
        kat_adi: (str) mahalin bulunduğu katın adı
        Output: (bool) mahal nosunun katta kayıtlı olup olmadığı
        """
        mahal_no = self.kat_listesi[kat_adi].kod + "-" + no
        return mahal_no in self.mahal_listesi.keys()

    # seçilen kata göre mahal listesi döndürür
    def mahal_listesi_dondur(self, kat_adi):
        mahal_no_listesi = [mahal_no for mahal_no in self.kat_listesi[kat_adi].mahal_listesi]
        mahal_listesi = [f"({mahal_no}) {self.mahal_listesi[mahal_no].ad}" for mahal_no in mahal_no_listesi]
        return [mahal_no_listesi, mahal_listesi]

    def malzemesiz_mahal_listesi_dondur(self, kat_adi, tip):
        mahal_no_listesi, mahal_listesi = self.mahal_listesi_dondur(kat_adi)
        malzemesiz_mahal_no_listesi = []
        malzemesiz_mahal_listesi = []
        index = 0
        while index < len(mahal_no_listesi):
            mahal_no = mahal_no_listesi[index]
            if self.mahal_listesi[mahal_no].malzeme_bos(tip):
                malzemesiz_mahal_no_listesi.append(mahal_no)
                malzemesiz_mahal_listesi.append(mahal_listesi[index])
            index += 1
        return [malzemesiz_mahal_no_listesi, malzemesiz_mahal_listesi]

    def ekle_malzeme(self, mahal_no, tip, malzeme_adi):
        """
        Input:
        mahal_no: (str) malzeme eklenecek mahal nosu
        tip : (str) malzeme tipi
        malzeme_adi: eklenecek malzeme adı
        """
        miktar = self.mahal_listesi[mahal_no].ekle_malzeme(tip, malzeme_adi)
        self.malzeme_listesi[tip][malzeme_adi].mahal_ekle(mahal_no, miktar)


    def ekle_dograma(self, mahal_no, tip, dograma_adi, adet, adet_ekle):
        olcu = self.dograma_listesi[tip][dograma_adi].olcu_dondur()
        eklendi = self.mahal_listesi[mahal_no].ekle_dograma(tip, dograma_adi, adet, adet_ekle, olcu, self)
        if eklendi:
            dograma = self.dograma_listesi[tip][dograma_adi]
            dograma.ekle_mahal(mahal_no)
            if adet_ekle:
                dograma.ekle_adet(adet)
        return eklendi

    def duzelt_kat_no(self, mahal_no, kat_adi, kat_kod, yeni_no):
        dograma_listesi, malzeme_listesi, eski_mahal_no, yeni_mahal_no = self.mahal_listesi[mahal_no].duzelt_kat_no(kat_kod, yeni_no)
        self.duzelt_mahal_no(dograma_listesi, malzeme_listesi, eski_mahal_no, yeni_mahal_no, kat_adi)

    def duzelt_mahal_no(self, dograma_listesi, malzeme_listesi, eski_mahal_no, yeni_mahal_no, kat_adi):
        mahal = self.mahal_listesi.pop(eski_mahal_no)
        kat = self.kat_listesi[kat_adi]
        self.mahal_listesi[yeni_mahal_no] = mahal
        kat.mahal_listesi.remove(eski_mahal_no)
        kat.mahal_listesi.append(yeni_mahal_no)
        for tip in dograma_listesi:
            for dograma_adi in dograma_listesi[tip]:
                self.dograma_listesi[tip][dograma_adi].duzelt_mahal_no(eski_mahal_no, yeni_mahal_no)
        for tip in malzeme_listesi:
            malzeme_adi = malzeme_listesi[tip]
            self.malzeme_listesi[tip][malzeme_adi].duzelt_mahal_no(eski_mahal_no, yeni_mahal_no)

    # Doğrama İşlemleri
    # yeni doğrama oluşturur
    def yeni_dograma(self, ad, en, boy, malzeme, tip):
        dograma = Dograma(ad, en, boy, malzeme, tip)
        self.dograma_listesi[tip][ad] = dograma

    # kayitli doğrama adlarını verir
    def dograma_listesi_dondur(self, tip):
        """
        Input:
        tip: (str) listelenecek doğramanın tipi
        Output: (list) kayıtlı doğrama adı listesi
        """
        liste_ad = self.dograma_listesi[tip].keys()
        return liste_ad

    def kontrol_dograma_adi(self, tip, ad):
        """
        Input:
        tip : (str) doğrama tipi
        ad: (str) kontrol edilecek ad
        """
        if ad not in self.dograma_listesi_dondur(tip):
            return False
        else:
            return True

    def dograma_verilerini_dondur(self, ad, tip):
        """
        Input:
        ad: (str) doğrama adı
        Output:
        veriler: (dict) doğrama verileri
        """
        veriler = {}
        dograma = self.dograma_listesi[tip][ad]
        veriler["Ad"] = dograma.ad
        veriler["Malzeme"] = dograma.malzeme
        veriler["En"] = dograma.en
        veriler["Boy"] = dograma.boy
        return veriler

    # doğramada yapılacak düzeltme işlemini seçer
    def duzelt_dograma(self, tip, ad, degisiklik, yeni_veri):
        """
        Input:
        tip: (str) doğrama tipi
        ad: (str) doğrama adı
        degisiklik: (str) yapılacak değişilik
        yeni_veri: (str) değiştirilecek değer
        """
        if degisiklik == "Ad":
            self.duzelt_dograma_ad(tip, ad, yeni_veri)
        elif degisiklik == "Malzeme":
            self.dograma_listesi[tip][ad].duzelt_malzeme(yeni_veri)
        elif degisiklik == "En":
            self.duzelt_dograma_en(tip, ad, yeni_veri)
        elif degisiklik == "Boy":
            self.duzelt_dograma_boy(tip, ad, yeni_veri)

    # doğrama adını değiştirir
    def duzelt_dograma_ad(self, tip, ad, yeni_ad):
        dograma = self.dograma_listesi[tip].pop(ad)
        self.dograma_listesi[tip][yeni_ad] = dograma
        mahal_no_listesi = dograma.duzelt_ad(yeni_ad)
        for mahal_no in mahal_no_listesi:
            mahal = self.mahal_listesi[mahal_no]
            mahal.duzelt_dograma_ad(tip, ad, yeni_ad)

    # doğrama en ölçüsünü değiştirir
    def duzelt_dograma_en(self, tip, ad, yeni_en):
        dograma = self.dograma_listesi[tip][ad]
        olcu = dograma.olcu_dondur()
        mahal_no_listesi = dograma.duzelt_en(yeni_en)
        for mahal_no in mahal_no_listesi:
            mahal = self.mahal_listesi[mahal_no]
            mahal.duzelt_dograma_en(tip, ad, olcu, yeni_en, self)

    # doğrama boy ölçüsünü değiştirir
    def duzelt_dograma_boy(self, tip, ad, yeni_boy):
        dograma = self.dograma_listesi[tip][ad]
        olcu = dograma.olcu_dondur()
        mahal_no_listesi = dograma.duzelt_boy(yeni_boy)
        for mahal_no in mahal_no_listesi:
            mahal = self.mahal_listesi[mahal_no]
            mahal.duzelt_dograma_boy(tip, ad, olcu, yeni_boy, self)

    # Malzeme İşlemleri
    # yeni malzeme oluşturur
    def yeni_malzeme(self, ad, tip):
        malzeme = Malzeme(ad, tip)
        self.malzeme_listesi[tip][ad] = malzeme

    # kayitli malzeme adi listesi verir
    def malzeme_listesi_dondur(self, tip):
        """
        Input:
        tip : (str) listelenecek malzeme tipi
        Output: (list) kayıtlı malzeme adı listesi
        """
        return self.malzeme_listesi[tip].keys()

    # malzeme adinin kayitli olup olmadığını kontrol eder
    def kontrol_malzeme_adi(self, tip, ad):
        """
        Input:
        tip: (str) kontrol edilecek malzeme tipi
        ad: (str) kontrol edilecek malzeme adı
        Output: (bool) malzeme adinin kayıtlı olup olmadığı bilgisi
        """
        if ad not in self.malzeme_listesi_dondur(tip):
            return False
        else:
            return True

    # malzeme adı değişikliğini yapar
    def duzelt_malzeme(self, tip, ad, yeni_ad):
        """
        Input:
        tip: (str) malzeme tipi
        ad: (str) malzemenin eski adı
        yeni_ad: (str) malzemenin yeni adı
        """
        malzeme = self.malzeme_listesi[tip].pop(ad)
        mahal_listesi = malzeme.duzelt_ad(yeni_ad)
        self.malzeme_listesi[tip][yeni_ad] = malzeme

        # malzemenin kayıtlı olduğu mahallerde isim değişikliğini uygula
        for mahal_no in mahal_listesi:
            self.mahal_listesi[mahal_no].duzelt_malzeme_ad(tip, yeni_ad)
