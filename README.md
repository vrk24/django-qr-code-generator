# QR Code Generator – Django 🧾📱

A Django web application to generate QR codes for restaurant digital menus.
Users can generate QR codes and download them in **PNG** or **PDF** format.

## 🚀 Features
- Generate QR code from URL
- Download as PNG
- Download as styled PDF
- Bootstrap UI
- Modal-based format selection

## 🛠 Tech Stack
- Python
- Django
- qrcode
- ReportLab
- Bootstrap 5

QR-CODE-DJANGO/
│
├── django_qr/
│   ├── static/
│   │   └── qr_result.css
│   ├── templates/
│   │   ├── generate_qr_code.html
│   │   └── qr_result.html
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── settings.py
│
├── manage.py
├── README.md
├── .gitignore

## ▶️ How to Run Locally

```bash
git clone https://github.com/your-username/qr-code-django.git

cd qr-code-django

python -m venv env

env\Scripts\activate

pip install -r requirements.txt

IDEAL FINAL STRUCTURE (WHAT IT SHOULD LOOK LIKE)

python manage.py runserver

