from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Announcement, Category, Comment, Like
from .forms import AnnouncementForm, CommentForm

# Monkey patch for Django 6.0.1 paginator bug
def validate_number(self, number):
    try:
        number = int(number)
    except (TypeError, ValueError):
        raise PageNotAnInteger("Page number is not an integer")
    if number < 1:
        raise EmptyPage("Page number is less than 1")
    if number > self.num_pages:
        if number == 1 and self.num_pages == 0:
            pass
        else:
            raise EmptyPage("Page number is greater than number of pages")
    return number

def _validate_number(self, number):
    return validate_number(self, number)

Paginator.validate_number = validate_number
Paginator._validate_number = _validate_number

@login_required
def toggle_like(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, announcement=announcement)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    if request.is_ajax() or request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'likes_count': announcement.likes.count()})
    return redirect('announcement_detail', pk=pk)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Announcement, Category, Comment, Like
from .forms import AnnouncementForm, CommentForm

# Monkey patch for Django 6.0.1 paginator bug
def validate_number(self, number):
    try:
        number = int(number)
    except (TypeError, ValueError):
        raise PageNotAnInteger("Page number is not an integer")
    if number < 1:
        raise EmptyPage("Page number is less than 1")
    if number > self.num_pages:
        if number == 1 and self.num_pages == 0:
            pass
        else:
            raise EmptyPage("Page number is greater than number of pages")
    return number

def _validate_number(self, number):
    return validate_number(self, number)

Paginator.validate_number = validate_number
Paginator._validate_number = _validate_number

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('announcement_list')
        else:
            messages.error(request, 'Невірне ім\'я користувача або пароль.')
    return render(request, 'announcements/login.html')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Добавить в группу Student
            student_group = Group.objects.get(name='Student')
            user.groups.add(student_group)
            login(request, user)
            messages.success(request, 'Реєстрація успішна!')
            return redirect('announcement_list')
    else:
        form = UserCreationForm()
    return render(request, 'announcements/register.html', {'form': form})

def announcement_list(request):
    announcements = Announcement.objects.all()
    categories = Category.objects.all()


    query = request.GET.get('q')
    if query:
        announcements = announcements.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    # Фильтр по категории
    category_id = request.GET.get('category')
    if category_id:
        announcements = announcements.filter(category_id=category_id)

    # Фильтр по статусу (активные/истекшие)
    status = request.GET.get('status')
    if status == 'active':
        announcements = announcements.filter(end_date__gte=timezone.now().date())
    elif status == 'expired':
        announcements = announcements.filter(end_date__lt=timezone.now().date())

    # Пагинация
    paginator = Paginator(announcements, 10)  # 10 объявлений на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'announcements': page_obj,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'status': status,
        'is_admin': request.user.is_authenticated and request.user.groups.filter(name='Admin').exists(),
    }
    return render(request, 'announcements/list.html', context)

@login_required
def announcement_create(request):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('announcement_list')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            return redirect('announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'announcements/form.html', {'form': form, 'title': 'Створити оголошення'})

@login_required
def announcement_edit(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if not request.user.groups.filter(name='Admin').exists() or announcement.author != request.user:
        return redirect('announcement_list')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcement_list')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'announcements/form.html', {'form': form, 'title': 'Редагувати оголошення'})

def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    comments = announcement.comments.all().order_by('-created_at')
    comment_form = CommentForm()

    liked = False
    if request.user.is_authenticated:
        liked = announcement.likes.filter(user=request.user).exists()

    context = {
        'announcement': announcement,
        'comments': comments,
        'comment_form': comment_form,
        'is_admin': request.user.is_authenticated and request.user.groups.filter(name='Admin').exists(),
        'liked': liked,
    }
    return render(request, 'announcements/detail.html', context)

@login_required
def add_comment(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.announcement = announcement
            comment.author = request.user
            comment.save()
            messages.success(request, 'Коментар додано!')
            return redirect('announcement_detail', pk=pk)
    else:
        form = CommentForm()
    return redirect('announcement_detail', pk=pk)

@login_required
def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if not request.user.groups.filter(name='Admin').exists() or announcement.author != request.user:
        return redirect('announcement_list')

    if request.method == 'POST':
        announcement.delete()
        return redirect('announcement_list')
    return render(request, 'announcements/delete.html', {'announcement': announcement})
