# portfolio/utils.py

import os
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def link_callback(uri, rel):
    """
    Mengonversi URI HTML (seperti path ke CSS atau gambar)
    ke path file sistem yang absolut.
    """
    if uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT or settings.STATICFILES_DIRS[0], uri.replace(settings.STATIC_URL, ""))
        if not os.path.isfile(path):
            for static_dir in settings.STATICFILES_DIRS:
                path = os.path.join(static_dir, uri.replace(settings.STATIC_URL, ""))
                if os.path.isfile(path):
                    break
    else:
        return uri
    return path

def render_to_pdf(template_path, context_dict={}):
    """
    Fungsi untuk merender template Django menjadi respons PDF.
    """
    template = get_template(template_path)
    html = template.render(context_dict)
    
    result = BytesIO()
    
    pdf = pisa.CreatePDF(
        BytesIO(html.encode("UTF-8")),
        dest=result,
        encoding='UTF-8',
        link_callback=link_callback  # <-- Ini penting untuk memuat CSS
    )

    if pdf.err:
        return HttpResponse("Invalid PDF", status_code=400, content_type='text/plain')
    
    return HttpResponse(result.getvalue(), content_type='application/pdf')