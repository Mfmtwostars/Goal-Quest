from django.contrib import admin

from QuestApp.models import Team, Player, Highlight, Photo, Match, Coach, Achievement, News, Comment, NewsArticle, \
    Interview, SpecialFeature, Category, Product

# Register your models here.
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Coach)
admin.site.register(Achievement)
admin.site.register(Highlight)
admin.site.register(Photo)
admin.site.register(Match)
admin.site.register(News)
admin.site.register(Comment)
admin.site.register(NewsArticle)
admin.site.register(Interview)
admin.site.register(SpecialFeature)
admin.site.register(Category)
admin.site.register(Product)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'date', 'venue', 'home_team_score', 'away_team_score', 'is_live')
    list_filter = ('date', 'is_live')
    search_fields = ('home_team', 'away_team', 'venue')

class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'author')
    list_filter = ('published_date',)

class InterviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'interviewee', 'published_date')
    search_fields = ('title', 'author', 'interviewee')
    list_filter = ('published_date',)
