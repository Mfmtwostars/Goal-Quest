from django.shortcuts import render, redirect, get_object_or_404
from QuestApp.models import Team, Coach, Player, Achievement, Photo, Match, News,Comment,NewsArticle, Interview,SpecialFeature,Category, Product,Cart, CartItem
from QuestApp.forms import CoachForm, PlayerForm, AchievementForm, PhotoForm, MatchForm, NewsForm,TeamForm,SupportForm,LineupForm, KeyPlayerForm, CommentForm,UserRegistrationForm
import requests, logging, json, base64,re
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail

from datetime import datetime
# Create your views here.
def index(request):
    return render(request, 'index.html')
def base(request):
        return render(request, 'base.html')

def team_list(request):
    teams = Team.objects.all()
    return render(request, 'team_list.html', {'teams': teams})

def team_profile(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    return render(request, 'team_profile.html', {'team': team})

def player_profile(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    return render(request, 'player_profile.html', {'player': player})

def add_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('team_list')
    else:
        form = TeamForm()
    return render(request, 'add_team.html', {'form': form})

def add_coach(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        form = CoachForm(request.POST)
        if form.is_valid():
            coach = form.save()
            team.coaches.add(coach)
            return redirect('team_profile', team_id=team_id)
    else:
        form = CoachForm()
    return render(request, 'add_coach.html', {'form': form, 'team': team})

def add_player(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save()
            team.players.add(player)
            return redirect('team_profile', team_id=team_id)
    else:
        form = PlayerForm()
    return render(request, 'add_player.html', {'form': form, 'team': team})

def add_achievement(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        form = AchievementForm(request.POST)
        if form.is_valid():
            achievement = form.save()
            team.achievements.add(achievement)
            return redirect('team_profile', team_id=team_id)
    else:
        form = AchievementForm()
    return render(request, 'add_achievement.html', {'form': form, 'team': team})

def add_photo(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            team.photos.add(photo)
            return redirect('team_profile', team_id=team_id)
    else:
        form = PhotoForm()
    return render(request, 'add_photo.html', {'form': form, 'team': team})

def add_match(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save()
            team.upcoming_matches.add(match)
            return redirect('team_profile', team_id=team_id)
    else:
        form = MatchForm()
    return render(request, 'add_match.html', {'form': form, 'team': team})

def add_news(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save()
            team.news.add(news)
            return redirect('team_profile', team_id=team_id)
    else:
        form = NewsForm()
    return render(request, 'add_news.html', {'form': form, 'team': team})

def edit_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            return redirect('team_profile', team_id=team_id)
    else:
        form = TeamForm(instance=team)
    return render(request, 'edit_team.html', {'form': form, 'team': team})

def delete_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        team.delete()
        return redirect('team_list')
    return render(request, 'delete_team.html', {'team': team})

def edit_player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            form.save()
            return redirect('player_profile', player_id=player_id)
    else:
        form = PlayerForm(instance=player)
    return render(request, 'edit_player.html', {'form': form, 'player': player})

def delete_player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    if request.method == 'POST':
        player.delete()
        return redirect('team_profile', team_id=player.team.id)
    return render(request, 'delete_player.html', {'player': player})
logger = logging.getLogger(__name__)

def latest_news(request):
    news_list = NewsArticle.objects.all().order_by('-published_date')[:10]
    return render(request, 'latest_news.html', {'news_list': news_list})

def upcoming_matches(request):
    match_list = Match.objects.filter(date__gte=timezone.now()).order_by('date')[:10]
    return render(request, 'upcoming_matches.html', {'match_list': match_list})

def special_features(request):
    feature_list = SpecialFeature.objects.all().order_by('-date')[:10]
    return render(request, 'special_features.html', {'feature_list': feature_list})

def validate_phone_number(phone_number):
    pattern = re.compile(r'^\+254\d{9}$')
    if pattern.match(phone_number):
        return True
    return False
logger = logging.getLogger(__name__)

def get_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_url, auth=(consumer_key, consumer_secret))
    logger.info(f"MPESA Access Token Response: {response.text}")
    try:
        mpesa_access_token = json.loads(response.text)
        validated_mpesa_access_token = mpesa_access_token['access_token']
        return validated_mpesa_access_token
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Error parsing access token: {e}")
        logger.error(f"Response Text: {response.text}")
        return None
def lipa_na_mpesa_online(phone_number, amount):
    access_token = get_access_token()

    if not access_token:
        return None

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer {}".format(access_token)}
    request = {
        "BusinessShortCode": "174379",
        "Password": "YourPassword",
        "Timestamp": "YourTimestamp",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": "174379",
        "PhoneNumber": phone_number,
        "CallBackURL": "https://yourcallbackurl.com/callback",
        "AccountReference": "GoalQuest",
        "TransactionDesc": "Payment for GoalQuest Support"
    }

    response = requests.post(api_url, json=request, headers=headers)

    if response.status_code == 200:
        try:
            return json.loads(response.text)
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}")
            logger.error(f"Response Text: {response.text}")
            return None
    else:
        logger.error(f"Error: {response.status_code} - {response.text}")
        return None

def support_team(request, team_id):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            amount = form.cleaned_data['amount']

            if not validate_phone_number(phone_number):
                return JsonResponse({'error': 'Invalid phone number format. Please use +254xxxxxxxxx format.'}, status=400)

            response = lipa_na_mpesa_online(phone_number, amount)
            if response:
                return render(request, 'payment_success.html', {'response': response})
            else:
                return JsonResponse({'error': 'Payment request failed.'}, status=500)
    else:
        form = SupportForm()
    return render(request, 'support_team.html', {'form': form, 'team_id': team_id})

def match_list(request):
    upcoming_matches = Match.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'match_list.html', {'upcoming_matches': upcoming_matches})

def match_detail(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    comments = Comment.objects.filter(match=match).order_by('-created_date')

    if request.method == 'POST':
        lineup_form = LineupForm(request.POST, instance=match)
        keyplayer_forms = [KeyPlayerForm(request.POST, instance=player) for player in
                           match.home_team_lineup.all().union(match.away_team_lineup.all())]
        comment_form = CommentForm(request.POST)

        if lineup_form.is_valid() and comment_form.is_valid():
            lineup_form.save()
            comment = comment_form.save(commit=False)
            comment.match = match
            comment.save()
            for form in keyplayer_forms:
                if form.is_valid():
                    form.save()
            return redirect('match_detail', match_id=match_id)
    else:
        lineup_form = LineupForm(instance=match)
        keyplayer_forms = [KeyPlayerForm(instance=player) for player in
                           match.home_team_lineup.all().union(match.away_team_lineup.all())]
        comment_form = CommentForm()

    return render(request, 'match_detail.html', {
        'match': match,
        'comments': comments,
        'lineup_form': lineup_form,
        'keyplayer_forms': keyplayer_forms,
        'comment_form': comment_form,
    })


def live_scores(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    data = {
        'home_team_score': match.home_team_score,
        'away_team_score': match.away_team_score,
    }
    return JsonResponse(data)

def news_list(request):
    news_articles = NewsArticle.objects.all().order_by('-published_date')
    return render(request, 'news_list.html', {'news_articles': news_articles})

def news_detail(request, article_id):
    article = get_object_or_404(NewsArticle, pk=article_id)
    return render(request, 'news_detail.html', {'article': article})

def interview_list(request):
    interviews = Interview.objects.all().order_by('-published_date')
    return render(request, 'interview_list.html', {'interviews': interviews})

def interview_detail(request, interview_id):
    interview = get_object_or_404(Interview, pk=interview_id)
    return render(request, 'interview_detail.html', {'interview': interview})
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        send_mail(
            f"New contact form submission from {name}",
            message,
            settings.DEFAULT_FROM_EMAIL,
            ['contact@goalquestsoccer.com'],
            fail_silently=False,
        )
        messages.success(request, 'Thank you for reaching out to us! We will get back to you shortly.')
        return redirect('contact')

    return render(request, 'contact.html')

def shop_home(request):
    categories = Category.objects.all()
    return render(request, 'shop_home.html', {'categories': categories})

def product_list(request, category_id):
    products = Product.objects.filter(category_id=category_id)
    return render(request, 'product_list.html', {'products': products})
def about(request):
    return render(request, 'about.html')
def terms(request):
    return render(request, 'terms.html')
def privacy(request):
    return render(request, 'privacy.html')
def support(request):
    return render(request, 'support.html')
def faq(request):
    return render(request, 'faq.html')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, defaults={'created_at': timezone.now()})
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')

@login_required
def cart_detail(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        # Redirect to shop if no cart exists
        return redirect('shop_home')

    return render(request, 'cart_detail.html', {'cart': cart})


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())

    if request.method == 'POST':
        return render(request, 'checkout_success.html')

    return render(request, 'checkout.html', {'cart': cart, 'total_price': total_price})

def checkout_success(request):
    return render(request, 'checkout_success.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
