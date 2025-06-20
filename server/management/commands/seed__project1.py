from django.core.management.base import BaseCommand
from server.models import (
    Project, Task, SettingTask, Staff, Department,
    ReportingTask, FeedbackCustomer, AdditionalCosts
)
from django.utils import timezone
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Создание одного проекта и генерация задач с привязкой сотрудников'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Запуск генерации проекта и задач"))
        self.generate_project_with_tasks()
        self.stdout.write(self.style.SUCCESS("Генерация завершена"))

    def generate_project_with_tasks(self):
        # Получение сотрудников по ролям
        staff_by_role = {
            "backend": Staff.objects.filter(category="2", department__name="backend").first(),
            "integration": Staff.objects.filter(category="2", department__name="integration").first(),
            "devops": Staff.objects.filter(category="2", department__name="devops").first()
        }

        if None in staff_by_role.values():
            self.stdout.write(self.style.ERROR("Не хватает сотрудников в департаментах backend, integration, devops"))
            return

        customer = Staff.objects.filter(category="3").first()
        if not customer:
            self.stdout.write(self.style.ERROR("Не найден заказчик (category=3)"))
            return

        add_costs = AdditionalCosts.objects.order_by('?').first()
        if not add_costs:
            self.stdout.write(self.style.ERROR("Отсутствует запись в AdditionalCosts"))
            return

        # Создание проекта
        project = Project.objects.create(
            type="2",
            name="ERP Агротех 2025",
            data_start=timezone.now().date(),
            data_end=(timezone.now() + timedelta(days=60)).date(),
            additional_costs=add_costs,
            payment_client=450000,
            total_cost=700000,
            expected_costs=500000,
            actual_costs=480000,
            expected_profits=200000,
            actual_profits=220000,
            status="Development"
        )
        project.staff.set(list(staff_by_role.values()) + [customer])

        # Обновлённый словарь с двумя дополнительными булевыми значениями: is_done и is_report_approved
        tasks_by_role = {
            "backend": [
                # (название, статус, план, факт, результат, выполнена, отчёт принят)
                ("Реализация REST API авторизации", "adopted_customer", 16, 25, "положительный", True, True),
                ("Обработка ролей и прав доступа", "adopted_customer", 11, 16, "отрицательный", True, False),
                ("Сервис логирования действий", "verification", 20, 18, "", False, False),
                ("Разработка микросервиса аналитики", "Started", 8, 9, "", False, False),
                ("Обработка очередей задач", "verification_staff", 10, 14, "", False, False),
                ("Работа с файловым хранилищем", "Not_started", 6, 10, "", False, False),
                ("Настройка подписки на события", "adopted_customer", 10, 7, "отрицательный", True, True),
                ("Ведение Swagger документации API", "adopted_customer", 6, 5, "положительный", True, True),
                ("Рефакторинг сервиса уведомлений", "verification", 7, 20, "", False, False)
            ],
            "integration": [
                ("Интеграция с 1С", "adopted_customer", 16, 25, "положительный", True, True),
                ("Интеграция с платежной системой Tinkoff", "adopted_customer", 14, 17, "отрицательный", True, False),
                ("Настройка вебхуков от CRM", "verification_staff", 12, 15, "", False, False),
                ("Интеграция с BI-платформой PowerBI", "verification", 10, 14, "", False, False),
                ("Сервис экспорта Excel / PDF", "Started", 8, 15, "", False, False),
                ("Интеграция с документооборотом", "verification", 12, 10, "", False, False),
                ("Сервис контроля времени", "Not_started", 6, 30, "", False, False),
                ("Интеграция push-уведомлений", "adopted", 9, 4, "", True, True),
                ("Сервис email-контактов", "rejected_customer", 7, 14, "", False, False),
                ("Парсинг из Telegram-ботов", "adopted_customer", 10, 10, "положительный", True, True),
                ("Проверка ИНН и КПП", "verification_staff", 6, 5, "", False, False)
            ],
            "devops": [
                ("Настройка CI/CD GitLab", "adopted_customer", 12, 13, "отрицательный", True, False),
                ("Поднятие инфраструктуры в Docker", "adopted_customer", 14, 14, "положительный", True, True),
                ("Мониторинг Prometheus + Grafana", "verification", 10, 30, "", False, False),
                ("Конфигурация nginx + TLS", "Started", 7, 10, "", False, False),
                ("Настройка репликации PostgreSQL", "verification_staff", 11, 12, "", False, False),
                ("Внедрение логирования через ELK", "Not_started", 8, 12, "", False, False),
                ("Обеспечение отказоустойчивости", "adopted_customer", 9, 7, "положительный", True, True),
                ("Настройка внешнего брандмауэра", "adopted_customer", 6, 5, "положительный", True, True)
            ]
        }

        base_date = datetime(2025, 1, 1)

        for role, task_list in tasks_by_role.items():
            staff_member = staff_by_role[role]
            for i, (title, status, planned, fact, result, is_done, is_report_approved) in enumerate(task_list):
                date_start = base_date + timedelta(days=i * 3)
                date_finish = date_start + timedelta(days=10)

                description = f"{title} — задача по направлению {role}, связанная с проектом ERP. План: {planned}ч, факт: {fact}ч."
                task = Task.objects.create(
                    name=title,
                    dsc=description,
                    type=role
                )

                # Логика статусов задачи
                is_finished = is_done
                is_active = not is_finished
                is_started = not is_finished

                setting_task = SettingTask.objects.create(
                    staff=staff_member,
                    task=task,
                    scheduled_hours=planned,
                    scheduled_day=planned // 2,
                    actual_hours=fact,
                    actual_day=fact // 2,
                    status=status,
                    is_started=is_started,
                    is_active=is_active
                )

                # Отчёт сотрудника создаём только если задача выполнена
                if is_done:
                    report = ReportingTask.objects.create(
                        data_start=date_start,
                        report_stuff=f"Финальный отчёт по задаче '{title}'",
                        is_adopted='adopted' if is_report_approved else 'rejected',
                        comment_director="Одобрено" if is_report_approved else "Отклонено"
                    )
                    setting_task.reportings.add(report)

                    # Фидбэк от заказчика добавляем только если отчёт принят
                    if is_report_approved:
                        feedback = FeedbackCustomer.objects.create(
                            data_start=date_finish,
                            report_stuff=f"Фидбек заказчика по задаче '{title}'",
                            is_adopted='adopted',
                            comment_director=result or "Нет комментариев"
                        )
                        setting_task.feedback_customer.add(feedback)

                project.task.add(setting_task)