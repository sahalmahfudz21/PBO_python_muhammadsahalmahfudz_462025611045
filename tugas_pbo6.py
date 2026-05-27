class dompetdigital:
   __nama = ""
   __saldo = 0
   __no_rekening = ""
   __pin = ""
   def _init_(self, nama, saldo, no_rekening, pin):
        self.__nama = nama
        self.__saldo = saldo
        self.__no_rekening = no_rekening
        self.__pin = pin

   def get_nama(self):
        return self.__nama 

   def get_saldo(self, pin_input):
        if pin_input != self.__pin:
            print("PIN salah. Tidak dapat menampilkan saldo.")
            return
        print(f"Saldo Anda saat ini: {self.__saldo}")

   def get_no_rekening(self):
        return self.__no_rekening
   
   def cek_saldo(self, pin_input):
        if pin_input != self.__pin:
            print("PIN salah. Tidak dapat menampilkan saldo.")
            return
        print(f"Saldo Anda saat ini: {self.__saldo}")

   def top_up(self, jumlah, pin_input):
        if pin_input != self.__pin:
            print("PIN salah. Tidak dapat melakukan top up.")
            return
        if jumlah <= 0:
            print("Jumlah top up harus lebih besar dari 0.")
            return
        self.__saldo += jumlah
        print(f"Top up sebesar {jumlah} berhasil. Saldo sekarang: {self.__saldo}")

   def tarik_tunai(self, jumlah, pin_input):
        if pin_input != self.__pin:
            print("PIN salah. Tidak dapat melakukan tarik tunai.")
            return
        if jumlah <= 0:
            print("Jumlah tarik tunai harus lebih besar dari 0.")
            return
        if jumlah > self.__saldo:
            print("Saldo tidak cukup untuk melakukan tarik tunai.")
            return
        self.__saldo -= jumlah
        print(f"Tarik tunai sebesar {jumlah} berhasil. Saldo sekarang: {self.__saldo}")

Dompet1 = dompetdigital("Budi", 1000000, "9876543210", "1234")
Dompet1.cek_saldo("1234")   
Dompet1.top_up(500000, "1234")
Dompet1.tarik_tunai(200000, "1234")
Dompet1.tarik_tunai(1500000, "1234")