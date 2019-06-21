class Dograma():
	def __init__(self, ad, en, boy, malzeme, tip):
		"""
		ad: (str) dograma adı
		en: (float) dograma genisligi
		boy: (float) dograma yuksekligi
		malzeme: (str) dograma malzemesi
		adet: (int) dograma adedi
		mahal: (dict) dogramanin bulundugu mahaller ve adet miktarı
		"""
		self.ad = ad
		self.en = en
		self.boy = boy
		self.malzeme = malzeme
		self.tip = tip
		self.adet = 0
		self.mahal_listesi = []

	# doğramanın eklendiği mahalin nosunu ekler
	def ekle_mahal(self, mahal_no):
		"""
		Input
		mahal_no: (str) doğramanın eklendiği mahal no
		"""
		self.mahal_listesi.append(mahal_no)

	def kaldir_mahal(self, mahal_no):
		self.mahal_listesi.remove(mahal_no)

	# doğrama adet toplamına ekler
	def ekle_adet(self, adet):
		"""
		Input:
		adet: (int) eklenecek adet miktarı
		"""
		self.adet += adet

	# Düzeltme İşlemleri
	# doğrama adını düzeltir
	def duzelt_ad(self, yeni_ad):
		"""
		Input:
		yeni_ad: (str) doğramanın yeni adı
		Output: (list) doğramanın kayıtlı olduğu mahal noları
		"""
		self.ad = yeni_ad
		return self.mahal_listesi

	# doğramanın malzemesini düzeltir
	def duzelt_malzeme(self, yeni_malzeme):
		self.malzeme = yeni_malzeme

	# dogramanın en ölçüsünü değiştirir
	def duzelt_en(self, yeni_en):
		"""
		Input:
		yeni_en: (str) doğramanın yeni en ölçüsü
		Output: (list) doğramanın kayıtlı olduğu mahal noları
		"""
		self.en = float(yeni_en)
		return self.mahal_listesi

	# doğramanın boy ölçüsünü değiştirir
	def duzelt_boy(self, yeni_boy):
		"""
		Input:
		yeni_boy: (str) doğramanın yeni boy ölçüsü
		Output: (list) doğramanın kayıtlı olduğu mahal noları
		"""
		self.boy = float(yeni_boy)
		return self.mahal_listesi

	# mahal no değişikliğini uygular
	def duzelt_mahal_no(self, eski_mahal_no, yeni_mahal_no):
		self.mahal_listesi.remove(eski_mahal_no)
		self.mahal_listesi.append(yeni_mahal_no)

	# dograma olculerini verir
	def olcu_dondur(self):
		"""
		Output: (list) doğrama ölçüleri
		"""
		return [self.en, self.boy]

	# doğrama verilerini listeler
	def listele(self):
		"""
		Output: (list) doğrama verileri
		"""
		olcu = str(self.en) + "/" + str(self.boy)
		return [self.ad, olcu, str(self.adet), self.malzeme]

	# Dosya İşlemleri
	# doğrama verilerini aktarır
	def kayit_aktar(self):
		"""
		Output: (dict) doğrama verileri
		"""
		return {"Tip": self.tip, "Ad": self.ad, "En": self.en, "Boy": self.boy,
				"Malzeme": self.malzeme, "Adet": self.adet, "Mahal": self.mahal_listesi}

	# kayıtlı doğrama verilerini yükler
	def yukle(self, veriler):
		"""
		Input:
		veriler: (dict) kayıtlı doğrama verileri (adet, mahal_listesi)
		"""
		self.adet = veriler["Adet"]
		self.mahal_listesi = veriler["Mahal"]

	# cls dosyası için doğrama verilerini aktarır
	def aktar(self):
		"""
		Output: (dict) dograma verileri
		"""
		return {"": "", "Ad": self.ad, "En": self.en,
				"Boy": self.boy, "Malzeme": self.malzeme, "Adet": self.adet}
