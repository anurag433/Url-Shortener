from .models import ShortURL
from .utils import generate_short_code

def create_short_url(original_url):

    while True:
        code = generate_short_code()

        if not ShortURL.objects.filter(short_code=code).exists():
            break
    
    return ShortURL.objects.create(
        original_url=original_url,
        short_code=code
    )