from django.db import models
from django.contrib.auth.models import AbstractUser


class TransactionPayment(models.Model):
    class Meta:
        verbose_name = 'Зарплатный проект'
        verbose_name_plural = 'Зарплатный проект'

    FIELD_CAT = [
        ('1', 'Зарплата'),
        ('2', 'Оплата заказчика'),
    ]

    data_salary = models.DateField(verbose_name='Дата оплаты')
    category = models.CharField(verbose_name='Категория', choices=FIELD_CAT, max_length=1)
    payment = models.IntegerField(verbose_name='Оплата')


class Department(models.Model):
    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    name = models.CharField('Должность', max_length=155)
    description = models.TextField('Описание должности', null=True, blank=True)
    bet = models.IntegerField(verbose_name='Ставка')
    bet_local = models.IntegerField(verbose_name='Внутренняя ставка')

    def __str__(self):
        return self.name


class Staff(AbstractUser):
    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователь'

    FIELD_BANK = [
        ('t-bank', 'Т-банк'),
        ('sber', 'Сбербанк'),
        ('alpha', 'Альфа'),
        ('vtb', 'ВТБ'),
        ('other', 'Другое'),
        ('not_bank', 'Отсутствует')
    ]

    FIELD_CAT = [
        ('1', 'Руководитель'),
        ('2', 'Сотрудник'),
        ('3', 'Заказчик')
    ]

    name = models.CharField('ФИО', max_length=155)
    category = models.CharField(verbose_name='Категория', choices=FIELD_CAT, max_length=1)
    department = models.ForeignKey(Department, verbose_name='Должность', on_delete=models.PROTECT, null=True, blank=True)
    transaction = models.ManyToManyField(TransactionPayment, verbose_name='Финансовая транзакция', blank=True, null=True)
    account_bank = models.CharField(verbose_name='Номер счета', max_length=30, null=True, blank=True)
    bank = models.CharField(verbose_name='Банк', max_length=20, choices=FIELD_BANK, default='not_bank', null=True, blank=True)
    notifications = models.ManyToManyField('Notification', verbose_name='Уведомления', blank=True, null=True)


class FileTask(models.Model):
    class Meta:
        verbose_name = 'Файл к задаче'
        verbose_name_plural = 'Файлы к задачам'

    file = models.FileField(verbose_name='Файл', upload_to='project/task/%Y/%m/%d/')


class Task(models.Model):
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    name = models.CharField(verbose_name='Наименование задачи', max_length=155)
    dsc = models.TextField(verbose_name='Описание задачи')
    files = models.ManyToManyField(FileTask, verbose_name='Файлы', blank=True, null=True)
    type = models.CharField(verbose_name='Тип задачи', max_length=40, null=True, blank=True, choices=[('backend', ' Разработка серверной логики, REST API, микросервисов.'),
                                                                               ('frontend', 'Интерфейсная часть, SPA, SSR.'),
                                                                               ('integration', 'Интеграция с внешними API, 1С, CRM, платёжками.'),
                                                                               ('database',
                                                                                'Проектирование и оптимизация БД, миграции, индексы.'),
                                                                               ('devops',
                                                                                'CI/CD, деплой, настройка серверов, мониторинг..'),
                                                                               ('ml_ai',
                                                                                'Модели ИИ, аналитика, обучение, инференс.'),
                                                                               ('mobile',
                                                                                ' iOS/Android разработка.'),
                                                                               ('testing',
                                                                                'Написание unit, e2e, нагрузочное тестирование.'),
                                                                               ('ux_ui',
                                                                                'Проектирование пользовательского опыта, прототипы.'),
                                                                               ('documentation',
                                                                                'Подготовка технической документации, Swagger, Confluence.'),
                                                                               ('architecture',
                                                                                'Проектирование архитектуры решения, паттерны.'),
                                                                               ('security',
                                                                                'Аудит безопасности, защита API, шифрование.'),
                                                                               ('research',
                                                                                'R&D задачи, эксперименты с новыми технологиями.'),
                                                                               ('refactoring',
                                                                                'Улучшение старого кода, устранение технического долга.'),
                                                                               ('support',
                                                                                'Исправление багов, поддержка пользователей.'),
                                                                               ])


