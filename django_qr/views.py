from django.shortcuts import render
from .forms import QRCodeForm
import qrcode
import os
from django.conf import settings
from django.http import FileResponse, Http404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm


def generate_qr_code(request):
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    if request.method == 'POST':
        form = QRCodeForm(request.POST)

        if form.is_valid():
            res_name = form.cleaned_data['restaurant_name']
            url = form.cleaned_data['url']

            safe_name = res_name.replace(" ", "_").lower()

            # ---------- PNG ----------
            png_name = f"{safe_name}_menu.png"
            png_path = os.path.join(settings.MEDIA_ROOT, png_name)

            qr = qrcode.make(url)
            qr.save(png_path)

            # ---------- PDF ----------
            pdf_name = f"{safe_name}_menu.pdf"
            pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_name)

            c = canvas.Canvas(pdf_path, pagesize=A4)
            width, height = A4

            # Background
            c.setFillColorRGB(0.96, 0.96, 0.96)
            c.rect(0, 0, width, height, fill=1)

            # Border
            c.setStrokeColorRGB(0.2, 0.2, 0.2)
            c.setLineWidth(3)
            c.rect(1 * cm, 1 * cm, width - 2 * cm, height - 2 * cm)

            # Title
            c.setFillColorRGB(0, 0, 0)
            c.setFont("Helvetica-Bold", 22)
            c.drawCentredString(width / 2, height - 3 * cm, res_name)

            # Subtitle
            c.setFont("Helvetica", 12)
            c.drawCentredString(
                width / 2,
                height - 4.2 * cm,
                "Scan to view our digital menu"
            )

            # QR Card
            card_width = 10 * cm
            card_height = 10 * cm
            card_x = (width - card_width) / 2
            card_y = (height - card_height) / 2 - 1 * cm

            c.setFillColorRGB(1, 1, 1)
            c.roundRect(card_x, card_y, card_width, card_height, 15, fill=1)

            # QR inside card
            qr_size = 8 * cm
            c.drawImage(
                png_path,
                card_x + (card_width - qr_size) / 2,
                card_y + (card_height - qr_size) / 2,
                qr_size,
                qr_size
            )

            # Footer
            c.setFont("Helvetica-Oblique", 9)
            c.setFillColorRGB(0.3, 0.3, 0.3)
            c.drawCentredString(
                width / 2,
                2 * cm,
                "Powered by QR Menu Generator"
            )

            c.showPage()
            c.save()

            # ---------- RESULT PAGE ----------
            return render(request, 'qr_result.html', {
                'qr_image_url': settings.MEDIA_URL + png_name,
                'res_name': res_name,
                'png_name': png_name,
                'pdf_name': pdf_name
            })

    else:
        form = QRCodeForm()

    return render(request, 'generate_qr_code.html', {'form': form})


def download_qr(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'),
                            as_attachment=True,
                            filename=filename)
    else:
        raise Http404("File not found")
