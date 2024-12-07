from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=100)
    slogan = models.CharField(max_length=255)
    history = models.TextField()
    image = models.ImageField(upload_to='team_images/', null=True, blank=True)
    coaches = models.ManyToManyField('Coach')
    logo = models.ImageField(upload_to='team_logos/', null=True, blank=True)
    players = models.ManyToManyField('Player')
    achievements = models.ManyToManyField('Achievement')
    photos = models.ManyToManyField('Photo', related_name='team_photos')
    upcoming_matches = models.ManyToManyField('Match', related_name='upcoming_matches')
    news = models.ManyToManyField('News')

    def __str__(self):
        return self.name


class Coach(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Achievement(models.Model):
    year = models.IntegerField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Highlight(models.Model):
    year = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.description


class Photo(models.Model):
    image = models.ImageField(upload_to='team_images/', null=True, blank=True, default='default.jpg')
    caption = models.CharField(max_length=255)

    def __str__(self):
        return self.caption


class News(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.title

class Player(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    biography = models.TextField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    appearances = models.IntegerField()
    highlights = models.ManyToManyField('Highlight')
    photos = models.ManyToManyField('Photo', related_name='player_photos')
    news = models.ManyToManyField('News')
    is_key_player = models.BooleanField(default=False)  # Add a field to mark key players

    def __str__(self):
        return self.name

class Match(models.Model):
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    date = models.DateTimeField()
    venue = models.CharField(max_length=100)
    home_team_score = models.IntegerField(null=True, blank=True)
    away_team_score = models.IntegerField(null=True, blank=True)
    is_live = models.BooleanField(default=False)
    home_team_lineup = models.ManyToManyField(Player, related_name='home_team_lineup')
    away_team_lineup = models.ManyToManyField(Player, related_name='away_team_lineup')

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date.strftime('%Y-%m-%d %H:%M')}"
class Comment(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.author} on {self.match}"

class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class Interview(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=100)
    interviewee = models.CharField(max_length=100)
    image = models.ImageField(upload_to='interview_images/', null=True, blank=True)

    def __str__(self):
        return self.title
class SpecialFeature(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart {self.id} for {self.user.username}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
