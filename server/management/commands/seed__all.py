from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Запускает все сиды по порядку: пользователей и проекты 1–8.'

    def handle(self, *args, **options):
        seeds = [
            'seed__user',
            'seed__project1',
            'seed__project2',
            'seed__project3',
            'seed__project4',
            'seed__project5',
            'seed__project6',
            'seed__project7',
            'seed__project8',
        ]

        for seed in seeds:
            self.stdout.write(self.style.NOTICE(f'→ Запуск {seed}...'))
            try:
                call_command(seed)
                self.stdout.write(self.style.SUCCESS(f'✔ Успешно выполнен: {seed}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✖ Ошибка в {seed}: {e}'))
                raise CommandError(f'Прерывание: ошибка при выполнении {seed}')