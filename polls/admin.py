from django.contrib import admin

# Register your models here.
from .models import Poll,Choice,Vote

admin.site.register([Poll,Choice,Vote])