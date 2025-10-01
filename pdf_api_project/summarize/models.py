from django.db import models

class PDFSummaryAudit(models.Model):
    url = models.URLField(unique=True)
    extracted_text = models.TextField()
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary for {self.url}"
