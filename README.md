# 📦 Django Project Setup with MySQL Database

Panduan ini akan membantu Anda untuk:
- Menginstal Python & Django
- Membuat dan menjalankan proyek Django
- Menghubungkan MySQL sebagai database backend

---

## 🐍 1. Instalasi Python

Pastikan Python 3.8+ sudah terinstal. Jika belum, unduh dari [https://www.python.org/downloads/](https://www.python.org/downloads/)

Cek versi:
```bash
python --version
# atau
python3 --version
```

---

## 🔧 2. Membuat Virtual Environment

```bash
# Buat virtualenv
python -m venv venv

# Aktifkan virtualenv
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

---

## 📦 3. Instalasi Django dan MySQL Client

```bash
pip install django
pip install mysqlclient
```

> Jika gagal install `mysqlclient`, pastikan Anda sudah menginstal library development dari MySQL:

- **Windows**: Instal MySQL dan tambahkan ke PATH.
- **Ubuntu/Debian**:
  ```bash
  sudo apt install libmysqlclient-dev python3-dev
  ```

---

## 🚀 4. Membuat Proyek Django

```bash
django-admin startproject myproject
cd myproject
python manage.py migrate
python manage.py runserver
```

Akses di browser: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🗄️ 5. Menghubungkan Django dengan MySQL

Edit file `myproject/settings.py` pada bagian `DATABASES`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nama_database',
        'USER': 'nama_user_mysql',
        'PASSWORD': 'password_mysql',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Setelah konfigurasi, jalankan migrasi awal:

```bash
python manage.py migrate
```

---

## 🧪 6. Menjalankan Server

```bash
python manage.py runserver
```

Buka di browser: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📝 Catatan Tambahan

- Pastikan database MySQL sudah dibuat terlebih dahulu.
- Gunakan `.env` file atau library seperti `python-decouple` untuk menyimpan kredensial database di production.
- Untuk memulai app baru:
  ```bash
  python manage.py startapp nama_app
  ```

---

## ✅ Selesai!

Selamat, proyek Django Anda sekarang sudah siap digunakan dan terhubung ke MySQL 🎉

## develop by dani hartanto