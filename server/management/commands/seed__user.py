#TODO Генерация сотрудников (разработчики и закзачики)

from django.core.management.base import BaseCommand
from server.models import Staff, Department
from django.utils import timezone
import random
from faker import Faker

fake = Faker("ru_RU")


class Command(BaseCommand):
    help = 'Генерация тестовых данных для сотрудников и заказчиков в соответствии с текущей БД'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("🚀 Начало генерации сотрудников: разработчики и заказчики"))

        self.create_departments()
        self.create_staff_users()
        self.create_customers()

        self.stdout.write(self.style.SUCCESS("✅ Генерация завершена"))

    def create_departments(self):
        departments_data = [
            ('backend', 'Разработка серверной логики, REST API, микросервисов.'),
            ('frontend', 'Интерфейсная часть, SPA, SSR.'),
            ('integration', 'Интеграция с внешними API, 1С, CRM, платёжками.'),
            ('database', 'Проектирование и оптимизация БД, миграции, индексы.'),
            ('devops', 'CI/CD, деплой, настройка серверов, мониторинг.'),
            ('ml_ai', 'Модели ИИ, аналитика, обучение, инференс.'),
            ('mobile', 'iOS/Android разработка.'),
            ('testing', 'Написание unit, e2e, нагрузочное тестирование.'),
            ('ux_ui', 'Проектирование пользовательского опыта, прототипы.'),
            ('documentation', 'Подготовка технической документации, Swagger, Confluence.'),
            ('architecture', 'Проектирование архитектуры решения, паттерны.'),
            ('security', 'Аудит безопасности, защита API, шифрование.'),
            ('research', 'R&D задачи, эксперименты с новыми технологиями.'),
            ('refactoring', 'Улучшение старого кода, устранение технического долга.'),
            ('support', 'Исправление багов, поддержка пользователей.'),
        ]

        for name, description in departments_data:
            Department.objects.get_or_create(
                name=name,
                defaults={'description': description, 'bet': random.randint(1500, 3000), 'bet_local': random.randint(500, 1000)}
            )

    def create_staff_users(self):
        companies = {
            "mobile_wave": ['mobile', 'frontend', 'backend'],
            "ml_solutions": ['ml_ai', 'research', 'backend'],
            "cloud_infra": ['devops', 'integration', 'security'],
            "web_apps": ['frontend', 'ux_ui', 'testing'],
            "enterprise_soft": ['architecture', 'database', 'integration'],
            "qa_experts": ['testing', 'documentation', 'support'],
            "universal_team": ['backend', 'frontend', 'support', 'refactoring'],
        }

        departments = {d.name: d for d in Department.objects.all()}
        user_id = 1

        for company, roles in companies.items():
            for _ in range(10):  # 10 пользователей на компанию
                role = random.choice(roles)
                Staff.objects.create_user(
                    username=f"user_{user_id}",
                    password="test1234",
                    name=fake.name(),
                    category="2",  # сотрудник
                    department=departments[role],
                    account_bank=fake.iban(),
                    bank=random.choice(['t-bank', 'sber', 'alpha', 'vtb', 'other']),
                )
                user_id += 1

    def create_customers(self):
        customer_companies = [
            "mobile_wave", "ml_solutions", "cloud_infra", "web_apps",
            "enterprise_soft", "qa_experts", "universal_team", "ml_solutions"
        ]

        for i, company in enumerate(customer_companies, start=1):
            Staff.objects.create_user(
                username=f"customer_{i}",
                password="test1234",
                name=f"{fake.company()} ({company})",
                category="3",  # заказчик
                bank="not_bank"
            )




