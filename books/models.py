from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import Profile


class Genre(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    favourite_of = models.ManyToManyField(User, blank=True, related_name='fav_genres')

    def clean(self):
        self.name = " ".join(map(str.capitalize, self.name.split(" ")))
        if self.name == '':
            raise ValidationError('Empty string is not a valid Genre name')

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100, unique=False)
    info = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='author_images')

    def clean(self):
        if len(self.info) < 200:
            raise ValidationError('author\'s info must be greater than 200')
        self.name = " ".join(map(str.capitalize, self.name.split(" ")))
        if self.name == '':
            raise ValidationError('Empty string is not a valid Author name')

    def __str__(self):
        return self.name


class Book(models.Model):
    ISBN = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    author = models.ManyToManyField(Author)
    genre = models.ManyToManyField(Genre)
    cover_image = models.ImageField(upload_to='book_images')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5)
    info = models.CharField(max_length=1000)
    released_date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)

    # objects = BookManager()

    def clean(self):
        if 0 < self.rating > 5 or self.rating < 0:
            raise ValidationError('rating should be less than or equal to 5 and less than equal to 0')
        self.name = " ".join(map(str.capitalize, self.name.split(" ")))
        if self.name == '':
            raise ValidationError('Empty string is not a valid Book name')
        if len(self.info) < 200:
            raise ValidationError('book info must be greater than 200')
        self.ISBN = self.ISBN.replace(" ", "").upper()

    def __str__(self):
        return self.name

    @property
    def available_stock(self):
        return self.entity_set.filter(deal_is_active=True).count()

    @property
    def in_stock(self):
        return self.available_stock > 0

    def get_genre_set(self):
        return self.genre.all()

    def get_all_authors(self):
        return self.author.values('name')

    def get_sold_stock(self):
        return self.entity_set.filter(deal_is_active=False).count()

    def get_first_hand_entities(self):
        return self.entity_set.filter(created_by__user__is_staff=True)

    def get_second_hand_entities(self):
        return self.entity_set.filter(created_by__user__is_staff=False)


class Entity(models.Model):
    product = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='entity_set')
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    deal_is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.name


"""
q = Q()
for i in d:
...     q |= Q(name__iexact=i)

functools.reduce(lambda acc,x: acc | Q(name__iexact=x), d, Q())
"""