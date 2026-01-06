from django.contrib import admin
from .models import Ideas, Comments, Votes

admin.site.register(Ideas)
admin.site.register(Comments)
admin.site.register(Votes)
