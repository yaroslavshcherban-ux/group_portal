from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from announcements.models import Category, Announcement
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Create sample data'

    def handle(self, *args, **options):
        # Создать категории
        news = Category.objects.get_or_create(name='Новости', description='Школьные новости')[0]
        events = Category.objects.get_or_create(name='События', description='Школьные мероприятия')[0]
        important = Category.objects.get_or_create(name='Важное', description='Важные объявления')[0]

        # Создать пользователей
        admin_group = Group.objects.get(name='Admin')
        student_group = Group.objects.get(name='Student')

        admin_user = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})[0]
        admin_user.groups.add(admin_group)
        admin_user.set_password('admin123')
        admin_user.save()

        student_user = User.objects.get_or_create(username='student', defaults={'email': 'student@example.com'})[0]
        student_user.groups.add(student_group)
        student_user.set_password('student123')
        student_user.save()

        # Создать объявления
        Announcement.objects.get_or_create(
            title='Добро пожаловать в новый учебный год!',
            content='Уважаемые ученики и родители! Мы рады приветствовать вас в новом учебном году. Желаем успехов в учёбе!',
            category=news,
            author=admin_user,
            end_date=date.today() + timedelta(days=30),
            is_pinned=True
        )

        Announcement.objects.get_or_create(
            title='Родительское собрание',
            content='Родительское собрание состоится 15 марта в 18:00 в актовом зале.',
            category=events,
            author=admin_user,
            end_date=date.today() + timedelta(days=10)
        )

        Announcement.objects.get_or_create(
            title='Изменение расписания',
            content='В связи с ремонтом, уроки физики переносятся на следующий понедельник.',
            category=important,
            author=admin_user,
            end_date=date.today() + timedelta(days=5),
            is_pinned=True
        )

        self.stdout.write(self.style.SUCCESS('Sample data created successfully'))