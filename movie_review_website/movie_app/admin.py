from django.contrib import admin
from .models import Movies, Category, FavMovies, Review


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class MoviesAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Movies, MoviesAdmin)


class FavMoviesAdmin(admin.ModelAdmin):
    list_display = ['favtitle', 'slug']
    prepopulated_fields = {'slug': ('favtitle',)}


admin.site.register(FavMovies, FavMoviesAdmin)
admin.site.register(Review)
