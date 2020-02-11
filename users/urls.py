from django.urls import path
from .views import (FrontLoginView, FrontLogoutView, FrontPasswordResetView,
    TemplateResetView, FrontPasswordResetConfirmView, TemplateResetDoneView,
    TemplateAccountView, FrontPasswordChangeView)

#namespace is '/accounts/'
urlpatterns = [
    path('profile/', TemplateAccountView.as_view(),
        name='profile'),
    path('login/', FrontLoginView.as_view(),
        name='front_login'),
    path('logout/', FrontLogoutView.as_view(),
        name='front_logout'),
    path('password_reset/', FrontPasswordResetView.as_view(),
        name='front_password_reset'),
    path('password_reset/done/', TemplateResetView.as_view(),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', FrontPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path('reset/done/', TemplateResetDoneView.as_view(),
        name='password_reset_complete'),
    path('password_change/', FrontPasswordChangeView.as_view(),
        name='password_change'),
    ]
