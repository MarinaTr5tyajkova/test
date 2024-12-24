from django.contrib import messages  # Импортируем модуль сообщений
from django.views.generic import TemplateView, CreateView, FormView, ListView, DetailView
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm
from .models import Product
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Order

class HomePageView(TemplateView):
    template_name = 'shop/home.html'  # Шаблон для главной страницы

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all().order_by('-created_at')[:5]  # Получаем последние пять товаров
        return context


class RegistrationView(CreateView):
    form_class = RegistrationForm   # Используем форму регистрации
    template_name = 'shop/register.html'   # Шаблон страницы регистрации
    success_url = '/login/'   # Перенаправление после успешной регистрации

    def form_valid(self, form):
        response = super().form_valid(form)  # Сохраняем пользователя
        messages.success(self.request, "Вы успешно зарегистрированы! Пожалуйста, войдите.")  # Сообщение об успешной регистрации
        return response


class LoginView(FormView):
    form_class = LoginForm   # Используем форму входа 
    template_name = 'shop/login.html'   # Шаблон страницы входа 

    def form_valid(self, form):
        username = form.cleaned_data['username']   # Получаем имя пользователя из формы 
        password = form.cleaned_data['password']   # Получаем пароль из формы 
        user = authenticate(self.request, username=username, password=password)   # Проверяем учетные данные пользователя 
        if user is not None:   # Если пользователь найден 
            login(self.request, user)   # Входим в систему 
            messages.success(self.request, "Вы успешно вошли в систему!")  # Сообщение об успешной авторизации
            return redirect('home')   # Перенаправляем на главную страницу 
        else:
            form.add_error(None, "Неверный логин или пароль.")   # Добавляем ошибку если учетные данные неверны 
            return self.form_invalid(form)   # Возвращаем форму с ошибками 


class ProductListView(ListView):
    model = Product                      # Модель для отображения списка товаров 
    template_name = 'shop/product_list.html'  # Шаблон для отображения списка товаров 
    context_object_name = 'products'     # Имя контекста для списка товаров 


class ProductDetailView(DetailView):
    model = Product                       # Модель для отображения деталей товара 
    template_name = 'shop/product_detail.html'  # Шаблон для отображения деталей товара 


def logout_view(request):
    logout(request)                       # Выход пользователя из системы 
    messages.success(request, "Вы успешно вышли из системы!")  # Сообщение об успешном выходе 
    return redirect('home')               # Перенаправление на главную страницу 

class SearchResultsView(ListView):
    model = Product
    template_name = 'shop/search_results.html'  # Шаблон для отображения результатов поиска
    context_object_name = 'products'  # Имя контекста для списка товаров

    def get_queryset(self):
        query = self.request.GET.get('query')  # Получаем параметр 'query' из URL
        return Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))  # Фильтруем товары по имени или описанию

@login_required  # Ограничиваем доступ к странице профиля только для авторизованных пользователей
def profile_view(request):
    orders = Order.objects.filter(user=request.user)  # Получаем все заказы текущего пользователя
    return render(request, 'shop/profile.html', {'user': request.user, 'orders': orders})