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
        self.stdout.write(self.style.SUCCESS("🚀 Запуск генерации проекта и задач"))
        self.generate_project_with_tasks()
        self.stdout.write(self.style.SUCCESS("✅ Генерация завершена"))

    def generate_project_with_tasks(self):
        # Получение сотрудников по ролям
        staff_by_role = {
            "backend": Staff.objects.filter(category="2", department__name="backend").first(),
            "integration": Staff.objects.filter(category="2", department__name="integration").first(),
            "devops": Staff.objects.filter(category="2", department__name="devops").first(),
            "database": Staff.objects.filter(category="2", department__name="database").first(),
            "ml_ai": Staff.objects.filter(category="2", department__name="ml_ai").first(),
            "frontend": Staff.objects.filter(category="2", department__name="frontend").first(),
            "testing": Staff.objects.filter(category="2", department__name="testing").first(),
            "ux_ui": Staff.objects.filter(category="2", department__name="ux_ui").first(),
            "mobile": Staff.objects.filter(category="2", department__name="mobile").first(),
            "architecture": Staff.objects.filter(category="2", department__name="architecture").first(),
            "documentation": Staff.objects.filter(category="2", department__name="documentation").first(),
        }

        if None in staff_by_role.values():
            self.stdout.write(self.style.ERROR("❌ Не хватает сотрудников в департаментах backend, integration, devops"))
            return

        customer = Staff.objects.filter(category="3").first()
        if not customer:
            self.stdout.write(self.style.ERROR("❌ Не найден заказчик (category=3)"))
            return

        add_costs = AdditionalCosts.objects.order_by('?').first()
        if not add_costs:
            self.stdout.write(self.style.ERROR("❌ Отсутствует запись в AdditionalCosts"))
            return

        # Создание проекта
        project = Project.objects.create(
            type="3",  # Тип: большой
            name="Система автоматизации логистических процессов",
            data_start=datetime(2022, 5, 1).date(),
            data_end=datetime(2023, 10, 30).date(),
            additional_costs=add_costs,
            payment_client=5500000,
            total_cost=5100000,
            expected_costs=4950000,
            actual_costs=4880000,
            expected_profits=550000,
            actual_profits=620000,
            status="Finished"
        )
        # Участники (12 человек), в данном примере - словарь с ключами ролей и списками сотрудников
        project.staff.set(list(staff_by_role.values()) + [customer])


        # Обновлённый словарь с двумя дополнительными булевыми значениями: is_done и is_report_approved
        tasks_by_role = {

            "backend": [
                ("Реализация API для логистических модулей", "adopted_customer", 145, 173, "положительный", True, True),
                ("Управление маршрутами и заказами", "adopted_customer", 38, 35, "положительный", True, True),
                ("Контроль доступа и ролей", "adopted_customer", 28, 26, "негативный", True, True),
                ("Реализация очередей задач (Celery)", "adopted_customer", 35, 13, "положительный", True, True),
                ("Интеграция с системой учета складов", "adopted_customer", 40, 37, "положительный", True, True),
                ("Поддержка геолокации транспорта", "adopted_customer", 30, 28, "негативный", True, True),
                ("Валидация и обработка заказов", "adopted_customer", 25, 22, "положительный", True, True),
                ("Настройка повторных заданий cron", "adopted_customer", 18, 27, "негативный", True, True),
                ("Обработка загрузки и выгрузки данных", "adopted_customer", 32, 31, "положительный", True, True),
            ],
            "frontend": [
                ("Интерфейс диспетчера логистики", "adopted_customer", 140, 248, "положительный", True, True),
                ("Визуализация маршрутов доставки", "adopted_customer", 36, 33, "положительный", True, True),
                ("Форма создания и редактирования заказов", "adopted_customer", 26, 25, "негативный", True, True),
                ("Фильтрация и сортировка таблиц", "adopted_customer", 20, 49, "положительный", True, True),
                ("UI уведомлений о статусах", "adopted_customer", 22, 21, "положительный", True, True),
                ("Личный кабинет водителя", "adopted_customer", 28, 26, "негативный", True, True),
                ("Работа с картой (Leaflet)", "adopted_customer", 34, 42, "положительный", True, True),
                ("Мобильная адаптация интерфейса", "adopted_customer", 24, 43, "негативный", True, True),
            ],
            "integration": [
                ("Интеграция с системой складского учёта", "adopted_customer", 36, 34, "положительный", True, True),
                ("Синхронизация с внешней ТМС", "adopted_customer", 32, 31, "негативный", True, True),
                ("Обмен заказами с SAP", "adopted_customer", 30, 28, "положительный", True, True),
                ("Интеграция через SOAP/REST", "adopted_customer", 20, 49, "негативный", True, True),
                ("Обработка ошибок интеграции", "adopted_customer", 25, 24, "положительный", True, True),
                ("Подключение к API транспортных провайдеров", "adopted_customer", 26, 24, "негативный", True, True),
            ],
            "database": [
                ("Проектирование логистической схемы БД", "adopted_customer", 34, 33, "положительный", True, True),
                ("Оптимизация индексов заказов", "adopted_customer", 28, 36, "негативный", True, True),
                ("Поддержка версионности маршрутов", "adopted_customer", 24, 32, "положительный", True, True),
                ("SQL для выборки по складам", "adopted_customer", 22, 20, "положительный", True, True),
                ("Настройка бэкапов и восстановления", "adopted_customer", 18, 17, "негативный", True, True),
                ("Переход на логическую репликацию", "adopted_customer", 26, 24, "негативный", True, True),
            ],
            "devops": [
                ("CI/CD для backend и frontend", "adopted_customer", 36, 34, "положительный", True, True),
                ("Автодеплой в staging и prod", "adopted_customer", 30, 38, "положительный", True, True),
                ("Мониторинг с использованием Prometheus", "adopted_customer", 26, 24, "негативный", True, True),
                ("Логирование через ELK-стек", "adopted_customer", 24, 22, "положительный", True, True),
                ("Настройка секретов в Kubernetes", "adopted_customer", 22, 31, "негативный", True, True),
            ],
            "ml_ai": [
                ("Предсказание задержек доставки", "adopted_customer", 30, 28, "положительный", True, True),
                ("Классификация заказов по приоритету", "adopted_customer", 26, 25, "положительный", True, True),
                ("Анализ маршрутов на предмет оптимальности", "adopted_customer", 34, 22, "негативный", True, True),
                ("Интеграция моделей в API", "adopted_customer", 22, 21, "негативный", True, True),
            ],
            "mobile": [
                ("Мобильное приложение для водителей", "adopted_customer", 40, 38, "положительный", True, True),
                ("Сканирование QR-кодов на складе", "adopted_customer", 22, 21, "негативный", True, True),
                ("Интеграция push-уведомлений", "adopted_customer", 18, 17, "положительный", True, True),
                ("Работа с оффлайн-режимом", "adopted_customer", 20, 28, "негативный", True, True),
            ],
            "testing": [
                ("E2E тесты маршрутов", "adopted_customer", 126, 124, "положительный", True, True),
                ("Интеграционные тесты API", "adopted_customer", 24, 22, "положительный", True, True),
                ("Нагрузочное тестирование базы заказов", "adopted_customer", 20, 18, "негативный", True, True),
                ("Тестирование мобильного клиента", "adopted_customer", 22, 5, "положительный", True, True),
            ],
            "ux_ui": [
                ("UI логистических панелей", "adopted_customer", 28, 26, "положительный", True, True),
                ("Анализ пользовательских сценариев", "adopted_customer", 24, 22, "негативный", True, True),
                ("Адаптивный дизайн интерфейсов", "adopted_customer", 29, 40, "положительный", True, True),
                ("Тестирование интерфейса с операторами", "adopted_customer", 20, 19, "негативный", True, True),
            ],
            "documentation": [
                ("Документация API для партнёров", "adopted_customer", 18, 17, "положительный", True, True),
                ("Описание интеграционных схем", "adopted_customer", 20, 18, "негативный", True, True),
                ("Руководство для водителей", "adopted_customer", 22, 21, "положительный", True, True),
            ],
            "architecture": [
                ("Архитектура логистической системы", "adopted_customer", 40, 38, "положительный", True, True),
                ("Описание компонентной структуры", "adopted_customer", 38, 35, "негативный", True, True),
                ("Архитектурный контроль качества кода", "adopted_customer", 30, 58, "положительный", True, True),
            ],
        }



        base_date = datetime(2022, 5, 1)

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