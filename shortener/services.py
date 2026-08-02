from .models import ShortURL
from .utils import generate_short_code
import qrcode
from io import BytesIO
from django.core.files import File

def create_short_url(original_url, expiry_date=None):

    while True:
        code = generate_short_code()

        if not ShortURL.objects.filter(short_code=code).exists():
            break
    
    return ShortURL.objects.create(
        original_url=original_url,
        short_code=code,
        expiry_date=expiry_date
    )

def generate_qr(obj, short_url):
    qr = qrcode.make(short_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    filename = f"{obj.short_code}.png"
    obj.qr_code.save(
        filename,
        File(buffer),
        save=True
    )