class ReportingChapter(models.Model):
    class Meta:
        verbose_name = 'Отчет о разделе'
        verbose_name_plural = 'Отчет о разделах'

    STATUS_FIELD = [
        ('verification', 'На проверке'),
        ('adopted', 'Принят'),
        ('rejected', 'Отклонен')
    ]

    data_start = models.DateTimeField(verbose_name='Дата подачи', auto_created=True)
    data_end = models.DateTimeField(verbose_name='Дата обратной связи', blank=True, null=True)
    report_executor = models.CharField(verbose_name='Отчет от исполнителя', max_length=500)
    comment_customer = models.CharField(verbose_name='Комментарий от заказчика', max_length=500, blank=True, null=True)
    status = models.CharField(verbose_name='Статус', max_length=20, choices=STATUS_FIELD, default='verification')


class Chapter(models.Model):
    class Meta:
        verbose_name = 'Раздел задачи'
        verbose_name_plural = 'Разделы задач'

    STATUS_FIELD = [
        ('Not_started', 'Не начат'),
        ('Started', 'Начат'),
        ('verification', 'На проверке'),
        ('adopted', 'Принят'),
        ('rejected', 'Отклонен')
    ]

    name = models.CharField(verbose_name='Наименование раздела', max_length=155)
    tasks = models.ManyToManyField(Task, verbose_name='Задачи')
    reporting = models.ManyToManyField(ReportingChapter, verbose_name='Отчеты', null=True, blank=True)
    status = models.CharField(verbose_name='Статус', max_length=30, choices=STATUS_FIELD, default='Not_started')


class ReportingTask(models.Model):
    class Meta:
        verbose_name = 'Отчет о задаче'
        verbose_name_plural = 'Отчет о задачах'

    STATUS_FIELD = [
        ('verification', 'На проверке'),
        ('adopted', 'Принят'),
        ('rejected', 'Отклонен')
    ]

    data_start = models.DateTimeField(verbose_name='Дата подачи', auto_created=True)
    data_end = models.DateTimeField(verbose_name='Дата обратной связи', blank=True, null=True)
    report_stuff = models.CharField(verbose_name='Отчет от сотрудника', max_length=500)
    comment_director = models.CharField(verbose_name='Комментарий от директора', max_length=500, blank=True, null=True)
    is_adopted = models.CharField(verbose_name='Принято', choices=STATUS_FIELD, default='verification', max_length=40)


