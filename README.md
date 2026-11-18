# NR AI v0.3 — web/PWA + Android wrapper starter

## Fitur versi 0.3
- Website responsif untuk HP dan desktop.
- AI Chat melalui backend FastAPI + Ollama lokal.
- Riwayat chat tersimpan di perangkat (localStorage).
- Pengaturan alamat backend, berguna saat aplikasi Android mengakses server di jaringan lokal.
- Tombol salin prompt untuk video, gambar, dan musik.
- AI Voice memakai text-to-speech browser/perangkat.
- Scaffold Capacitor untuk membungkus frontend menjadi proyek Android.

## A. Jalankan AI Chat di komputer
Prasyarat: Python 3.11+ dan Ollama.

1. Pasang Ollama dari https://ollama.com
2. Jalankan model: `ollama pull qwen2.5:3b`
3. Dari folder proyek, buat virtual environment dan instal:
   - `python -m venv .venv`
   - Windows: `.venv\\Scripts\\activate`
   - macOS/Linux: `source .venv/bin/activate`
   - `pip install -r requirements.txt`
4. Jalankan server dari folder proyek:
   `uvicorn backend.main:app --reload`
5. Buka `http://127.0.0.1:8000`

Pastikan Ollama berjalan. Model 3B membutuhkan RAM dan CPU yang memadai; kecepatannya bergantung perangkat.

## B. Akses dari HP di jaringan Wi-Fi yang sama
1. Jalankan backend di komputer dengan:
   `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
2. Cari alamat IP lokal komputer (misalnya `192.168.1.10`).
3. Buka NR AI di HP atau aplikasi Android.
4. Tekan tombol **Server** dan isi `http://IP-KOMPUTER:8000`.
5. Pastikan firewall komputer mengizinkan koneksi pada port 8000. Jangan mengekspos Ollama port 11434 ke internet.

## C. Buat proyek Android (perlu komputer)
Prasyarat: Node.js LTS, Android Studio, Android SDK, dan JDK sesuai versi Android Studio.

1. Dari folder proyek:
   `npm install`
2. Tambahkan platform Android:
   `npm run android:add`
3. Sinkronkan aset:
   `npm run sync`
4. Buka Android Studio:
   `npm run open:android`
5. Di Android Studio, uji di emulator/perangkat. Untuk APK, gunakan menu Build > Build Bundle(s) / APK(s) > Build APK(s).

Ini adalah scaffold proyek Android, bukan file APK siap pasang. APK final harus dibangun dan diuji dengan Android Studio.

## Status fitur
- AI Chat: berjalan jika backend FastAPI dan Ollama aktif.
- Video AI: prompt builder saja, belum menghasilkan MP4.
- Gambar AI: prompt builder saja, belum menghasilkan file gambar.
- Musik AI: prompt builder saja, belum menghasilkan audio musik.
- Voice: text-to-speech browser/perangkat, ketersediaan suara tergantung perangkat.

## Catatan penting
Tidak ada jaminan generator video/gambar/musik tanpa batas dan gratis. Model generatif memerlukan GPU, RAM, penyimpanan, listrik, dan/atau hosting. Integrasi model perlu dipilih berdasarkan kemampuan perangkat, lisensi, dan kebijakan penggunaannya. Jangan menyimpan API key rahasia di frontend.

## D. Membuat APK hanya dengan HP Android (build cloud)
File workflow GitHub Actions sudah disertakan di `.github/workflows/build-android.yml`. Kompilasi dilakukan oleh server GitHub, bukan oleh HP.

1. Buat akun atau masuk ke GitHub melalui browser HP: https://github.com
2. Buat repository baru, misalnya `nr-ai-app`.
3. Unggah seluruh isi folder proyek ini ke repository (termasuk folder tersembunyi `.github`). Jika unggah lewat web sulit, gunakan aplikasi GitHub atau fitur upload file pada halaman repository.
4. Buka tab **Actions** pada repository dan izinkan Actions jika diminta.
5. Pilih workflow **Build NR AI APK**, tekan **Run workflow**, lalu tunggu sampai selesai.
6. Buka hasil workflow yang berhasil, cari bagian **Artifacts**, lalu unduh `NR-AI-debug-APK`.
7. Ekstrak ZIP artifact dan pasang `app-debug.apk` di HP. Android mungkin meminta izin **Install unknown apps** untuk browser atau aplikasi file manager yang digunakan.

Jika proses gagal, buka hasil workflow dan lihat log merah pada langkah yang gagal. APK debug ini untuk pengujian/pemasangan pribadi, bukan APK rilis Play Store.

**Penting:** APK ini membungkus antarmuka NR AI. AI Chat masih membutuhkan backend NR AI + Ollama yang berjalan di komputer/server dan alamatnya diatur melalui tombol **Server**. Fitur video, gambar, dan musik pada versi ini masih pembuat prompt, belum generator media sungguhan.
