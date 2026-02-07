from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="categories/common/", blank=True, null=True)
    mobile_image = models.ImageField(
        upload_to="categories/mobile/",
        blank=True,
        null=True
    )
    mobile_secondary_image = models.ImageField(
        upload_to="categories/mobile_secondary/",
        blank=True,
        null=True
    )
    desktop_image = models.ImageField(
        upload_to="categories/desktop/",
        blank=True,
        null=True
    )
    desktop_secondary_image = models.ImageField(
        upload_to="categories/desktop_secondary",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
