print ("""Nama Anggota Kelompok 1, kelas 2024D:
      1.	EL SYIFA SAWITRI        (24091397120)
      2.	NUR ISMA ULAIYAH        (24091397127)
      3.	ADITYA NUR FIRMANSYAH   (24091397138)
""")

# Import library yang dibutuhkan
import itertools                  # Untuk menyusun semua kemungkinan permutasi (TSP)
import networkx as nx             # Untuk membuat dan menganalisis graf
import matplotlib.pyplot as plt   # Untuk menampilkan visualisasi graf

# ======================= KELAS PETA ==========================
class Peta:
    def __init__(self):
        # Inisialisasi adjacency list untuk menyimpan daftar kota dan jalannya
        self.daftarKota = {}

    def tambahKota(self, kota):
        # Menambahkan kota ke dalam graf jika belum ada
        if kota not in self.daftarKota:
            self.daftarKota[kota] = {}

    def printKota(self):
        # Menampilkan semua kota beserta koneksinya
        for kota in self.daftarKota:
            print(f"{kota} -- {self.daftarKota[kota]}")

    def tambahJalan(self, kota1, kota2, jarak):
        # Menambahkan edge/jalan dua arah antar kota dengan jaraknya
        if kota1 in self.daftarKota and kota2 in self.daftarKota:
            self.daftarKota[kota1][kota2] = jarak
            self.daftarKota[kota2][kota1] = jarak

    def hapusKota(self, kotaDihapus):
        # Menghapus kota dan semua jalan yang terhubung dengannya
        if kotaDihapus in self.daftarKota:
            for kota in list(self.daftarKota.keys()):
                if kotaDihapus in self.daftarKota[kota]:
                    del self.daftarKota[kota][kotaDihapus]
            del self.daftarKota[kotaDihapus]

    def hapusJalan(self, kota1, kota2):
        # Menghapus jalan antara dua kota
        if kota1 in self.daftarKota and kota2 in self.daftarKota:
            self.daftarKota[kota1].pop(kota2, None)
            self.daftarKota[kota2].pop(kota1, None)

    def ruteTempuh(self, kota1, kota2):
        # Menampilkan rute terpendek dari kota1 ke kota2 menggunakan Dijkstra
        daftar_jarak, daftar_rute = self.dijkstra(kota1)

        if kota1 not in daftar_jarak or kota2 not in daftar_jarak:
            print("Anda harus memasukkan sesuai daftar kota")
        else:
            jarak_tempuh = daftar_jarak[kota2]
            rute = []
            current = kota2
            while current != kota1:
                rute.append(current)
                current = daftar_rute[current]
            rute.append(kota1)
            rute.reverse()
            print(f"\nJalur tercepat dari {kota1} ke {kota2} (dengan moda transportasi mobil):")
            print(" -> ".join(rute))
            print(f"Total jarak tempuh: {jarak_tempuh:.2f} km")

    def dijkstra(self, start):
        # Implementasi algoritma Dijkstra untuk mencari jarak terpendek dari satu kota ke semua kota lainnya
        kota_ingin_dikunjungi = list(self.daftarKota.keys())
        daftar_jarak = {kota: float("inf") for kota in kota_ingin_dikunjungi}
        daftar_jarak[start] = 0
        daftar_rute = {}

        while kota_ingin_dikunjungi:
            kota_terdekat = min(kota_ingin_dikunjungi, key=lambda kota: daftar_jarak[kota])
            kota_ingin_dikunjungi.remove(kota_terdekat)

            for kota_tetangga, jarak in self.daftarKota[kota_terdekat].items():
                total_jarak = daftar_jarak[kota_terdekat] + jarak
                if total_jarak < daftar_jarak[kota_tetangga]:
                    daftar_jarak[kota_tetangga] = total_jarak
                    daftar_rute[kota_tetangga] = kota_terdekat

        return daftar_jarak, daftar_rute

    # Mencari rute TSP terbaik (tanpa harus kembali ke kota asal)
    def tsp_brute_force(self):
        kota_list = list(self.daftarKota.keys())
        min_jarak = float("inf")
        rute_terbaik = []

        for perm in itertools.permutations(kota_list):
            jarak_total = 0
            valid = True
            for i in range(len(perm) - 1):
                jarak = self.daftarKota[perm[i]].get(perm[i+1])
                if jarak is None:
                    valid = False
                    break
                jarak_total += jarak

            if valid and jarak_total < min_jarak:
                min_jarak = jarak_total
                rute_terbaik = list(perm)

        print("\nRute TSP terbaik (brute-force) dengan moda transportasi mobil:")
        print(" -> ".join(rute_terbaik))
        print("Total jarak tempuh:", min_jarak, "km")

