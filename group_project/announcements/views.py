from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils import timezone
from .models import Announcement, Category
from .forms import AnnouncementForm

def announcement_list(request):
    announcements = Announcement.objects.all()
    categories = Category.objects.all()

    # Поиск
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

    context = {
        'announcements': announcements,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'status': status,
    }
    return render(request, 'announcements/list.html', context)

@login_required
def announcement_create(request):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('announcement_list')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            return redirect('announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'announcements/form.html', {'form': form, 'title': 'Создать объявление'})

@login_required
def announcement_edit(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if not request.user.groups.filter(name='Admin').exists() or announcement.author != request.user:
        return redirect('announcement_list')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcement_list')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'announcements/form.html', {'form': form, 'title': 'Редактировать объявление'})

@login_required
def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if not request.user.groups.filter(name='Admin').exists() or announcement.author != request.user:
        return redirect('announcement_list')

    if request.method == 'POST':
        announcement.delete()
        return redirect('announcement_list')
    return render(request, 'announcements/delete.html', {'announcement': announcement})
