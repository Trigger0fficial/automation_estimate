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
            "testing": Staff.objects.filter(category="2", department__name="testing").first(),
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
            type="2",  # Тип проекта: средний
            name="CRM Модуль учёта взаимодействия с клиентами",
            data_start=datetime(2024, 10, 10).date(),
            data_end=datetime(2025, 2, 3).date(),
            additional_costs=add_costs,
            payment_client=750000,
            total_cost=980000,
            expected_costs=780000,
            actual_costs=765000,
            expected_profits=200000,
            actual_profits=215000,
            status="Finished"
        )
        project.staff.set(list(staff_by_role.values()) + [customer])

        # Обновлённый словарь с двумя дополнительными булевыми значениями: is_done и is_report_approved
        tasks_by_role = {
            "backend": [
                ("Проектирование моделей документов", "adopted_customer", 8, 7, "положительный", True, True),
                ("Реализация бизнес-логики маршрутов согласования", "adopted_customer", 10, 10, "положительный", True,
                 True),
                ("API создания и обновления карточек", "adopted_customer", 9, 9, "положительный", True, True),
                ("Механизм автоматической архивации", "adopted_customer", 6, 7, "положительный", True, True),
                ("Проверка цифровой подписи", "adopted_customer", 7, 8, "положительный", True, True),
                ("API комментариев и истории действий", "adopted_customer", 6, 6, "положительный", True, True),
                ("Подсистема статусов документов", "adopted_customer", 7, 7, "положительный", True, True),
                ("Поддержка шаблонов договоров", "adopted_customer", 9, 10, "положительный", True, True),
                ("Асинхронная обработка вложений", "adopted_customer", 6, 5, "положительный", True, True),
                ("Обработка ошибок и логирование", "adopted_customer", 5, 6, "положительный", True, True),
                ("Контроль целостности документов", "adopted_customer", 6, 7, "положительный", True, True),
                ("Сервис конвертации форматов (PDF/DOCX)", "adopted_customer", 7, 6, "положительный", True, True),
                ("Подключение к электронной подписи (API КриптоПро)", "adopted_customer", 10, 11, "положительный", True,
                 True)
            ],
            "frontend": [
                ("Интерфейс фильтрации и поиска", "adopted_customer", 8, 10, "положительный", True, True),
                ("Разметка карточки документа", "adopted_customer", 7, 12, "положительный", True, True),
                ("UI согласования и маршрутов", "adopted_customer", 6, 4, "положительный", True, True),
                ("Анимации статуса и прогресса", "adopted_customer", 5, 9, "положительный", True, True),
                ("Модальное окно предпросмотра", "adopted_customer", 6, 10, "положительный", True, True),
                ("Настройка тем и цветовых схем", "adopted_customer", 5, 4, "положительный", True, True),
                ("Поддержка drag-n-drop загрузки", "adopted_customer", 7, 8, "положительный", True, True),
                ("UI уведомлений и всплывающих подсказок", "adopted_customer", 6, 2, "положительный", True, True),
                ("Форма отправки документа на подпись", "adopted_customer", 8, 4, "положительный", True, True),
                ("Адаптивная вёрстка под мобильные", "adopted_customer", 5, 10, "положительный", True, True),
                ("Интеграция с Vuex и маршрутизация", "adopted_customer", 7, 12, "положительный", True, True),
                ("UI-функциональность комментариев", "adopted_customer", 6, 4, "положительный", True, True)
            ],
            "integration": [
                ("Интеграция с LDAP (Active Directory)", "adopted_customer", 6, 10, "положительный", True, True),
                ("Интеграция с системой Росреестр", "adopted_customer", 8, 7, "положительный", True, True),
                ("Подключение к 1С:Документооборот", "adopted_customer", 10, 12, "положительный", True, True),
                ("Интеграция с почтовым шлюзом SMTP", "adopted_customer", 6, 10, "положительный", True, True),
                ("Интеграция с ЭЦП (API внешнего сервиса)", "adopted_customer", 7, 14, "положительный", True, True),
                ("Импорт и экспорт в Excel", "adopted_customer", 7, 10, "положительный", True, True),
                ("Настройка вебхуков", "adopted_customer", 6, 12, "положительный", True, True),
                ("API обратной синхронизации", "adopted_customer", 5, 15, "положительный", True, True),
                ("Интеграция с внутренней CRM", "adopted_customer", 8, 1, "положительный", True, True),
                ("Интеграция с внешним сканером документов", "adopted_customer", 6, 14, "положительный", True, True),
                ("Webhook нотификации", "adopted_customer", 5, 3, "положительный", True, True)
            ],
            "devops": [
                ("Настройка CI/CD для backend", "adopted_customer", 6, 15, "положительный", True, True),
                ("CI/CD pipeline для frontend", "adopted_customer", 6, 5, "положительный", True, True),
                ("Docker-контейнеризация всех модулей", "adopted_customer", 7, 3, "положительный", True, True),
                ("Мониторинг с использованием Prometheus", "adopted_customer", 5, 6, "положительный", True, True),
                ("Настройка логирования через ELK", "adopted_customer", 6, 10, "положительный", True, True),
                ("Резервное копирование и восстановление", "adopted_customer", 6, 14, "положительный", True, True),
                ("Развёртывание на K8s кластере", "adopted_customer", 8, 12, "положительный", True, True),
                ("Обеспечение безопасности DevOps процессов", "adopted_customer", 7, 5, "положительный", True, True)
            ],
            "database": [
                ("Оптимизация запросов и индексов", "adopted_customer", 6, 4, "положительный", True, True),
                ("Миграции схемы базы данных", "adopted_customer", 5, 4, "положительный", True, True),
                ("Репликация и резервное копирование", "adopted_customer", 7, 6, "положительный", True, True),
                ("Тюнинг производительности", "adopted_customer", 6, 3, "положительный", True, True),
                ("Настройка безопасности БД", "adopted_customer", 5, 20, "положительный", True, True),
                ("Документирование структуры БД", "adopted_customer", 5, 10, "положительный", True, True)
            ],
            "testing": [
                ("Разработка тест-кейсов для backend", "adopted_customer", 7, 10, "положительный", True, True),
                ("Написание интеграционных тестов", "adopted_customer", 7, 6, "положительный", True, True),
                ("Автоматизация UI тестирования", "adopted_customer", 6, 10, "положительный", True, True),
                ("Нагрузочное тестирование", "adopted_customer", 6, 9, "положительный", True, True),
                ("Проведение регрессионного тестирования", "adopted_customer", 5, 8, "положительный", True, True),
                ("Отчёты по качеству и покрытию", "adopted_customer", 5, 2, "положительный", True, True)
            ]
        }

        base_date = datetime(2024, 10, 10)

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