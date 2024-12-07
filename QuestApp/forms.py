from django import forms
from django.contrib.auth.models import User

from .models import Coach, Player, Achievement, Photo, Match, News, Team, Comment


class CoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = ['name', 'role']

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'position', 'biography', 'goals', 'assists', 'appearances']

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['year', 'title']

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['home_team', 'away_team', 'date', 'venue', 'home_team_score', 'away_team_score', 'is_live']

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'url']

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'slogan', 'history', 'image', 'logo']

class SupportForm(forms.Form):
    phone_number = forms.CharField(max_length=13, help_text="Enter your phone number in the format +2547XXXXXXXX")
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

class LineupForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['home_team_lineup', 'away_team_lineup']
        widgets = {
            'home_team_lineup': forms.CheckboxSelectMultiple,
            'away_team_lineup': forms.CheckboxSelectMultiple,
        }

class KeyPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['is_key_player']
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don’t match.')
        return cd['password2']