# # TODO Генерация первого проекта
# from django.core.management.base import BaseCommand
# from server.models import (
#     Project, Task, SettingTask, Staff, Department,
#     ReportingTask, FeedbackCustomer, AdditionalCosts
# )
# from django.utils import timezone
# from datetime import datetime, timedelta
# import random
#
# class Command(BaseCommand):
#     help = 'Создание одного проекта и генерация десятков задач с привязкой сотрудников'
#
#     def handle(self, *args, **kwargs):
#         self.stdout.write(self.style.SUCCESS("🚀 Запуск генерации проекта и задач"))
#
#         self.generate_project_with_tasks()
#
#         self.stdout.write(self.style.SUCCESS("✅ Генерация завершена"))
#
#     def generate_project_with_tasks(self):
#         # --- Шаг 1. Проверка и выбор данных ---
#         staff_by_role = {
#             "backend": Staff.objects.filter(category="2", department__name="backend").first(),
#             "integration": Staff.objects.filter(category="2", department__name="integration").first(),
#             "devops": Staff.objects.filter(category="2", department__name="devops").first()
#         }
#
#         if None in staff_by_role.values():
#             self.stdout.write(self.style.ERROR("❌ Не хватает сотрудников в департаментах backend, integration, devops"))
#             return
#
#         customer = Staff.objects.filter(category="3").first()
#         if not customer:
#             self.stdout.write(self.style.ERROR("❌ Не найден заказчик (category=3)"))
#             return
#
#         add_costs = AdditionalCosts.objects.order_by('?').first()
#         if not add_costs:
#             self.stdout.write(self.style.ERROR("❌ Отсутствует запись в AdditionalCosts"))
#             return
#
#         # --- Шаг 2. Создание проекта ---
#         project = Project.objects.create(
#             type="2",
#             name="ERP Агротех 2025",
#             data_start=timezone.now().date(),
#             data_end=(timezone.now() + timedelta(days=60)).date(),
#             additional_costs=add_costs,
#             payment_client=450000,
#             total_cost=700000,
#             expected_costs=500000,
#             actual_costs=480000,
#             expected_profits=200000,
#             actual_profits=220000,
#             status="Development"
#         )
#
#         # Привязка сотрудников и заказчика
#         project.staff.set(list(staff_by_role.values()) + [customer])
#
#         # --- Шаг 3. Данные задач ---
#         tasks_by_role = {
#             "backend": [
#                 ("Реализация REST API авторизации", "adopted_customer", 12, 10, "положительный"),
#                 ("Обработка ролей и прав доступа", "adopted_customer", 14, 16, "отрицательный"),
#                 ("Сервис логирования действий", "verification", 10, 9, ""),
#                 ("Разработка микросервиса аналитики", "Started", 8, 4, ""),
#                 ("Обработка очередей задач", "verification_staff", 9, 7, ""),
#                 ("Работа с файловым хранилищем", "Not_started", 6, 0, ""),
#                 ("Настройка подписки на события", "adopted_customer", 10, 11, "отрицательный"),
#                 ("Ведение Swagger документации API", "adopted_customer", 6, 5, "положительный"),
#                 ("Рефакторинг сервиса уведомлений", "verification", 7, 6, "")
#             ],
#             "integration": [
#                 ("Интеграция с 1С", "adopted_customer", 16, 15, "положительный"),
#                 ("Интеграция с платежной системой Tinkoff", "adopted_customer", 14, 17, "отрицательный"),
#                 ("Настройка вебхуков от CRM", "verification_staff", 12, 11, ""),
#                 ("Интеграция с BI-платформой PowerBI", "verification", 10, 9, ""),
#                 ("Сервис экспорта Excel / PDF", "Started", 8, 3, ""),
#                 ("Интеграция с документооборотом", "verification", 12, 11, ""),
#                 ("Сервис контроля времени", "Not_started", 6, 0, ""),
#                 ("Интеграция push-уведомлений", "adopted", 9, 8, ""),
#                 ("Сервис email-контактов", "rejected_customer", 7, 10, ""),
#                 ("Парсинг из Telegram-ботов", "adopted_customer", 10, 10, "положительный"),
#                 ("Проверка ИНН и КПП", "verification_staff", 6, 5, "")
#             ],
#             "devops": [
#                 ("Настройка CI/CD GitLab", "adopted_customer", 12, 13, "отрицательный"),
#                 ("Поднятие инфраструктуры в Docker", "adopted_customer", 14, 12, "положительный"),
#                 ("Мониторинг Prometheus + Grafana", "verification", 10, 8, ""),
#                 ("Конфигурация nginx + TLS", "Started", 7, 2, ""),
#                 ("Настройка репликации PostgreSQL", "verification_staff", 11, 9, ""),
#                 ("Внедрение логирования через ELK", "Not_started", 8, 0, ""),
#                 ("Обеспечение отказоустойчивости", "adopted_customer", 9, 7, "положительный"),
#                 ("Настройка внешнего брандмауэра", "adopted_customer", 6, 5, "положительный")
#             ]
#         }
#
#         base_date = datetime(2025, 1, 1)
#
#         # --- Шаг 4. Генерация задач ---
#         for role, task_list in tasks_by_role.items():
#             staff_member = staff_by_role[role]
#             for i, (title, status, planned, fact, result) in enumerate(task_list):
#                 date_start = base_date + timedelta(days=i * 3)
#                 date_finish = date_start + timedelta(days=10)
#
#                 task = Task.objects.create(
#                     name=title,
#                     dsc=f"Автоматически сгенерированная задача по направлению {role}",
#                     type=role
#                 )
#
#                 reporting = ReportingTask.objects.create(
#                     data_start=date_start,
#                     report_stuff=f"Отчёт по задаче '{title}' от исполнителя",
#                     is_adopted=random.choice(['verification', 'adopted', 'rejected']),
#                     comment_director=random.choice(["", "Нужна доработка", "Одобрено", "Оценка положительная"])
#                 )
#
#                 feedback = FeedbackCustomer.objects.create(
#                     data_start=date_finish,
#                     report_stuff=f"Фидбек от заказчика по задаче '{title}'",
#                     is_adopted=random.choice(['verification', 'adopted', 'rejected']),
#                     comment_director=result or random.choice(["", "Не соответствует требованиям", "Хорошее исполнение"])
#                 )
#
#                 setting_task = SettingTask.objects.create(
#                     staff=staff_member,
#                     task=task,
#                     scheduled_hours=planned,
#                     scheduled_day=planned // 2,
#                     actual_hours=fact,
#                     actual_day=fact // 2,
#                     status=status,
#                     is_started=True,
#                     is_active=False
#                 )
#                 setting_task.reportings.add(reporting)
#                 setting_task.feedback_customer.add(feedback)
#
#                 project.task.add(setting_task)