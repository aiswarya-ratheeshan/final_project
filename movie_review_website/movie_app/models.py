from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)


    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def __str__(self):
        return '{}'.format(self.name)

class Movies(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    username = models.CharField(max_length=250)
    poster = models.ImageField(upload_to='gallery',blank=True)
    category = models.CharField(max_length=250)
    desc = models.TextField(blank=True)
    release_date = models.DateField()
    actor = models.CharField(max_length=250)
    director = models.CharField(max_length=250)
    writer = models.CharField(max_length=250)

    movie_link = models.URLField(max_length=200)

    class Meta:
        ordering = ('title',)
        verbose_name = 'movie'
        verbose_name_plural = 'movies'



    def __str__(self):
        return '{}'.format(self.title)

class FavMovies(models.Model):
    favtitle = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    username = models.CharField(max_length=250)
    poster = models.ImageField(upload_to='gallery',blank=True)
    category = models.CharField(max_length=250)
    desc = models.TextField(blank=True)
    release_date = models.DateField()
    actor = models.CharField(max_length=250)
    director = models.CharField(max_length=250)
    writer = models.CharField(max_length=250)

    movie_link = models.URLField(max_length=200)

    class Meta:
        ordering = ('favtitle',)
        verbose_name = 'favmovie'
        verbose_name_plural = 'favmovies'



    def __str__(self):
        return '{}'.format(self.favtitle)
class Review(models.Model):
    username=models.CharField(max_length=250)
    movie=models.CharField(max_length=250)
    date=models.DateField(auto_now=True)
    review=models.CharField(max_length=250)

    def __str__(self):
        return '{}'.format(self.username)


