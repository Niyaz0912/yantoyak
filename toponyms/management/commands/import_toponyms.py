import csv
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from toponyms.models import Toponym

class Command(BaseCommand):
    help = 'Импорт топонимов из CSV файла'
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Путь к CSV файлу')
    
    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f'Файл не найден: {csv_file}'))
            return
        
        # Получаем или создаем пользователя для импорта
        admin_user, created = User.objects.get_or_create(
            username='import_bot',
            defaults={'email': 'import@yantoyak.ru', 'is_staff': True}
        )
        
        imported_count = 0
        skipped_count = 0
        
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Пропускаем если уже существует
                if Toponym.objects.filter(reg_number=row['ID']).exists():
                    skipped_count += 1
                    continue
                
                # Создаем топоним
                try:
                    # Определяем тип объекта
                    type_mapping = {
                        'урочище': 'tract',
                        'гора': 'mountain',
                        'скала': 'rock',
                        'родник': 'spring',
                        'ключ': 'spring',
                        'источник': 'spring',
                        'лес': 'forest',
                        'роща': 'forest',
                        'бор': 'forest',
                        'поле': 'field',
                        'луг': 'field',
                        'овраг': 'ravine',
                        'лог': 'ravine',
                        'долина': 'other',
                        'ущелье': 'other',
                        'пещера': 'other',
                        'грот': 'other',
                        'камень': 'rock',
                        'останец': 'rock',
                        'увал': 'mountain',
                        'курган': 'other',
                        'месторождение': 'other',
                        'обрыв': 'rock',
                        'перевал': 'other',
                        'кряж': 'mountain',
                        'хребет': 'mountain'
                    }
                    
                    obj_type = row['Type'].lower()
                    django_type = type_mapping.get(obj_type, 'other')
                    
                    # Создаем запись
                    Toponym.objects.create(
                        name_rus=row['Name'][:200],  # Ограничиваем длину
                        name_bash='',  # Пока нет башкирских названий
                        type=django_type,
                        latitude=float(row['Latitude']),
                        longitude=float(row['Longitude']),
                        description=row.get('Description', '')[:500],
                        reg_number=row['ID'],
                        map_nomenclature=row.get('Map_Code', ''),
                        status='published',
                        created_by=admin_user,
                        votes_for=0,
                        votes_against=0
                    )
                    
                    imported_count += 1
                    
                    if imported_count % 100 == 0:
                        self.stdout.write(f'Импортировано {imported_count}...')
                        
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Ошибка при импорте {row["ID"]}: {e}'))
                    skipped_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Импорт завершен. Импортировано: {imported_count}, Пропущено: {skipped_count}'
        ))