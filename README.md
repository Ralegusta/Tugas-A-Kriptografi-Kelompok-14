# Aplikasi Web Simple Cipher

Aplikasi web sederhana yang dibangun menggunakan Flask untuk mengenkripsi dan mendekripsi teks dan file menggunakan beberapa algoritma cipher klasik. Proyek ini dibuat sebagai bagian dari tugas mata kuliah Kriptografi.

## Fitur

- Enkripsi dan dekripsi untuk input teks manual maupun unggah file.
- Mendukung 6 jenis algoritma cipher klasik:
  1.  **Shift Cipher**: Mendukung teks dan file.
  2.  **Substitution Cipher**: Hanya mendukung teks.
  3.  **Affine Cipher**: Hanya mendukung teks.
  4.  **Vigenere Cipher**: Hanya mendukung teks.
  5.  **Hill Cipher**: Hanya mendukung teks.
  6.  **Permutation Cipher**: Mendukung teks dan file.
- Cipherteks ditampilkan dalam format kelompok 5 huruf untuk keterbacaan.
- Hasil enkripsi/dekripsi file dapat langsung diunduh, dengan nama file asli yang dipertahankan saat dekripsi.

## Cara Menjalankan Program

1.  **Clone Repositori**
    ```bash
    git clone https://github.com/Ralegusta/Tugas-A-Kriptografi-Kelompok-14.git
    cd Tugas-A-Kriptografi-Kelompok-14
    ```

2.  **Buat dan Aktifkan Virtual Environment**
    ```bash
    # Membuat virtual environment
    python -m venv .venv

    # Mengaktifkan di Windows (PowerShell)
    .\.venv\Scripts\activate
    ```

3.  **Install Dependensi**
    Pastikan virtual environment aktif (ditandai dengan adanya tulisan (.venv) berwarna hijau ), lalu jalankan:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan Aplikasi Flask**
    ```bash
    flask run
    ```

5.  **Buka di Browser**
    Buka browser web Anda dan kunjungi alamat `http://127.0.0.1:5000`.

## Catatan Tambahan

- Beberapa cipher (Substitution, Affine, Vigenere, Hill) hanya diimplementasikan untuk input teks karena operasinya berbasis alfabet (modulo 26) dan tidak cocok untuk data biner.
- Program ini berjalan dalam mode debug, yang akan menampilkan pesan error pada terminal jika terjadi error.