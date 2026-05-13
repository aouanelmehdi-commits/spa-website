import urllib.request
import urllib.parse
import json
def send_telegram(booking):
    try:
        token   = '8710037618:AAEVRb2GXqOHTBHsZPPWwVTGmoNsLQj3tKs'
        chat_id = '6005848408'
        
        message = f"""
🌿 New Booking!
👤 {booking.first_name} {booking.last_name}
📞 {booking.phone}
📧 {booking.email}
💆 {booking.service}
📅 {booking.date}
⏰ {booking.time}
        """.strip()

        data = urllib.parse.urlencode({
            'chat_id': chat_id,
            'text': message,
        }).encode()

        url = f'https://api.telegram.org/bot{token}/sendMessage'
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req)
        print("Telegram sent!")
    except Exception as e:
        print("Telegram error:", e)
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Booking, ContactMessage
def index(request):
    site_url = request.build_absolute_uri('/')
    return render(request, 'index.html', {'site_url': site_url})

# ── REGISTER ──
def register_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name  = request.POST['last_name']
        email      = request.POST['email']
        password   = request.POST['password']
        password2  = request.POST['password2']

        if password != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=email).exists():
            return render(request, 'register.html', {'error': 'Email already registered'})

        user = User.objects.create_user(
            username   = email,
            email      = email,
            password   = password,
            first_name = first_name,
            last_name  = last_name
        )
        login(request, user)
        return redirect('dashboard')
    return render(request, 'register.html')

# ── LOGIN ──
def login_view(request):
    if request.method == 'POST':
        email    = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')

# ── LOGOUT ──
def logout_view(request):
    logout(request)
    return redirect('login')

# ── DASHBOARD ──
@login_required(login_url='/login/')
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'bookings': bookings})

# ── BOOKING ──
def booking_view(request):
    if request.method == 'POST':
        try:
            booking = Booking.objects.create(
                user       = request.user if request.user.is_authenticated else None,
                first_name = request.POST['first_name'],
                last_name  = request.POST['last_name'],
                email      = request.POST['email'],
                phone      = request.POST['phone'],
                service    = request.POST['service'],
                date       = request.POST['date'],
                time       = request.POST['time'],
            )
            send_telegram(booking)
            return redirect('booking_success')
        except Exception as e:
            print("BOOKING ERROR:", e)
            return render(request, 'booking.html', {'error': str(e)})
    selected_service = request.GET.get('service', '')
    return render(request, 'booking.html', {'selected_service': selected_service})

def booking_success(request):
    return render(request, 'booking_success.html')


# ── CONTACT ──
def contact_view(request):
    if request.method == 'POST':
        try:
            ContactMessage.objects.create(
                first_name = request.POST['first_name'],
                last_name  = request.POST['last_name'],
                email      = request.POST['email'],
                phone      = request.POST.get('phone', ''),
                message    = request.POST['message'],
            )
            return redirect('contact_success')
        except Exception as e:
            return render(request, 'contact.html', {'error': str(e)})
    return render(request, 'contact.html')

def contact_success(request):
    return render(request, 'contact_success.html')
# ── CANCEL BOOKING ──
@login_required(login_url='/login/')
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
        booking.status = 'cancelled'
        booking.save()
    except Booking.DoesNotExist:
        pass
    return redirect('dashboard')