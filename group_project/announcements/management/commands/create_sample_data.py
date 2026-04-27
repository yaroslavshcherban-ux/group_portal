from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from announcements.models import Category, Announcement, Comment
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Create sample data'

    def handle(self, *args, **options):
        # Очистить старые данные
        Announcement.objects.all().delete()
        Category.objects.all().delete()

        # Создать категории
        news = Category.objects.get_or_create(name='Новини', description='Шкільні новини')[0]
        events = Category.objects.get_or_create(name='Події', description='Шкільні заходи')[0]
        important = Category.objects.get_or_create(name='Важливе', description='Важливі оголошення')[0]
        sports = Category.objects.get_or_create(name='Спорт', description='Спортивні події')[0]
        education = Category.objects.get_or_create(name='Освіта', description='Навчальні матеріали')[0]

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
            title='Ласкаво просимо до нового навчального року!',
            content='Шановні учні та батьки! Ми раді привітати вас у новому навчальному році. Бажаємо успіхів у навчанні, цікавих відкриттів та незабутніх моментів!',
            category=news,
            author=admin_user,
            end_date=date.today() + timedelta(days=30),
            is_pinned=True
        )

        Announcement.objects.get_or_create(
            title='Батьківські збори',
            content='Батьківські збори відбудуться 15 березня о 18:00 в актовому залі. Обговорюватимемо успіхи учнів та плани на наступний семестр.',
            category=events,
            author=admin_user,
            end_date=date.today() + timedelta(days=10)
        )

        Announcement.objects.get_or_create(
            title='Зміна розкладу',
            content='У зв\'язку з ремонтом, уроки фізики переносяться на наступний понеділок. Детальний розклад буде опубліковано завтра.',
            category=important,
            author=admin_user,
            end_date=date.today() + timedelta(days=5),
            is_pinned=True
        )

        Announcement.objects.get_or_create(
            title='Спартакіада школярів',
            content='Запрошуємо всіх учнів взяти участь у шкільній спартакіаді! Реєстрація відкрита до 20 березня. Команди формуються за класами.',
            category=sports,
            author=admin_user,
            end_date=date.today() + timedelta(days=15)
        )

        Announcement.objects.get_or_create(
            title='Новий навчальний матеріал з математики',
            content='Опубліковано нові завдання з алгебри для 9 класу. Завантажте матеріали з шкільного порталу та підготуйтеся до контрольної.',
            category=education,
            author=admin_user,
            end_date=date.today() + timedelta(days=7)
        )

        Announcement.objects.get_or_create(
            title='Конкурс малюнків "Моя школа"',
            content='Оголошується конкурс дитячих малюнків на тему "Моя школа". Приймаємо роботи до 25 березня. Переможці отримають призи!',
            category=events,
            author=admin_user,
            end_date=date.today() + timedelta(days=12)
        )

        Announcement.objects.get_or_create(
            title='Важлива інформація про безпеку',
            content='Нагадуємо всім учням про правила поведінки на території школи. Заборонено бігати по коридорах та використовувати мобільні телефони на уроках.',
            category=important,
            author=admin_user,
            end_date=date.today() + timedelta(days=30),
            is_pinned=True
        )

        Announcement.objects.get_or_create(
            title='Футбольний турнір',
            content='Цього тижня відбудеться внутрішньошкільний футбольний турнір. Вболівайте за свою команду!',
            category=sports,
            author=admin_user,
            end_date=date.today() + timedelta(days=3)
        )

        Announcement.objects.get_or_create(
            title='Онлайн-курс з програмування',
            content='Для учнів старших класів доступний безкоштовний онлайн-курс з Python. Реєстрація через шкільний портал.',
            category=education,
            author=admin_user,
            end_date=date.today() + timedelta(days=20)
        )

        Announcement.objects.get_or_create(
            title='День відкритих дверей',
            content='Запрошуємо батьків на День відкритих дверей 30 березня. Познайомтеся з викладачами та навчальним процесом.',
            category=events,
            author=admin_user,
            end_date=date.today() + timedelta(days=17)
        )

        Announcement.objects.get_or_create(
            title='Лікарський огляд учнів',
            content='Усі учні повинні пройти медичний огляд у шкільній лікарні. Розклад за класами буде опубліковано наступного тижня.',
            category=important,
            author=admin_user,
            end_date=date.today() + timedelta(days=25)
        )

        Announcement.objects.get_or_create(
            title='Турнір з шахів',
            content='Відкрита реєстрація на шкільний чемпіонат з шахів. Змагання відбудуться у спортивній залі.',
            category=sports,
            author=admin_user,
            end_date=date.today() + timedelta(days=8)
        )

        Announcement.objects.get_or_create(
            title='Допомога з домашніми завданнями',
            content='Щочетверга після уроків працює консультаційний центр для допомоги з домашніми завданнями. Викладачі допоможуть з математикою та українською мовою.',
            category=education,
            author=admin_user,
            end_date=date.today() + timedelta(days=30)
        )

        Announcement.objects.get_or_create(
            title='Екскурсія до музею',
            content='Для учнів 10-11 класів організовується екскурсія до історичного музею міста. Вартість - 50 грн. Реєстрація обов\'язкова.',
            category=events,
            author=admin_user,
            end_date=date.today() + timedelta(days=14)
        )

        Announcement.objects.get_or_create(
            title='Нові правила поведінки',
            content='Затверджено нові правила внутрішнього розпорядку школи. Всі учні повинні ознайомитися та підписати правила.',
            category=important,
            author=admin_user,
            end_date=date.today() + timedelta(days=20),
            is_pinned=True
        )

        Announcement.objects.get_or_create(
            title='Баскетбольний матч',
            content='Цього п\'ятниці наша школа грає проти команди з сусідньої школи. Початок о 16:00 на шкільному майданчику.',
            category=sports,
            author=admin_user,
            end_date=date.today() + timedelta(days=2)
        )

        Announcement.objects.get_or_create(
            title='Підготовка до Олімпіади з фізики',
            content='Для учнів, які цікавляться фізикою, організовуються додаткові заняття для підготовки до обласної олімпіади.',
            category=education,
            author=admin_user,
            end_date=date.today() + timedelta(days=40)
        )

        Announcement.objects.get_or_create(
            title='Шкільний фестиваль мистецтв',
            content='Оголошується фестиваль шкільних талантів! Приймаємо заявки на виступи до 10 квітня. Тематика вільна.',
            category=events,
            author=admin_user,
            end_date=date.today() + timedelta(days=28)
        )

        Announcement.objects.get_or_create(
            title='Ремонт спортивного залу',
            content='Спортивний зал буде закритий на ремонт з 15 по 20 квітня. Уроки фізкультури проводитимуться на вулиці.',
            category=important,
            author=admin_user,
            end_date=date.today() + timedelta(days=35)
        )

        Announcement.objects.get_or_create(
            title='Волейбольні змагання',
            content='Запрошуємо дівчат 8-11 класів взяти участь у волейбольних змаганнях між класами.',
            category=sports,
            author=admin_user,
            end_date=date.today() + timedelta(days=10)
        )

        Announcement.objects.get_or_create(
            title='Курс англійської мови онлайн',
            content='Для покращення знань англійської пропонуємо безкоштовний онлайн-курс з носієм мови. Реєстрація через класних керівників.',
            category=education,
            author=admin_user,
            end_date=date.today() + timedelta(days=50)
        )

        Announcement.objects.get_or_create(
            title='День здоров\'я',
            content='25 квітня відбудеться День здоров\'я з різноманітними активностями: біг, ігри, здорове харчування.',
            category=events,
            author=admin_user,
            end_date=date.today() + timedelta(days=42)
        )

        Announcement.objects.get_or_create(
            title='Заборона використання гаджетів',
            content='Згідно з новими правилами, використання мобільних телефонів заборонено на території школи під час навчального процесу.',
            category=important,
            author=admin_user,
            end_date=date.today() + timedelta(days=60),
            is_pinned=True
        )

        Announcement.objects.get_or_create(
            title='Тренування з футболу',
            content='Хлопці 9-11 класів запрошуються на додаткові тренування з футболу після уроків по середах.',
            category=sports,
            author=admin_user,
            end_date=date.today() + timedelta(days=30)
        )

        Announcement.objects.get_or_create(
            title='Підручники з хімії',
            content='Нові підручники з хімії для 10 класу доступні в шкільній бібліотеці. Ознайомтеся з матеріалами.',
            category=education,
            author=admin_user,
            end_date=date.today() + timedelta(days=90)
        )

        # Добавить комментарии
        announcements = Announcement.objects.all()
        if announcements.exists():
            first_announcement = announcements.first()
            Comment.objects.get_or_create(
                announcement=first_announcement,
                author=student_user,
                content='Дуже корисна інформація!'
            )

        self.stdout.write(self.style.SUCCESS('Sample data created successfully'))