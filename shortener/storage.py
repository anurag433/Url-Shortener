from supabase import create_client
from django.conf import settings

supabase = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY
)


def upload_file(file_bytes: bytes, filename: str):

    bucket = settings.SUPABASE_BUCKET

    supabase.storage.from_(bucket).upload(
        path=filename,
        file=file_bytes,
        file_options={
            "content-type": "image/png",
            "upsert": "true"
        }
    )

    return supabase.storage.from_(bucket).get_public_url(filename)