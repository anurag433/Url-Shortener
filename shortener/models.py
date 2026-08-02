from django.db import models

class ShortURL(models.Model):

    original_url = models.URLField(max_length=2048) 
    short_code = models.CharField(
        max_length = 5 ,
        unique = True    
    )
    created_at = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(
        null=True,
        blank=True
    )
    clicks = models.IntegerField(default=0)
    qr_code = models.ImageField(
        upload_to="qr_codes/",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.short_code
