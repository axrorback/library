from django.db import models
from django.utils.text import slugify
import uuid
from django_ckeditor_5.fields import CKEditor5Field

class Book(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    description = CKEditor5Field(config_name='default')

    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255, blank=True)

    language = models.ForeignKey(
        "library.Language",
        on_delete=models.PROTECT,
        related_name="books",
        null=True,
        blank=True
    )
    categories = models.ManyToManyField(
        "library.Category",
        related_name="books",
        blank=True
    )

    publication_year = models.PositiveIntegerField(null=True, blank=True)

    pages = models.PositiveIntegerField(null=True, blank=True)

    cover = models.ImageField(
        upload_to="books/covers/",
        null=True,
        blank=True
    )

    file = models.FileField(
        upload_to="books/files/",
        help_text="PDF, EPUB, DOCX"
    )

    file_size = models.PositiveIntegerField(help_text="Bytes", editable=False)

    views_count = models.PositiveIntegerField(default=0)
    downloads_count = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=Status,
        default=Status.DRAFT
    )

    is_free = models.BooleanField(default=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["author"]),
            models.Index(fields=["status"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.file and not self.file_size:
            self.file_size = self.file.size

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title