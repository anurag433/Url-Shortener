from datetime import timedelta

from django.utils import timezone

from .models import ShortURL
from .storage import delete_file
from core.cache import delete_from_cache


def cleanup_old_urls():
    today = timezone.localdate()
    cutoff_date = today - timedelta(days=30)
    deleted_count = 0
    urls = ShortURL.objects.all()

    for obj in urls:
        delete_link = False

        if obj.created_at <= cutoff_date:
            delete_link = True

        elif obj.expiry_date and obj.expiry_date < today:
            delete_link = True

        if delete_link:
            try:
                delete_file(f"{obj.short_code}.png")
            except Exception:
                pass
            try:
                delete_from_cache(obj.short_code)
            except Exception:
                pass

            obj.delete()
            deleted_count += 1

    return {
        "deleted_links": deleted_count
    }