from django.contrib import admin
from .models import Category, BoardGame, Listing

admin.site.register(Category)
admin.site.register(BoardGame)
admin.site.register(Listing)
