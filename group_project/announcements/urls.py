from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.announcement_list, name='announcement_list'),
    path('<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('create/', views.announcement_create, name='announcement_create'),
    path('<int:pk>/edit/', views.announcement_edit, name='announcement_edit'),
    path('<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', LogoutView.as_view(next_page='announcement_list'), name='logout'),
    path('<int:pk>/like/', views.toggle_like, name='toggle_like'),
]