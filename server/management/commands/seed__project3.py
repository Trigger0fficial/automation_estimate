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
            "ml_ai": Staff.objects.filter(category="2", department__name="testing").first(),
            "frontend": Staff.objects.filter(category="2", department__name="frontend").first(),
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
            type="2",  # Тип проекта: средний (до 12 человек)
            name="ERP-система для управления производственными активами",
            data_start=datetime(2023, 4, 15).date(),
            data_end=datetime(2024, 6, 30).date(),
            additional_costs=add_costs,
            payment_client=3500000,
            total_cost=3200000,
            expected_costs=3000000,
            actual_costs=2950000,
            expected_profits=500000,
            actual_profits=550000,
            status="Finished"
        )

        # Участники (12 человек), в данном примере - словарь с ключами ролей и списками сотрудников
        project.staff.set(list(staff_by_role.values()) + [customer])


        # Обновлённый словарь с двумя дополнительными булевыми значениями: is_done и is_report_approved
        tasks_by_role = {

                "backend": [
                    ("Разработка модулей управления активами", "adopted_customer", 16, 19, "негативный", True, True),
                    ("Реализация бизнес-логики автоматического планирования", "adopted_customer", 18, 16, "положительный", True, True),
                    ("API для взаимодействия с оборудованием", "adopted_customer", 14, 15, "негативный", True, True),
                    ("Обработка событий и уведомлений", "adopted_customer", 15, 18, "негативный", True, True),
                    ("Оптимизация запросов к базе данных", "adopted_customer", 12, 13, "положительный", True, True),
                    ("Механизм аутентификации и авторизации", "adopted_customer", 14, 12, "негативный", True, True),
                    ("Реализация отчетных модулей", "adopted_customer", 16, 29, "положительный", True, True),
                    ("Интеграция с внешними сервисами", "adopted_customer", 18, 6, "положительный", True, True),
                    ("Рефакторинг кода и повышение тестируемости", "adopted_customer", 15, 20, "положительный", True, True),
                    ("Обработка ошибок и логирование", "adopted_customer", 14, 24, "негативный", True, True),
                    ("Поддержка версионности данных", "adopted_customer", 13, 11, "негативный", True, True),
                    ("Настройка очередей задач", "adopted_customer", 12, 15, "положительный", True, True),
                    ("Модуль резервного копирования", "adopted_customer", 14, 28, "положительный", True, True),
                    ("API документация", "adopted_customer", 10, 20, "положительный", True, True),
                    ("Обеспечение безопасности данных", "adopted_customer", 16, 24, "негативный", True, True)
                ],
                "frontend": [
                    ("Разработка интерфейса мониторинга активов", "adopted_customer", 15, 20, "негативный", True, True),
                    ("Реализация динамических дашбордов", "adopted_customer", 18, 20, "положительный", True, True),
                    ("UI компонентов для управления задачами", "adopted_customer", 14, 41, "негативный", True, True),
                    ("Настройка адаптивного дизайна", "adopted_customer", 15, 23, "негативный", True, True),
                    ("Реализация уведомлений и алертов", "adopted_customer", 13, 14, "положительный", True, True),
                    ("Оптимизация клиентского рендеринга", "adopted_customer", 14, 8, "положительный", True, True),
                    ("Интеграция с backend API", "adopted_customer", 17, 6, "положительный", True, True),
                    ("Обработка ошибок и уведомлений", "adopted_customer", 13, 8, "положительный", True, True),
                    ("Реализация форм ввода и валидации", "adopted_customer", 16, 20, "положительный", True, True),
                    ("Разработка модулей отчетности", "adopted_customer", 15, 12, "негативный", True, True),
                    ("UI тестирование и фиксы", "adopted_customer", 14, 15, "положительный", True, True),
                    ("Поддержка многоязычности", "adopted_customer", 12, 10, "положительный", True, True),
                    ("Настройка тем и стилизация", "adopted_customer", 13, 8, "негативный", True, True),
                    ("Реализация поиска и фильтрации", "adopted_customer", 16, 14, "положительный", True, True),
                    ("Обучение пользователей", "adopted_customer", 14, 10, "негативный", True, True)
                ],
                "integration": [
                    ("Интеграция с системой IoT", "adopted_customer", 15, 13, "негативный", True, True),
                    ("Подключение к ERP-системам клиента", "adopted_customer", 17, 15, "положительный", True, True),
                    ("Реализация вебхуков и событий", "adopted_customer", 14, 17, "негативный", True, True),
                    ("Интеграция с системой аутентификации", "adopted_customer", 13, 19, "положительный", True, True),
                    ("Обмен данными с CRM", "adopted_customer", 14, 10, "положительный", True, True),
                    ("Поддержка протоколов обмена", "adopted_customer", 12, 5, "положительный", True, True),
                    ("Обеспечение безопасности интеграций", "adopted_customer", 15, 10, "положительный", True, True),
                    ("Обработка ошибок интеграций", "adopted_customer", 13, 10, "положительный", True, True),
                    ("Тестирование и отладка интеграций", "adopted_customer", 14, 34, "положительный", True, True),
                    ("Документирование интеграционных API", "adopted_customer", 12, 15, "положительный", True, True),
                    ("Мониторинг интеграционных процессов", "adopted_customer", 13, 10, "положительный", True, True),
                    ("Оптимизация производительности интеграций", "adopted_customer", 14, 9, "негативный", True, True),
                    ("Настройка очередей и брокеров сообщений", "adopted_customer", 15, 10, "положительный", True, True),
                    ("Автоматизация обновления интеграций", "adopted_customer", 13, 14, "негативный", True, True)
                ],
                "devops": [
                    ("Проектирование CI/CD pipeline", "adopted_customer", 15, 13, "негативный", True, True),
                    ("Автоматизация развертывания", "adopted_customer", 16, 14, "положительный", True, True),
                    ("Настройка мониторинга и алертинга", "adopted_customer", 14, 17, "негативный", True, True),
                    ("Организация резервного копирования", "adopted_customer", 13, 12, "положительный", True, True),
                    ("Оптимизация ресурсов серверов", "adopted_customer", 15, 13, "положительный", True, True),
                    ("Настройка контейнеризации (Docker/K8s)", "adopted_customer", 16, 8, "негативный", True, True),
                    ("Безопасность и аудит инфраструктуры", "adopted_customer", 14, 12, "негативный", True, True),
                    ("Поддержка и обновление DevOps инструментов", "adopted_customer", 15, 43, "положительный", True, True),
                    ("Организация логирования (ELK)", "adopted_customer", 13, 11, "негативный", True, True),
                    ("Документирование инфраструктуры", "adopted_customer", 12, 11, "положительный", True, True),
                    ("Обеспечение высокой доступности", "adopted_customer", 14, 20, "положительный", True, True),
                    ("Обучение команды DevOps практикам", "adopted_customer", 15, 14, "положительный", True, True),
                    ("Обновление и миграции инфраструктуры", "adopted_customer", 13, 11, "негативный", True, True),
                    ("Оптимизация процессов CI/CD", "adopted_customer", 14, 25, "положительный", True, True)
                ],
                "database": [
                    ("Проектирование схемы базы данных", "adopted_customer", 15, 2, "негативный", True, True),
                    ("Оптимизация запросов", "adopted_customer", 16, 13, "положительный", True, True),
                    ("Настройка репликации и резервного копирования", "adopted_customer", 14, 16, "негативный", True, True),
                    ("Миграции и управление версиями", "adopted_customer", 13, 3, "негативный", True, True),
                    ("Обеспечение целостности данных", "adopted_customer", 15, 13, "положительный", True, True),
                    ("Настройка индексов и производительности", "adopted_customer", 16, 2, "положительный", True, True),
                    ("Анализ и оптимизация загрузки", "adopted_customer", 14, 12, "негативный", True, True),
                    ("Поддержка высоконагруженных систем", "adopted_customer", 13, 9, "положительный", True, True),
                    ("Мониторинг и алертинг базы данных", "adopted_customer", 15, 14, "положительный", True, True),
                    ("Документирование структуры БД", "adopted_customer", 12, 19, "положительный", True, True),
                    ("Обучение команды работе с БД", "adopted_customer", 14, 13, "положительный", True, True),
                    ("Реализация хранимых процедур и триггеров", "adopted_customer", 15, 13, "негативный", True, True),
                    ("Обеспечение безопасности данных", "adopted_customer", 14, 20, "негативный", True, True),
                    ("Оптимизация транзакций", "adopted_customer", 13, 12, "положительный", True, True)
                ],
                "ml_ai": [
                    ("Исследование данных для моделей", "adopted_customer", 15, 13, "негативный", True, True),
                    ("Разработка моделей машинного обучения", "adopted_customer", 16, 14, "положительный", True, True),
                    ("Тестирование и валидация моделей", "adopted_customer", 14, 12, "негативный", True, True),
                    ("Оптимизация гиперпараметров", "adopted_customer", 13, 11, "негативный", True, True),
                    ("Интеграция моделей в систему", "adopted_customer", 15, 13, "положительный", True, True),
                    ("Мониторинг качества моделей", "adopted_customer", 16, 19, "положительный", True, True),
                    ("Обучение персонала работе с моделями", "adopted_customer", 14, 12, "негативный", True, True),
                    ("Обеспечение масштабируемости решений", "adopted_customer", 13, 11, "негативный", True, True),
                    ("Разработка алгоритмов предсказания", "adopted_customer", 15, 20, "положительный", True, True),
                    ("Документирование исследований и моделей", "adopted_customer", 12, 11, "положительный", True, True),
                    ("Обработка и подготовка данных", "adopted_customer", 14, 12, "негативный", True, True),
                    ("Разработка и поддержка пайплайнов данных", "adopted_customer", 15, 24, "негативный", True, True),
                    ("Анализ результатов моделей", "adopted_customer", 13, 12, "положительный", True, True),
                    ("Оптимизация вычислительных ресурсов", "adopted_customer", 14, 54, "положительный", True, True)
                ]
            }


        base_date = datetime(2023, 4, 5)

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
                    scheduled_day=planned // 4,
                    actual_hours=fact,
                    actual_day=fact // 4,
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