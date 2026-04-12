from django.urls import path
from . import views

urlpatterns = [
    path('',                  views.index,           name='index'),
    path('register/',         views.register_view,   name='register'),
    path('login/',            views.login_view,       name='login'),
    path('logout/',           views.logout_view,      name='logout'),
    path('dashboard/',        views.dashboard,        name='dashboard'),
    path('booking/',          views.booking_view,     name='booking'),
    path('booking/success/',  views.booking_success,  name='booking_success'),
    path('booking/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('contact/',          views.contact_view,     name='contact'),
    path('contact/success/',  views.contact_success,  name='contact_success'),
]