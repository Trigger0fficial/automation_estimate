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
            type="3",  # Тип проекта: большой (до 15 человек)
            name="ML-платформа прогнозирования и оптимизации аграрного производства",
            data_start=datetime(2020, 2, 1).date(),
            data_end=datetime(2021, 7, 31).date(),
            additional_costs=add_costs,
            payment_client=5200000,
            total_cost=4800000,
            expected_costs=4500000,
            actual_costs=4400000,
            expected_profits=700000,
            actual_profits=800000,
            status="Finished"
        )

        # Участники (12 человек), в данном примере - словарь с ключами ролей и списками сотрудников
        project.staff.set(list(staff_by_role.values()) + [customer])


        # Обновлённый словарь с двумя дополнительными булевыми значениями: is_done и is_report_approved
        tasks_by_role = {

                "backend": [
                    ("Разработка API для предсказаний модели", "adopted_customer", 16, 34, "положительный", True, True),
                    ("Сервис сбора обучающих данных", "adopted_customer", 14, 20, "положительный", True, True),
                    ("Реализация очередей задач инференса", "adopted_customer", 15, 21, "негативный", True, True),
                    ("REST API для настройки модели", "adopted_customer", 13, 12, "негативный", True, True),
                    ("Панель мониторинга процессов обучения", "adopted_customer", 150, 240, "положительный", True, True),
                    ("Асинхронная обработка входящих запросов", "adopted_customer", 14, 16, "положительный", True, True),
                    ("Поддержка версий моделей", "adopted_customer", 11, 10, "негативный", True, True),
                    ("Механизм логирования действий пользователей", "adopted_customer", 13, 17, "негативный", True, True),
                    ("Сервис агрегации результатов инференса", "adopted_customer", 12, 11, "положительный", True, True),
                    ("Интерфейс авторизации по токену", "adopted_customer", 11, 10, "положительный", True, True),
                    ("API-документация через Swagger", "adopted_customer", 10, 9, "положительный", True, True),
                    ("Реализация нотаций в API", "adopted_customer", 12, 11, "положительный", True, True)
                ],
                "frontend": [
                    ("Визуализация результатов моделей", "adopted_customer", 150, 134, "положительный", True, True),
                    ("Интерфейс настройки гиперпараметров", "adopted_customer", 13, 20, "негативный", True, True),
                    ("SPA на Vue для панели управления", "adopted_customer", 15, 25, "положительный", True, True),
                    ("Реализация авторизации через JWT", "adopted_customer", 12, 12, "положительный", True, True),
                    ("Интерактивные графики и диаграммы", "adopted_customer", 12, 34, "положительный", True, True),
                    ("Подключение к API инференса", "adopted_customer", 13, 20, "негативный", True, True),
                    ("Отображение истории запусков моделей", "adopted_customer", 11, 10, "положительный", True, True),
                    ("Профиль пользователя и настройки", "adopted_customer", 12, 20, "положительный", True, True),
                    ("Поддержка темной темы", "adopted_customer", 10, 10, "положительный", True, True),
                    ("Форма обратной связи", "adopted_customer", 10, 9, "негативный", True, True),
                    ("SSR для улучшения SEO", "adopted_customer", 13, 14, "положительный", True, True)
                ],
                "integration": [
                    ("Интеграция с системой учета 1С", "adopted_customer", 14, 10, "негативный", True, True),
                    ("Передача данных в Power BI", "adopted_customer", 13, 15, "положительный", True, True),
                    ("Обработка событий от SCADA-систем", "adopted_customer", 12, 11, "положительный", True, True),
                    ("Обмен результатами с CRM Bitrix24", "adopted_customer", 13, 8, "положительный", True, True),
                    ("Обработка webhook от сторонних систем", "adopted_customer", 11, 10, "положительный", True, True),
                    ("Интеграция с внутренней BI платформой", "adopted_customer", 14, 14, "положительный", True, True),
                    ("Синхронизация расписания с Outlook API", "adopted_customer", 12, 32, "негативный", True, True),
                    ("Передача логов в Grafana", "adopted_customer", 10, 9, "положительный", True, True),
                    ("Работа с файловыми хранилищами AWS", "adopted_customer", 11, 10, "положительный", True, True),
                    ("Интеграция с платёжным шлюзом", "adopted_customer", 13, 75, "положительный", True, True)
                ],
                "devops": [
                    ("Настройка CI/CD пайплайнов", "adopted_customer", 14, 16, "положительный", True, True),
                    ("Деплой моделей в Docker", "adopted_customer", 13, 12, "положительный", True, True),
                    ("Мониторинг через Prometheus", "adopted_customer", 12, 18, "положительный", True, True),
                    ("Оркестрация с Kubernetes", "adopted_customer", 15, 14, "негативный", True, True),
                    ("Ротация логов через Fluentd", "adopted_customer", 12, 22, "негативный", True, True),
                    ("Настройка NGINX для API", "adopted_customer", 11, 11, "положительный", True, True),
                    ("Оптимизация использования ресурсов", "adopted_customer", 13, 12, "положительный", True, True),
                    ("Инфраструктура как код через Terraform", "adopted_customer", 14, 13, "положительный", True, True),
                    ("Автоматизация резервного копирования", "adopted_customer", 11, 8, "положительный", True, True),
                    ("Конфигурация dev/prod окружений", "adopted_customer", 12, 19, "положительный", True, True)
                ],
                "database": [
                    ("Проектирование схемы хранения метрик", "adopted_customer", 14, 13, "положительный", True, True),
                    ("Оптимизация запросов к результатам моделей", "adopted_customer", 13, 11, "негативный", True, True),
                    ("Нормализация таблиц логов", "adopted_customer", 12, 12, "положительный", True, True),
                    ("Индексация таблиц по ключевым полям", "adopted_customer", 13, 8, "положительный", True, True),
                    ("Резервное копирование через pg_dump", "adopted_customer", 11, 10, "положительный", True, True),
                    ("Архивирование старых данных", "adopted_customer", 12, 11, "положительный", True, True),
                    ("Мониторинг нагрузки на базу", "adopted_customer", 11, 10, "негативный", True, True),
                    ("Проектирование модели ManyToMany связей", "adopted_customer", 14, 22, "негативный", True, True),
                    ("Репликация между инстансами", "adopted_customer", 15, 14, "положительный", True, True),
                    ("Аудит изменений через триггеры", "adopted_customer", 13, 34, "положительный", True, True)
                ],
                "ml_ai": [
                    ("Исследование данных для моделей", "adopted_customer", 15, 13, "негативный", True, True),
                    ("Разработка моделей машинного обучения", "adopted_customer", 16, 14, "положительный", True, True),
                    ("Тестирование и валидация моделей", "adopted_customer", 14, 20, "негативный", True, True),
                    ("Оптимизация гиперпараметров", "adopted_customer", 13, 11, "негативный", True, True),
                    ("Интеграция моделей в систему", "adopted_customer", 15, 13, "положительный", True, True),
                    ("Мониторинг качества моделей", "adopted_customer", 16, 40, "положительный", True, True),
                    ("Обучение персонала работе с моделями", "adopted_customer", 14, 12, "негативный", True, True),
                    ("Обеспечение масштабируемости решений", "adopted_customer", 13, 17, "негативный", True, True),
                    ("Разработка алгоритмов предсказания", "adopted_customer", 15, 14, "положительный", True, True),
                    ("Документирование исследований и моделей", "adopted_customer", 12, 18, "положительный", True, True),
                    ("Обработка и подготовка данных", "adopted_customer", 14, 12, "негативный", True, True),
                    ("Разработка и поддержка пайплайнов данных", "adopted_customer", 15, 8, "негативный", True, True),
                    ("Анализ результатов моделей", "adopted_customer", 13, 12, "положительный", True, True),
                    ("Оптимизация вычислительных ресурсов", "adopted_customer", 14, 20, "положительный", True, True)
                ],
                "documentation": [
                    ("Подготовка архитектурного описания", "adopted_customer", 14, 13, "положительный", True, True),
                    ("Документация REST API", "adopted_customer", 13, 12, "положительный", True, True),
                    ("Описание моделей ML", "adopted_customer", 22, 32, "положительный", True, True),
                    ("Confluence для бизнес-процессов", "adopted_customer", 13, 32, "положительный", True, True),
                    ("Swagger UI описание эндпоинтов", "adopted_customer", 11, 5, "положительный", True, True),
                    ("Глоссарий терминов", "adopted_customer", 20,39, "негативный", True, True),
                    ("Чек-листы для тестировщиков", "adopted_customer", 12, 21, "положительный", True, True),
                    ("Ведение changelog", "adopted_customer", 11, 11, "положительный", True, True),
                    ("Описание процедур инференса", "adopted_customer", 42, 51, "положительный", True, True),
                    ("Документация для клиента", "adopted_customer", 23, 32, "положительный", True, True)
                ],
                "ux_ui": [
                    ("Проработка пользовательских сценариев", "adopted_customer", 34, 33, "положительный", True, True),
                    ("Прототипирование панели управления", "adopted_customer", 33, 31, "негативный", True, True),
                    ("Юзабилити-тесты с заказчиком", "adopted_customer", 32, 32, "положительный", True, True),
                    ("Интерактивные прототипы в Figma", "adopted_customer", 13, 12, "положительный", True, True),
                    ("UX анализ загрузки данных", "adopted_customer", 31, 30, "положительный", True, True),
                    ("Редизайн дашбордов", "adopted_customer", 32, 32, "положительный", True, True),
                    ("Поддержка адаптивности интерфейса", "adopted_customer", 31, 30, "положительный", True, True),
                    ("Работа с цветовой схемой", "adopted_customer", 30, 3, "негативный", True, True),
                    ("Настройка шрифта и типографики", "adopted_customer", 31, 30, "положительный", True, True),
                    ("Интерфейс отображения ошибок", "adopted_customer", 32, 31, "положительный", True, True)
                ],
                "testing": [
                    ("E2E тесты UI", "adopted_customer", 34, 35, "негативный", True, True),
                    ("Юнит-тесты backend логики", "adopted_customer", 33, 33, "положительный", True, True),
                    ("Нагрузочное тестирование API", "adopted_customer", 35, 34, "положительный", True, True),
                    ("Проверка безопасности авторизации", "adopted_customer", 32, 38, "негативный", True, True),
                    ("Smoke-тесты перед релизом", "adopted_customer", 31, 31, "положительный", True, True),
                    ("Регрессионные тесты моделей", "adopted_customer", 33, 32, "положительный", True, True),
                    ("Тестирование кроссбраузерности UI", "adopted_customer", 30, 23, "негативный", True, True),
                    ("Тестирование мобильной версии", "adopted_customer", 32, 31, "положительный", True, True),
                    ("Проверка корректности метрик", "adopted_customer", 33, 37, "положительный", True, True),
                    ("Контроль качества данных", "adopted_customer", 34, 36, "положительный", True, True)
                ]

            }


        base_date = datetime(2020, 2, 1)

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