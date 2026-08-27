from .models import ShortURL
from .utils import generate_short_code
import qrcode
from io import BytesIO
from .storage import upload_file

def create_short_url(original_url, expiry_date=None, custom_url=None):

    if custom_url:
        code = custom_url
        if ShortURL.objects.filter(short_code=code).exists():
            raise ValueError("This custom url is already taken")
    else:
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
    buffer.seek(0)

    filename = f"{obj.short_code}.png"
    public_url = upload_file(
        buffer.getvalue(),
        filename
    )
    obj.qr_code_url = public_url
    obj.save(update_fields=["qr_code_url"])