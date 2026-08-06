class Kendaraan:
    """Kelas dasar (A)."""

    def __init__(self, nama, **kwargs):
        # **kwargs diteruskan ke atas (ke object) agar rantai
        # cooperative multiple inheritance tidak putus.
        super().__init__(**kwargs)
        self.nama = nama
        print(f"[Kendaraan.__init__] Inisialisasi kendaraan: {nama}")

    def info(self):
        print(f"[Kendaraan.info] Nama kendaraan: {self.nama}")

    def bergerak(self):
        print("[Kendaraan.bergerak] Kendaraan bergerak secara umum.")


class Mobil(Kendaraan):
    """Kelas turunan pertama (B)."""

    def __init__(self, jumlah_roda, **kwargs):
        # Karena MRO pada kelas D nanti adalah
        # KendaraanAmfibi -> Mobil -> Kapal -> Kendaraan -> object,
        # super().__init__() di sini BISA memanggil Kapal.__init__
        # (bukan langsung Kendaraan). Karena itu semua parameter
        # dilempar lewat **kwargs agar setiap kelas di jalur MRO
        # tetap menerima argumen yang ia butuhkan.
        super().__init__(**kwargs)
        self.jumlah_roda = jumlah_roda
        print(f"[Mobil.__init__] Jumlah roda: {jumlah_roda}")

    def bergerak(self):
        print("[Mobil.bergerak] Bergerak di darat menggunakan roda.")
        super().bergerak()


class Kapal(Kendaraan):
    """Kelas turunan kedua (C)."""

    def __init__(self, kapasitas_penumpang, **kwargs):
        super().__init__(**kwargs)
        self.kapasitas_penumpang = kapasitas_penumpang
        print(f"[Kapal.__init__] Kapasitas penumpang: {kapasitas_penumpang}")

    def bergerak(self):
        print("[Kapal.bergerak] Bergerak di air menggunakan baling-baling.")
        super().bergerak()


class KendaraanAmfibi(Mobil, Kapal):
    """
    Kelas D: mewarisi dari Mobil (B) dan Kapal (C) sekaligus.
    Inilah letak Diamond Problem, karena Mobil dan Kapal
    sama-sama mewarisi dari Kendaraan (A).
    """

    def __init__(self, nama, jumlah_roda, kapasitas_penumpang):
        # super().__init__() mengikuti MRO (Method Resolution Order):
        # KendaraanAmfibi -> Mobil -> Kapal -> Kendaraan -> object
        # Berkat pola **kwargs kooperatif, SETIAP kelas di jalur
        # tersebut dipanggil TEPAT SATU KALI dan menerima parameter
        # yang tepat, meskipun Mobil dan Kapal sama-sama "turunan"
        # dari Kendaraan (menghindari duplikasi/redundansi kode).
        super().__init__(
            nama=nama,
            jumlah_roda=jumlah_roda,
            kapasitas_penumpang=kapasitas_penumpang,
        )
        print("[KendaraanAmfibi.__init__] Objek kendaraan amfibi berhasil dibuat.")

    def bergerak(self):
        print("[KendaraanAmfibi.bergerak] Kendaraan amfibi dapat bergerak di darat & air.")
        super().bergerak()  # akan mengikuti MRO: Mobil -> Kapal -> Kendaraan


def main():
    print("=" * 60)
    print("DEMONSTRASI DIAMOND PROBLEM & METHOD RESOLUTION ORDER (MRO)")
    print("=" * 60)

    print("\nMRO dari KendaraanAmfibi:")
    for i, kelas in enumerate(KendaraanAmfibi.__mro__, start=1):
        print(f"  {i}. {kelas.__name__}")

    print("\n--- Membuat objek KendaraanAmfibi ---")
    amfibi = KendaraanAmfibi("Sea-Rex 3000", jumlah_roda=4, kapasitas_penumpang=6)

    print("\n--- Memanggil method info() ---")
    amfibi.info()

    print("\n--- Memanggil method bergerak() ---")
    amfibi.bergerak()

    print("\n--- Verifikasi isinstance ---")
    print(f"Apakah amfibi instance dari Mobil?  {isinstance(amfibi, Mobil)}")
    print(f"Apakah amfibi instance dari Kapal?  {isinstance(amfibi, Kapal)}")
    print(f"Apakah amfibi instance dari Kendaraan? {isinstance(amfibi, Kendaraan)}")


if __name__ == "__main__":
    main()