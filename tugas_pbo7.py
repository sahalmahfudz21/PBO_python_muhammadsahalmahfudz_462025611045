class AlatPembayaran:
    def _init_(self, nama):
        self.nama = nama

    def proses_bayar(self, jumlah):
        print(f"{self.nama} memproses pembayaran sebesar Rp{jumlah:,}")

class KartuKredit(AlatPembayaran):
    def _init_(self, nama, bank):
        super()._init_(nama)
        self.bank = bank

    def proses_bayar(self, jumlah):  # override
        cicilan = jumlah / 3
        print(f"[Kartu Kredit {self.bank}] Membayar Rp{jumlah:,} → dicicil 3x = Rp{cicilan:,.0f}/bulan")

class EWallet(AlatPembayaran):
    def _init_(self, nama, saldo):
        super()._init_(nama)
        self.saldo = saldo

    def proses_bayar(self, jumlah):  # override
        if self.saldo >= jumlah:
            self.saldo -= jumlah
            print(f"[E-Wallet {self.nama}] Berhasil bayar Rp{jumlah:,}. Sisa saldo: Rp{self.saldo:,}")
        else:
            print(f"[E-Wallet {self.nama}] Saldo tidak cukup! Saldo: Rp{self.saldo:,}")

def jalankan_transaksi(objek, jumlah):
    print("-" * 45)
    objek.proses_bayar(jumlah)

if __name__ == "_main_":
    kartu  = KartuKredit("Visa Platinum", "BCA")
    dompet = EWallet("GoPay", saldo=150_000)
    dompet2= EWallet("OVO",   saldo=50_000)

    # Kirim objek berbeda ke fungsi yang SAMA → Duck Typing
    jalankan_transaksi(kartu,   300_000)
    jalankan_transaksi(dompet,  100_000)
    jalankan_transaksi(dompet2, 100_000)  # saldo tidak cukup
    print("-" * 45)