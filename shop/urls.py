from django.urls import path
from .views import HomePageView, RegistrationView, LoginView, ProductListView, ProductDetailView, logout_view, SearchResultsView, profile_view

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('logout/', logout_view, name='logout'),
    path('search_result/', SearchResultsView.as_view(), name='search_result'),
    path('profile/', profile_view, name='profile'),  # Страница профиля по адресу /profile/
]