class ActivityTask(models.Model):
    class Meta:
        verbose_name = 'Активность задачи'
        verbose_name_plural = 'Активность задач'

    data_start = models.DateTimeField(verbose_name='Начало')
    data_end = models.DateTimeField(verbose_name='Начало', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Завершена', default=False)


class FeedbackCustomer(models.Model):
    class Meta:
        verbose_name = 'Обратная связь от заказчика'
        verbose_name_plural = 'Обратные связи от заказчика'

    STATUS_FIELD = [
        ('verification', 'На проверке'),
        ('adopted', 'Принят'),
        ('rejected', 'Отклонен')
    ]

    data_start = models.DateTimeField(verbose_name='Дата подачи', auto_created=True)
    data_end = models.DateTimeField(verbose_name='Дата обратной связи', blank=True, null=True)
    report_stuff = models.CharField(verbose_name='Отчет о задаче', max_length=500)
    comment_director = models.CharField(verbose_name='Комментарий от заказчика', max_length=500, blank=True, null=True)
    is_adopted = models.CharField(verbose_name='Принято', choices=STATUS_FIELD,  default='verification', max_length=40)


class SettingTask(models.Model):
    class Meta:
        verbose_name = 'Постановка задачи'
        verbose_name_plural = 'Постановка задач'

    STATUS_FIELD = [
        ('Not_started', 'Не начата'),
        ('Started', 'Начата'),
        ('verification_staff', 'На проверке'),
        ('adopted', 'Принят '),
        ('rejected', 'Отклонен'),
        ('verification', 'На утверждении у заказчика'),
        ('adopted_customer', 'Утверждена заказчиком'),
        ('rejected_customer', 'Отклонено заказчиком'),

    ]

    staff = models.ForeignKey(Staff, verbose_name='Сотрудник', on_delete=models.PROTECT)
    task = models.ForeignKey(Task, verbose_name='Задача', on_delete=models.PROTECT)
    scheduled_hours = models.IntegerField(verbose_name='Плановые часы')
    actual_hours = models.IntegerField(verbose_name='Фактические часы', null=True, blank=True, default=0)
    scheduled_day = models.IntegerField(verbose_name='Плановые дни')
    actual_day = models.IntegerField(verbose_name='Фактические дни', null=True, blank=True, default=0)
    activity = models.ManyToManyField(ActivityTask, verbose_name='Активность проекта', blank=True, null=True)
    reportings = models.ManyToManyField(ReportingTask, verbose_name='Отчеты от сотрудника', null=True, blank=True)
    feedback_customer = models.ManyToManyField(FeedbackCustomer, verbose_name='Обратная связь заказчика', null=True,
                                               blank=True)
    status = models.CharField(verbose_name='Статус', max_length=30, choices=STATUS_FIELD, default='Not_started')
    is_started = models.BooleanField(verbose_name='Активна', default=False)
    is_active = models.BooleanField(verbose_name='Завершена', default=False)


class AdditionalCosts(models.Model):
    class Meta:
        verbose_name = 'Дополнительные затраты'
        verbose_name_plural = 'Дополнительные затраты'

    percent = models.IntegerField(verbose_name='Процент')

    def __str__(self):
        return f'{self.percent}%'


class DocumentProject(models.Model):
    class Meta:
        verbose_name = 'Документы к проекту'
        verbose_name_plural = 'Документы к проектам'

    FIELD_CAT = [
        ('1', 'Договор'),
        ('2', 'Смета'),
        ('3', 'Локальная смета'),
        ('4', 'Доп. соглашение'),
        ('5', 'Платежные документы'),
        ('6', 'Акт о закрытии работ'),
        ('7', 'Приложение к договору'),
        ('8', 'Акт')
    ]

    name = models.CharField(verbose_name='Наименование проекта', max_length=155)
    data_load = models.DateField(verbose_name='Дата загрузки', auto_created=True)
    category = models.CharField(verbose_name='Категория', choices=FIELD_CAT, max_length=2)
    document = models.FileField(verbose_name='Документ', upload_to='project/document/%Y/%m/%d/')


class Project(models.Model):
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    FIELD_STATUS = [
        ('start', 'Оформление'),
        ('Signing_contract', 'Подписание договора'),
        ('Development', 'Разработка'),
        ('Delivery_works', 'Сдача работ'),
        ('Waiting', 'В ожидании'),
        ('Cancel', 'Отменен'),
        ('Completed', 'Завершен')
    ]
    type = models.CharField(verbose_name='Тип проекта', choices=[('1', 'Мини проект (до 3 человек)'),
                                                                 ('2', 'Средний проект (до 7 человек)'),
                                                                 ('3', 'Большой проект (до 12 человек)'),
                                                                 ('4', 'Крупный проект (до 18 человек)')], max_length=30, default='1')
    name = models.CharField(verbose_name='Наименование проекта', max_length=155)
    staff = models.ManyToManyField(Staff, verbose_name='Сотрудники')
    data_start = models.DateField(verbose_name='Дата начала', null=True, blank=True)
    data_end = models.DateField(verbose_name='Дата окончания', null=True, blank=True)
    chapter = models.ManyToManyField(Chapter, verbose_name='Разделы', null=True, blank=True)
    task = models.ManyToManyField(SettingTask, verbose_name='Поставленные задачи', null=True, blank=True)
    transaction = models.ManyToManyField(TransactionPayment, verbose_name='Финансовая транзакция', blank=True,
                                         null=True)
    additional_costs = models.ForeignKey(AdditionalCosts, verbose_name='Дополнительные затраты', on_delete=models.PROTECT)
    status = models.CharField(verbose_name='Статус', choices=FIELD_STATUS, max_length=20, default='start')
    documents = models.ManyToManyField(DocumentProject, verbose_name='Документы', null=True, blank=True)
    payment_client = models.IntegerField(verbose_name='Оплачено клиентом', default=0)
    total_cost = models.IntegerField(verbose_name='Итоговая стоимость', null=True, blank=True, default=0)
    expected_costs = models.IntegerField(verbose_name='Ожидаемые затраты', null=True, blank=True, default=0)
    actual_costs = models.IntegerField(verbose_name='Фактические затраты', null=True, blank=True, default=0)
    expected_profits = models.IntegerField(verbose_name='Ожидаемая прибыль', null=True, blank=True, default=0)
    actual_profits = models.IntegerField(verbose_name='Фактическая прибыль', null=True, blank=True, default=0)


class Notification(models.Model):
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    CAT_FIELDS = [
        ('1', 'Задачи'),
        ('2', 'Встречи'),
        ('3', 'Зарплатный проект'),
    ]

    data_start = models.DateTimeField(verbose_name='Дата создания', auto_created=True, auto_now=True)
    data_end = models.DateTimeField(verbose_name='Дата окончания', null=True, blank=True)
    name = models.CharField(verbose_name='Название', max_length=55)
    category = models.CharField(verbose_name='Категория', max_length=10)
    color_style = models.CharField(verbose_name='Цвет уведомления', max_length=10, default='#6610f2')
    dsc = models.CharField(verbose_name='Описание', max_length=500)
    is_active = models.BooleanField(verbose_name='Активно', default=True)











