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
            type="3",  # Тип проекта: большой
            name="Веб-платформа для управления цифровыми услугами",
            data_start=datetime(2023, 3, 1).date(),
            data_end=datetime(2024, 5, 15).date(),
            additional_costs=add_costs,
            payment_client=4800000,
            total_cost=4400000,
            expected_costs=4200000,
            actual_costs=4150000,
            expected_profits=600000,
            actual_profits=650000,
            status="Finished"
        )
        # Участники (12 человек), в данном примере - словарь с ключами ролей и списками сотрудников
        project.staff.set(list(staff_by_role.values()) + [customer])


        # Обновлённый словарь с двумя дополнительными булевыми значениями: is_done и is_report_approved
        tasks_by_role = {

            "backend": [
                ("Проектирование REST API для модулей управления", "adopted_customer", 48, 46, "положительный", True, True),
                ("Реализация микросервисов на Django", "adopted_customer", 152, 239, "положительный", True, True),
                ("Обработка вебхуков от внешних систем", "adopted_customer", 35, 38, "негативный", True, True),
                ("Оптимизация запросов ORM", "adopted_customer", 28, 26, "положительный", True, True),
                ("Поддержка версий API", "adopted_customer", 24, 23, "негативный", True, True),
                ("Рефакторинг бизнес-логики", "adopted_customer", 32, 35, "положительный", True, True),
                ("Поддержка мультиязычности", "adopted_customer", 30, 29, "положительный", True, True),
                ("Реализация очередей задач (Celery)", "adopted_customer", 26, 24, "негативный", True, True),
                ("Поддержка WebSocket соединений", "adopted_customer", 38, 38, "положительный", True, True),
                ("Управление токенами доступа", "adopted_customer", 20, 18, "негативный", True, True),
            ],
            "frontend": [
                ("Разработка SPA-интерфейса на Vue.js", "adopted_customer", 50, 67, "положительный", True, True),
                ("Интеграция с backend API", "adopted_customer", 42, 40, "положительный", True, True),
                ("Поддержка динамических форм", "adopted_customer", 38, 36, "положительный", True, True),
                ("Разметка и адаптивность интерфейса", "adopted_customer", 35, 23, "негативный", True, True),
                ("Поддержка PWA (прогрессивное приложение)", "adopted_customer", 30, 27, "негативный", True, True),
                ("Настройка роутинга и состояния", "adopted_customer", 26, 24, "положительный", True, True),
                ("Оптимизация загрузки компонентов", "adopted_customer", 28, 40, "положительный", True, True),
                ("Обработка ошибок интерфейса", "adopted_customer", 24, 21, "негативный", True, True),
            ],
            "integration": [
                ("Интеграция с CRM-системой Bitrix", "adopted_customer", 44, 46, "негативный", True, True),
                ("Обработка API от 1С", "adopted_customer", 36, 34, "положительный", True, True),
                ("Интеграция с платёжными шлюзами", "adopted_customer", 40, 48, "положительный", True, True),
                ("Webhooks и уведомления для сторонних систем", "adopted_customer", 30, 58, "негативный", True, True),
                ("OAuth 2.0 и SSO подключения", "adopted_customer", 26, 35, "положительный", True, True),
                ("Документация на интеграции", "adopted_customer", 22, 20, "положительный", True, True),
                ("Тестирование интеграционных кейсов", "adopted_customer", 24, 33, "негативный", True, True),
            ],
            "database": [
                ("Проектирование схемы БД", "adopted_customer", 48, 45, "положительный", True, True),
                ("Оптимизация индексов", "adopted_customer", 40, 38, "положительный", True, True),
                ("Настройка репликации", "adopted_customer", 30, 28, "негативный", True, True),
                ("Разработка SQL-функций", "adopted_customer", 28, 36, "положительный", True, True),
                ("Резервное копирование и восстановление", "adopted_customer", 24, 23, "негативный", True, True),
                ("Поддержка версионности данных", "adopted_customer", 26, 25, "положительный", True, True),
                ("Миграции и сопровождение", "adopted_customer", 22, 21, "положительный", True, True),
                ("Анализ планов выполнения запросов", "adopted_customer", 30, 29, "негативный", True, True),
            ],
            "devops": [
                ("Настройка CI/CD GitLab", "adopted_customer", 46, 44, "положительный", True, True),
                ("Автоматизация деплоя в Docker", "adopted_customer", 42, 39, "положительный", True, True),
                ("Мониторинг через Grafana и Prometheus", "adopted_customer", 35, 33, "негативный", True, True),
                ("Настройка алертов и логирования", "adopted_customer", 38, 36, "положительный", True, True),
                ("Оптимизация ресурсов AWS", "adopted_customer", 30, 29, "негативный", True, True),
                ("Управление секретами (Vault)", "adopted_customer", 28, 26, "положительный", True, True),
            ],
            "ml_ai": [
                ("Анализ пользовательской активности", "adopted_customer", 34, 32, "положительный", True, True),
                ("Рекомендательные модели контента", "adopted_customer", 40, 37, "положительный", True, True),
                ("Кластеризация клиентов", "adopted_customer", 32, 29, "негативный", True, True),
                ("Обучение моделей на данных CRM", "adopted_customer", 30, 38, "положительный", True, True),
                ("Интеграция модели в backend", "adopted_customer", 26, 24, "негативный", True, True),
                ("Тестирование и A/B сравнение", "adopted_customer", 24, 32, "положительный", True, True),
            ],
            "mobile": [
                ("Разработка Flutter-приложения", "adopted_customer", 48, 45, "положительный", True, True),
                ("Аутентификация и push-уведомления", "adopted_customer", 40, 37, "негативный", True, True),
                ("Интеграция с API платформы", "adopted_customer", 36, 34, "положительный", True, True),
                ("Работа с оффлайн-режимом", "adopted_customer", 28, 25, "негативный", True, True),
                ("Тестирование на устройствах", "adopted_customer", 30, 28, "положительный", True, True),
            ],
            "testing": [
                ("Написание unit-тестов backend", "adopted_customer", 35, 42, "положительный", True, True),
                ("E2E тесты фронтенда", "adopted_customer", 38, 36, "положительный", True, True),
                ("Нагрузочное тестирование API", "adopted_customer", 28, 36, "негативный", True, True),
                ("Сценарии тестирования мобильного клиента", "adopted_customer", 30, 28, "положительный", True, True),
                ("Интеграционные тесты", "adopted_customer", 24, 43, "негативный", True, True),
            ],
            "ux_ui": [
                ("Разработка UX-карт пользовательских сценариев", "adopted_customer", 42, 40, "положительный", True,
                 True),
                ("Прототипирование интерфейса", "adopted_customer", 36, 34, "положительный", True, True),
                ("Пользовательские тестирования", "adopted_customer", 30, 48, "негативный", True, True),
                ("Адаптация под мобильные устройства", "adopted_customer", 28, 45, "негативный", True, True),
                ("UI-гайдлайн и компоненты", "adopted_customer", 32, 30, "положительный", True, True),
            ],
            "documentation": [
                ("Создание Swagger-спецификации", "adopted_customer", 24, 42, "положительный", True, True),
                ("Описание REST API", "adopted_customer", 20, 18, "негативный", True, True),
                ("Сопровождение Confluence", "adopted_customer", 18, 17, "положительный", True, True),
                ("Создание инструкций для пользователей", "adopted_customer", 22, 21, "положительный", True, True),
            ],
            "architecture": [
                ("Проектирование архитектуры микросервисов", "adopted_customer", 46, 44, "положительный", True, True),
                ("Моделирование взаимодействия компонентов", "adopted_customer", 40, 38, "положительный", True, True),
                ("Выбор технологий и стеков", "adopted_customer", 36, 45, "негативный", True, True),
                ("Архитектурный аудит решений", "adopted_customer", 28, 26, "негативный", True, True),
            ],
        }



        base_date = datetime(2023, 3, 1)

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