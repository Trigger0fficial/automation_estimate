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
            "frontend": Staff.objects.filter(category="2", department__name="frontend").first(),
            "ux_ui": Staff.objects.filter(category="2", department__name="ux_ui").first(),
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
            type="4",  # Тип: крупный
            name="Платформа управления цифровыми активами предприятия",
            data_start=datetime(2021, 3, 15).date(),
            data_end=datetime(2022, 11, 20).date(),
            additional_costs=add_costs,
            payment_client=7200000,
            total_cost=6700000,
            expected_costs=6550000,
            actual_costs=6480000,
            expected_profits=650000,
            actual_profits=720000,
            status="Finished"
        )

        # Участники (12 человек), в данном примере - словарь с ключами ролей и списками сотрудников
        project.staff.set(list(staff_by_role.values()) + [customer])


        # Обновлённый словарь с двумя дополнительными булевыми значениями: is_done и is_report_approved
        tasks_by_role = {
            "backend": [
                ("Разработка API управления активами #1", "adopted_customer", 42, 51, "положительный", True, True),
                ("Интеграция с внутренней ERP-системой #2", "adopted_customer", 40, 38, "положительный", True, True),
                ("Аутентификация и авторизация пользователей #3", "adopted_customer", 38, 37, "негативный", True, True),
                ("Обработка вложенных транзакций #4", "adopted_customer", 45, 43, "положительный", True, True),
                ("Разработка микросервисов учета #5", "adopted_customer", 36, 54, "положительный", True, True),
                ("Система аудита действий #6", "adopted_customer", 32, 30, "негативный", True, True),
                ("Импорт данных из Excel #7", "adopted_customer", 34, 32, "положительный", True, True),
                ("Модуль журналирования ошибок #8", "adopted_customer", 28, 36, "положительный", True, True),
                ("API документация Swagger #9", "adopted_customer", 26, 25, "негативный", True, True),
                ("Настройка политик доступа #10", "adopted_customer", 22, 51, "положительный", True, True),
                ("Механизмы обработки вложенных активов #11", "adopted_customer", 33, 32, "положительный", True, True),
                ("Интеграция с внешними API #12", "adopted_customer", 40, 39, "негативный", True, True),
                ("Настройка очередей Celery #13", "adopted_customer", 35, 33, "положительный", True, True),
                ("Обработка логов и метрик #14", "adopted_customer", 31, 59, "негативный", True, True),
                ("Валидация входящих данных #15", "adopted_customer", 29, 27, "положительный", True, True),
                ("Создание экспортных модулей #16", "adopted_customer", 25, 53, "положительный", True, True),
            ],
            "frontend": [
                ("Интерфейс управления активами #1", "adopted_customer", 40, 28, "положительный", True, True),
                ("Дашборды состояния ресурсов #2", "adopted_customer", 36, 34, "положительный", True, True),
                ("Форма создания активов #3", "adopted_customer", 28, 27, "негативный", True, True),
                ("Фильтрация и поиск по параметрам #4", "adopted_customer", 24, 23, "положительный", True, True),
                ("Отображение связей между объектами #5", "adopted_customer", 30, 29, "положительный", True, True),
                ("Адаптивная верстка интерфейсов #6", "adopted_customer", 26, 25, "негативный", True, True),
                ("Механизмы уведомлений #7", "adopted_customer", 22, 21, "положительный", True, True),
                ("Интерфейс редактирования объектов #8", "adopted_customer", 20, 29, "положительный", True, True),
                ("Привязка к картам активов #9", "adopted_customer", 34, 33, "негативный", True, True),
                ("История изменений и версионность #10", "adopted_customer", 28, 26, "положительный", True, True),
                ("Поддержка темной темы #11", "adopted_customer", 18, 17, "негативный", True, True),
                ("Работа с вложенными элементами #12", "adopted_customer", 23, 22, "положительный", True, True),
                ("Анимация и интерактивность #13", "adopted_customer", 19, 28, "положительный", True, True),
                ("Стилизация форм и таблиц #14", "adopted_customer", 25, 24, "негативный", True, True),
                ("Модальные окна и диалоги #15", "adopted_customer", 27, 26, "положительный", True, True),
                ("Подключение к API для визуализации #16", "adopted_customer", 32, 40, "положительный", True, True),
                ("Работа с WebSocket #17", "adopted_customer", 21, 20, "негативный", True, True),
            ],
            "integration": [
                ("Интеграция с системами SAP #1", "adopted_customer", 40, 29, "положительный", True, True),
                ("Настройка Webhook-интерфейсов #2", "adopted_customer", 34, 33, "негативный", True, True),
                ("Обработка REST-запросов внешних систем #3", "adopted_customer", 32, 30, "положительный", True, True),
                ("Импорт из внешнего реестра активов #4", "adopted_customer", 30, 28, "положительный", True, True),
                ("Интеграция с IoT-устройствами #5", "adopted_customer", 26, 24, "негативный", True, True),
                ("Реализация системы подписок #6", "adopted_customer", 22, 21, "положительный", True, True),
                ("Интеграция с системами учета движения #7", "adopted_customer", 24, 43, "положительный", True, True),
                ("Резервное взаимодействие через SOAP #8", "adopted_customer", 118, 147, "негативный", True, True),
            ],
            "database": [
                ("Разработка схемы хранения активов #1", "adopted_customer", 38, 46, "положительный", True, True),
                ("Индексация по типам объектов #2", "adopted_customer", 132, 140, "негативный", True, True),
                (
                "Хранимые процедуры по изменению статусов #3", "adopted_customer", 28, 27, "положительный", True, True),
                ("Репликация данных между модулями #4", "adopted_customer", 26, 25, "положительный", True, True),
                ("Архивирование неактивных объектов #5", "adopted_customer", 22, 21, "негативный", True, True),
                ("Настройка журналирования PostgreSQL #6", "adopted_customer", 24, 22, "положительный", True, True),
                ("Обеспечение отказоустойчивости базы #7", "adopted_customer", 120, 219, "положительный", True, True),
                ("Создание сложных представлений для отчетов #8", "adopted_customer", 25, 13, "негативный", True, True),
            ],
            "devops": [
                ("Организация CI/CD через GitLab #1", "adopted_customer", 36, 34, "положительный", True, True),
                ("Автоматизация деплоя через Ansible #2", "adopted_customer", 30, 28, "положительный", True, True),
                ("Мониторинг через Zabbix и Prometheus #3", "adopted_customer", 28, 36, "негативный", True, True),
                ("Управление секретами Vault #4", "adopted_customer", 24, 23, "положительный", True, True),
                ("Настройка Kubernetes кластера #5", "adopted_customer", 32, 30, "негативный", True, True),
                ("Инфраструктура как код (Terraform) #6", "adopted_customer", 26, 35, "положительный", True, True),
            ],
            "ux_ui": [
                (
                "Пользовательские сценарии редактирования #1", "adopted_customer", 28, 27, "положительный", True, True),
                ("Дизайн управления объектами #2", "adopted_customer", 26, 25, "негативный", True, True),
                ("Оценка UX интерфейсов #3", "adopted_customer", 24, 22, "положительный", True, True),
                ("Проверка на доступность (a11y) #4", "adopted_customer", 120, 139, "негативный", True, True),
                ("Создание макетов с Figma #5", "adopted_customer", 22, 26, "положительный", True, True),
                ("Участие в юзабилити-тестах #6", "adopted_customer", 18, 5, "положительный", True, True),
            ],
        }

        base_date = datetime(2021, 3, 15)

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