# ===================== JALANKAN PETA =====================
# Daftar kota dan edge
PetaKoreaSelatan = [
    "Seoul", "Busan", "Incheon", "Gwangju", "Daejeon",
    "Ulsan", "Suwon", "Changwon", "Jeju", "Andong"
]

# Daftar edge atau jalan antar kota beserta jaraknya
edges = [
    ("Seoul", "Busan", 325), ("Seoul", "Incheon", 48), ("Busan", "Gwangju", 128),
    ("Incheon", "Suwon", 30), ("Daejeon", "Ulsan", 165), ("Ulsan", "Changwon", 65),
    ("Jeju", "Seoul", 450), ("Andong", "Seoul", 200), ("Andong", "Busan", 150),
    ("Andong", "Gwangju", 180), ("Seoul", "Daejeon", 150), ("Suwon", "Daejeon", 90),
    ("Incheon", "Daejeon", 110), ("Jeju", "Busan", 500), ("Jeju", "Gwangju", 400),
    ("Jeju", "Ulsan", 470), ("Changwon", "Busan", 40), ("Changwon", "Gwangju", 200),
    ("Changwon", "Incheon", 380), ("Ulsan", "Busan", 70), ("Daejeon", "Andong", 160),
    ("Gwangju", "Suwon", 230), ("Seoul", "Changwon", 350), ("Suwon", "Jeju", 480),
    ("Incheon", "Jeju", 460), ("Gwangju", "Daejeon", 140), ("Andong", "Ulsan", 170),
    ("Busan", "Incheon", 370), ("Jeju", "Andong", 430), ("Suwon", "Ulsan", 310)
]

# Membuat objek dari kelas peta
KoreaSelatan = Peta()

# Menambahkan semua kota ke dalam graf
for kota in PetaKoreaSelatan:
    KoreaSelatan.tambahKota(kota)

# Menambahkan semua jalan ke dalam graf
for kota1, kota2, jarak in edges:
    KoreaSelatan.tambahJalan(kota1, kota2, jarak)

# ============ VISUALISASI MENGGUNAKAN NETWORKX ============
# Visualisasi menggunakan NetworkX
G = nx.Graph()
G.add_nodes_from(PetaKoreaSelatan)
for kota1, kota2, jarak in edges:
    G.add_edge(kota1, kota2, weight=jarak)

# Menampilkan graf
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42) # Menentukan posisi simpul
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
nx.draw_networkx_edges(G, pos, width=2)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Visualisasi Graf Korea Selatan")
plt.axis('off')
plt.show()

# Validasi konektivitas graph
if nx.is_connected(G):
    print("Graf terhubung (connected).")
else:
    print("Graf tidak terhubung.")

# Contoh penggunaan
print("\n===== DAFTAR KOTA =====")
for kota in PetaKoreaSelatan:
    print("-", kota)

# Input lokasi dan tujuan dari pengguna
lokasi = input("\nLokasi Anda sekarang: ").title()
tujuan = input("Tujuan Anda: ").title()

# Menampilkan rute terpendek dari lokasi ke tujuan
KoreaSelatan.ruteTempuh(lokasi, tujuan)

# Menjalankan TSP
print("\nMenjalankan TSP brute-force...")
KoreaSelatan.tsp_brute_force()