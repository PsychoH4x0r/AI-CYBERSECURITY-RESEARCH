# 🔬 AI Cybersecurity Research Environment

![Banner](https://img.shields.io/badge/Author-psychoh4x0r-red?style=flat-square) ![Version](https://img.shields.io/badge/Version-1.0-blue?style=flat-square) ![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

**AI Cybersecurity Research Environment** adalah alat canggih untuk penelitian keamanan siber, dibuat oleh **psychoh4x0r** alias **Unknown1337**. Proyek ini mengintegrasikan AI (via OpenRouter dan model seperti Claude 3.5 Sonnet) dengan fitur vulnerability assessment, network topology mapping, dan security auditing. Dirancang untuk peneliti keamanan yang ingin mengotomatiskan analisis kerentanan, memetakan topologi jaringan, dan melakukan audit konfigurasi dengan laporan HTML bertema gelap yang estetis.

⚠️ **Peringatan**: Alat ini hanya untuk **penelitian keamanan resmi dan berizin**. Penggunaan untuk aktivitas ilegal dilarang keras.

---

## 🚀 Fitur Utama

- **🛡️ Vulnerability Assessment**: 
  - Mengidentifikasi kerentanan (CVE) berdasarkan layanan dan versi.
  - Menghitung skor risiko (CVSS) dan memberikan rekomendasi remediasi.
  - Mendukung parsing output dari Nmap, Masscan, dan format lainnya.

- **🗺️ Network Topology Mapping**: 
  - Memetakan host, layanan, subnet, dan jalur serangan potensial.
  - Visualisasi HTML interaktif dengan tema gelap.

- **🔐 Security Configuration Audit**: 
  - Mengaudit konfigurasi SSL/TLS, header keamanan HTTP, dan layanan (SSH, FTP, web, database).
  - Menyediakan skor keamanan dan rekomendasi terperinci.

- **🤖 Integrasi AI OpenRouter**: 
  - Menggunakan model AI seperti Claude 3.5 Sonnet untuk analisis cerdas.
  - Fallback ke model gratis atau mode offline jika API tidak tersedia.

- **📊 Laporan Visual**: 
  - Menghasilkan laporan HTML dengan desain modern (dark theme).
  - Menyimpan hasil analisis dalam format JSON untuk analisis lebih lanjut.

- **🔑 Manajemen API Key**: 
  - Validasi dan manajemen API key OpenRouter dengan antarmuka interaktif.
  - Dukungan untuk kredit gratis dari OpenRouter.

- **🛠️ Setup Otomatis**: 
  - Menginstal alat pentesting (Nmap, Masscan, Metasploit, dll.) di Arch Linux.
  - Mengunduh wordlist SecLists untuk enumeration.

---

## 📋 Prasyarat

- **Sistem Operasi**: Arch Linux (direkomendasikan) atau distribusi Linux lain.
- **Python**: Versi 3.13 atau lebih baru.
- **Dependensi Sistem**:
  - `pacman` dan `yay` untuk instalasi paket.
  - `geckodriver` untuk otomatisasi berbasis browser (opsional).
  - `rust` untuk beberapa dependensi alat pentesting.
- **Dependensi Python**:
  - `open-interpreter`
  - `litellm`
  - `requests`
  - `psutil`
- **API Key**: OpenRouter API key (dapatkan gratis di [openrouter.ai/keys](https://openrouter.ai/keys)).
- **Ruang Disk**: Minimal 5GB untuk alat dan wordlist.

---

## ⚙️ Instalasi

1. **Clone Repository**
   ```bash
   git clone https://github.com/PsychoH4x0r/AI-CYBERSECURITY-RESEARCH
   cd ai-cybersec-research
   ```

2. **Buat Virtual Environment**
   ```bash
   python -m venv oi-env
   source oi-env/bin/activate
   ```

3. **Install Dependensi Python**
   ```bash
   pip install open-interpreter litellm requests psutil
   ```

4. **Install Alat Pentesting**
   Jalankan perintah berikut untuk menginstal alat pentesting dan wordlist:
   ```bash
   python unknown1337.py --install-tools
   ```

5. **Konfigurasi API Key**
   Jalankan menu manajemen API key untuk mengatur OpenRouter API key:
   ```bash
   python unknown1337.py --api-key-menu
   ```

6. **Verifikasi Setup**
   Jalankan pengecekan sistem:
   ```bash
   python unknown1337.py --system-check
   ```

---

## 🖥️ Penggunaan

Jalankan script utama dengan perintah:
```bash
python unknown1337.py
```

### Menu Interaktif
Setelah menjalankan script, kamu akan masuk ke menu interaktif dengan opsi berikut:
1. **Vulnerability Assessment**: Analisis kerentanan dari file scan (Nmap/Masscan) atau input langsung.
   ```bash
   python unknown1337.py --vuln-assess <scan_file.xml>
   ```
2. **Network Topology Mapping**: Buat peta jaringan dan visualisasi HTML.
   ```bash
   python unknown1337.py --network-map <scan_file.xml>
   ```
3. **Security Configuration Audit**: Audit SSL/TLS, header HTTP, dan konfigurasi layanan.
   ```bash
   python unknown1337.py --security-audit <target_url>
   ```
4. **API Key Management**: Kelola OpenRouter API key.
   ```bash
   python unknown1337.py --api-key-menu
   ```
5. **System Check**: Periksa status disk dan memori.
   ```bash
   python unknown1337.py --system-check
   ```

### Contoh Penggunaan
- **Analisis Kerentanan dari File Nmap**:
  ```bash
  python unknown1337.py --vuln-assess nmap_scan.xml
  ```
  Output: Laporan JSON dan HTML di `~/research/reports/`.

- **Pemetaan Jaringan**:
  ```bash
  python unknown1337.py --network-map nmap_scan.xml
  ```
  Output: Visualisasi HTML di `~/research/results/`.

- **Audit Konfigurasi Keamanan**:
  ```bash
  python unknown1337.py --security-audit https://example.com
  ```
  Output: Laporan audit HTML di `~/research/reports/`.

---

---

## 🛠️ Pemecahan Masalah

- **Error 404 Not Found (OpenRouter API)**:
  - Pastikan API key valid. Jalankan `python unknown1337.py --api-key-menu` dan pilih opsi 2 untuk validasi.
  - Periksa koneksi internet dan status OpenRouter di [status.openrouter.ai](https://status.openrouter.ai).

- **Timeout Error**:
  - Tambah timeout di `api_config.json`:
    ```json
    {"timeout": 30}
    ```
  - Pastikan firewall tidak memblokir port 443.

- **Dependensi Tidak Terinstall**:
  - Pastikan `pacman` dan `yay` terkonfigurasi dengan benar.
  - Jalankan ulang `python unknown1337.py --install-tools`.

- **Laporan HTML Tidak Terbuka**:
  - Pastikan browser modern (Firefox/Chrome) terinstall.
  - Buka file HTML di `~/research/reports/` secara manual.

Untuk bantuan lebih lanjut, buka issue di GitHub atau hubungi **psychoh4x0r** di X (@psychoh4x0r).

---

## 📜 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE). Gunakan dengan bijak untuk penelitian keamanan yang sah.

---

## 🙏 Kredit

- **psychoh4x0r (Unknown1337)**: Pencipta dan pengembang utama.
- **OpenRouter**: Integrasi API untuk model AI canggih.
- **Grok (xAI)**: Inspirasi dan bantuan dalam pengembangan kode.
- **SecLists**: Wordlist untuk enumeration.
- **Komunitas Arch Linux**: Dukungan alat pentesting.

---

## 🌟 Kontribusi

Ingin berkontribusi? Fork repo ini, buat perubahan, dan ajukan pull request. Pastikan kode sesuai standar `pylint` dan diuji di Arch Linux.

```bash
pylint unknown1337.py
```

⭐ **Star** repo ini di GitHub jika kamu merasa proyek ini membantu!

---

**⚠️ Catatan Hukum**: Selalu dapatkan izin sebelum melakukan pengujian keamanan. Penulis tidak bertanggung jawab atas penyalahgunaan alat ini.
