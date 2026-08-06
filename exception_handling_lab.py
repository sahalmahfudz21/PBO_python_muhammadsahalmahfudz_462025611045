# ------------------------------------------------------------
# 1. CUSTOM EXCEPTION CLASSES
# ------------------------------------------------------------
class TransaksiError(Exception):
    """Kelas dasar untuk semua exception yang berkaitan dengan transaksi bank.
    Membuat exception dasar ini mempermudah kita untuk menangkap
    SEMUA jenis error transaksi dengan satu blok except jika diperlukan.
    """
    pass


class SaldoMinimalError(TransaksiError):
    """Dipicu ketika penarikan menyebabkan saldo di bawah saldo minimal
    yang ditetapkan bank (misalnya karena biaya administrasi)."""

    def __init__(self, saldo_saat_ini, saldo_minimal):
        self.saldo_saat_ini = saldo_saat_ini
        self.saldo_minimal = saldo_minimal
        pesan = (
            f"Penarikan ditolak. Saldo akan menjadi Rp{saldo_saat_ini:,.0f}, "
            f"di bawah saldo minimal Rp{saldo_minimal:,.0f}."
        )
        super().__init__(pesan)


class JumlahTidakValidError(TransaksiError):
    """Dipicu ketika nominal transaksi <= 0 atau bukan berupa angka."""

    def __init__(self, jumlah):
        pesan = f"Jumlah transaksi tidak valid: {jumlah}. Nominal harus lebih besar dari 0."
        super().__init__(pesan)


class RekeningTerkunciError(TransaksiError):
    """Dipicu ketika rekening dalam status terkunci (misalnya karena
    terlalu banyak percobaan transaksi gagal) sehingga tidak boleh
    melakukan transaksi apa pun."""

    def __init__(self, nomor_rekening):
        pesan = f"Rekening {nomor_rekening} sedang terkunci dan tidak dapat bertransaksi."
        super().__init__(pesan)


# ------------------------------------------------------------
# 2. CLASS UTAMA
# ------------------------------------------------------------
class RekeningBank:
    """Merepresentasikan satu rekening nasabah beserta logika validasinya."""

    SALDO_MINIMAL = 50_000  # saldo minimal yang wajib tersisa di rekening

    def __init__(self, nomor_rekening, pemilik, saldo_awal=0):
        self.nomor_rekening = nomor_rekening
        self.pemilik = pemilik
        self.saldo = saldo_awal
        self.terkunci = False
        self.percobaan_gagal = 0

    def _validasi_jumlah(self, jumlah):
        if not isinstance(jumlah, (int, float)) or isinstance(jumlah, bool) or jumlah <= 0:
            raise JumlahTidakValidError(jumlah)

    def _validasi_status_rekening(self):
        if self.terkunci:
            raise RekeningTerkunciError(self.nomor_rekening)

    def setor(self, jumlah):
        """Menyetor dana ke rekening."""
        self._validasi_status_rekening()
        self._validasi_jumlah(jumlah)
        self.saldo += jumlah
        print(f"[Setor] Berhasil menyetor Rp{jumlah:,.0f}. Saldo sekarang: Rp{self.saldo:,.0f}")

    def tarik_tunai(self, jumlah):
        """Menarik dana dari rekening dengan validasi saldo minimal."""
        self._validasi_status_rekening()
        self._validasi_jumlah(jumlah)

        saldo_setelah_tarik = self.saldo - jumlah
        if saldo_setelah_tarik < self.SALDO_MINIMAL:
            self.percobaan_gagal += 1
            if self.percobaan_gagal >= 3:
                self.terkunci = True
            raise SaldoMinimalError(saldo_setelah_tarik, self.SALDO_MINIMAL)

        self.saldo = saldo_setelah_tarik
        self.percobaan_gagal = 0
        print(f"[Tarik] Berhasil menarik Rp{jumlah:,.0f}. Saldo sekarang: Rp{self.saldo:,.0f}")


# ------------------------------------------------------------
# 3. FUNGSI PEMBANTU: membungkus transaksi dengan try-except-finally
# ------------------------------------------------------------
def proses_transaksi(rekening, jenis, jumlah):
    """Membungkus satu transaksi dalam try-except-finally agar
    program tetap berjalan stabil meskipun terjadi error."""
    print(f"\n--- Memproses transaksi: {jenis.upper()} Rp{jumlah} ---")
    try:
        if jenis == "setor":
            rekening.setor(jumlah)
        elif jenis == "tarik":
            rekening.tarik_tunai(jumlah)
        else:
            raise ValueError(f"Jenis transaksi tidak dikenal: {jenis}")

    except SaldoMinimalError as e:
        print(f"[GAGAL] {e}")

    except JumlahTidakValidError as e:
        print(f"[GAGAL] {e}")

    except RekeningTerkunciError as e:
        print(f"[GAGAL] {e}")

    except TransaksiError as e:
        # Menangkap kemungkinan TransaksiError lain di masa depan
        # yang belum ditangani secara spesifik di atas.
        print(f"[GAGAL] Terjadi kesalahan transaksi: {e}")

    except Exception as e:
        # Jaring pengaman terakhir untuk error tak terduga
        # (misalnya ValueError dari jenis transaksi tidak dikenal).
        print(f"[ERROR TAK TERDUGA] {e}")

    finally:
        print("[Selesai] Proses pemeriksaan transaksi telah selesai dilakukan.")


# ------------------------------------------------------------
# 4. DEMONSTRASI PROGRAM
# ------------------------------------------------------------
def main():
    rekening = RekeningBank("1234567890", "Muhammad Sahal Mahfudz", saldo_awal=200_000)

    print("=" * 60)
    print("DEMONSTRASI EXCEPTION HANDLING - SISTEM TRANSAKSI BANK")
    print("=" * 60)
    print(f"Rekening awal: {rekening.nomor_rekening} milik {rekening.pemilik}")
    print(f"Saldo awal: Rp{rekening.saldo:,.0f}")

    # Transaksi normal (berhasil)
    proses_transaksi(rekening, "setor", 100_000)

    # Transaksi normal (berhasil)
    proses_transaksi(rekening, "tarik", 50_000)

    # Memicu JumlahTidakValidError (nominal negatif)
    proses_transaksi(rekening, "tarik", -10_000)

    # Memicu JumlahTidakValidError (bukan angka)
    proses_transaksi(rekening, "setor", "seratus ribu")

    # Memicu SaldoMinimalError (saldo akan di bawah saldo minimal)
    proses_transaksi(rekening, "tarik", 500_000)

    # Memicu jenis transaksi tidak dikenal -> ditangkap oleh except Exception
    proses_transaksi(rekening, "transfer_luar_negeri", 10_000)

    print(f"\nSaldo akhir rekening {rekening.nomor_rekening}: Rp{rekening.saldo:,.0f}")
    print(f"Status rekening terkunci: {rekening.terkunci}")


if __name__ == "__main__":
    main()
