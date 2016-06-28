from django.contrib import admin
from .models import Document, FlatPage, Publication


admin.site.register(Document)
admin.site.register(FlatPage)
admin.site.register(Publication)