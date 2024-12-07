
from django.contrib import admin
from django.urls import path

from QuestApp import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.base, name='base'),
    path('', views.index, name='home'),
    path('team/', views.team_list, name='team_list'),
    path('team/<int:team_id>/', views.team_profile, name='team_profile'),
    path('team/add/', views.add_team, name='add_team'),
    path('team/<int:team_id>/edit/', views.edit_team, name='edit_team'),
    path('team/<int:team_id>/delete/', views.delete_team, name='delete_team'),
    path('team/<int:team_id>/add_coach/', views.add_coach, name='add_coach'),
    path('team/<int:team_id>/add_player/', views.add_player, name='add_player'),
    path('team/<int:team_id>/add_achievement/', views.add_achievement, name='add_achievement'),
    path('team/<int:team_id>/add_photo/', views.add_photo, name='add_photo'),
    path('team/<int:team_id>/add_match/', views.add_match, name='add_match'),
    path('team/<int:team_id>/add_news/', views.add_news, name='add_news'),
    path('player/<int:player_id>/', views.player_profile, name='player_profile'),
    path('player/<int:player_id>/edit/', views.edit_player, name='edit_player'),
    path('player/<int:player_id>/delete/', views.delete_player, name='delete_player'),
    path('team/<int:team_id>/support/', views.support_team, name='support_team'),
    path('matches/', views.match_list, name='match_list'),
    path('matches/<int:match_id>/', views.match_detail, name='match_detail'),
    path('api/live_scores/<int:match_id>/', views.live_scores, name='live_scores'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:article_id>/', views.news_detail, name='news_detail'),
    path('interviews/', views.interview_list, name='interview_list'),
    path('interviews/<int:interview_id>/', views.interview_detail, name='interview_detail'),
    path('contact/', views.contact, name='contact'),
    path('latest_news/', views.latest_news, name='latest_news'),
    path('upcoming_matches/', views.upcoming_matches, name='upcoming_matches'),
    path('special_features/', views.special_features, name='special_features'),
    path('shop/', views.shop_home, name='shop_home'),
    path('shop/category/<int:category_id>/', views.product_list, name='product_list'),
    path('about/', views.about, name='about'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('support/', views.support, name='support'),
    path('faq/', views.faq, name='faq'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout_success/', views.checkout_success, name='checkout_success'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),




]