import pdfplumber
import re
import pandas as pd
from collections import defaultdict

def parse_pdf_correct(file_path):
    """Парсер с правильным определением полей"""
    all_text = []
    
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.extend(text.split('\n'))
    
    return all_text

def extract_records_correct(lines):
    """Правильное извлечение записей"""
    records = []
    
    for i in range(len(lines)):
        line = lines[i].strip()
        if not line or not re.match(r'^\d{7}\b', line):
            continue
        
        # Это строка с данными
        parts = line.split()
        
        # Ищем координаты в строке
        lat_idx = -1
        lon_idx = -1
        
        for j, part in enumerate(parts):
            if '°' in part and "'" in part:
                if lat_idx == -1:
                    lat_idx = j
                elif lon_idx == -1:
                    lon_idx = j
        
        # Если нашли обе координаты
        if lat_idx != -1 and lon_idx != -1:
            # Все между названием и первой координатой - это тип объекта
            # Название начинается с индекса 1 (после регистрационного номера)
            # Тип объекта - всё между названием и координатами
            
            # Простой подход: предполагаем, что тип - это одно слово перед координатами
            name_parts = []
            obj_type = ""
            
            for j in range(1, lat_idx):
                part = parts[j]
                # Проверяем, не координата ли это
                if '°' not in part:
                    # Проверяем, не тип ли это объекта (обычно одно слово)
                    if j == lat_idx - 1 and not any(c.isdigit() for c in part):
                        obj_type = part
                    else:
                        name_parts.append(part)
                else:
                    break
            
            name = ' '.join(name_parts) if name_parts else parts[1]
            
            # Если тип не определили, пробуем определить по следующей строке
            if not obj_type and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not re.match(r'^\d', next_line):
                    # Возможно, в следующей строке есть тип
                    next_parts = next_line.split()
                    if next_parts and not any('°' in p for p in next_parts):
                        obj_type = next_parts[0]
            
            # Код карты обычно после координат
            map_code = parts[lon_idx + 1] if lon_idx + 1 < len(parts) else ""
            
            records.append({
                'reg_num': parts[0],
                'name': name,
                'type': obj_type,
                'lat': parts[lat_idx],
                'lon': parts[lon_idx],
                'map_code': map_code,
                'description': ''
            })
    
    # Добавляем описания
    for i in range(len(lines)):
        line = lines[i].strip()
        if not line or re.match(r'^\d{7}\b', line):
            continue
        
        # Ищем, к какой записи относится это описание
        for rec in records:
            if not rec['description'] and i > 0:
                prev_line = lines[i-1].strip() if i-1 >= 0 else ""
                if rec['reg_num'] in prev_line:
                    rec['description'] = line
                    break
    
    return records

def convert_coordinates(coord):
    """Конвертируем координаты"""
    if not coord or '°' not in coord:
        return None
    
    try:
        coord = coord.replace("'", "").strip()
        degrees, minutes = coord.split('°')
        
        deg = float(degrees.strip())
        min_val = float(minutes.strip()) if minutes else 0
        
        return round(deg + (min_val / 60), 6)
    except:
        return None

def main():
    print("Чтение PDF...")
    lines = parse_pdf_correct("реестр.pdf")
    
    print("Извлечение записей...")
    records = extract_records_correct(lines)
    print(f"Найдено записей: {len(records)}")
    
    if not records:
        print("Проверяем первые 30 строк:")
        for i, line in enumerate(lines[:30]):
            print(f"{i:3}: {line}")
        return
    
    # Выводим первые 10 для анализа
    print("\nПервые 10 записей (для проверки структуры):")
    for i, rec in enumerate(records[:10]):
        print(f"{i+1:2}. {rec['reg_num']} | {rec['name']:20} | {rec['type']:15} | {rec['lat']} {rec['lon']}")
        if rec['description']:
            print(f"     Описание: {rec['description']}")
    
    # Фильтруем
    include_types = {
        'урочище', 'гора', 'скала', 'холм', 'возвышенность', 'вершина',
        'родник', 'источник', 'ключ', 'колодец',
        'лес', 'роща', 'бор', 'поле', 'луг', 'поляна',
        'овраг', 'лог', 'долина', 'ущелье', 'каньон',
        'пещера', 'грот', 'камень', 'останец', 'увал',
        'курган', 'месторождение', 'обрыв', 'перевал', 'кряж', 'хребет'
    }
    
    exclude_types = {
        'река', 'озеро', 'деревня', 'село', 'город', 'посёлок', 'поселок',
        'станция', 'разъезд', 'ж.-д.', 'пруд', 'водохранилище',
        'ручей', 'канал', 'протока', 'залив', 'пролив', 'болото'
    }
    
    data = []
    type_stats = defaultdict(int)
    
    for rec in records:
        obj_type = rec['type'].lower().strip()
        type_stats[obj_type] += 1
        
        if not obj_type:
            continue
            
        # Пропускаем исключенные типы
        if any(excl in obj_type for excl in exclude_types):
            continue
        
        # Включаем нужные типы
        if any(incl in obj_type for incl in include_types):
            lat = convert_coordinates(rec['lat'])
            lon = convert_coordinates(rec['lon'])
            
            if lat and lon:
                data.append({
                    'ID': rec['reg_num'],
                    'Название': rec['name'],
                    'Тип': rec['type'],
                    'Широта': lat,
                    'Долгота': lon,
                    'Карта': rec['map_code'],
                    'Описание': rec['description'].strip(),
                    'Источник': 'АГКГН'
                })
    
    print(f"\n\nСтатистика:")
    print(f"Всего записей: {len(records)}")
    print(f"Отфильтровано: {len(data)}")
    
    # Статистика по типам
    print("\nТипы объектов (топ-20):")
    for typ, count in sorted(type_stats.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {typ}: {count}")
    
    # Сохраняем
    if data:
        df = pd.DataFrame(data)
        
        # CSV для Google My Maps
        df.to_csv('toponyms_filtered_final.csv', index=False, encoding='utf-8-sig')
        print(f"\nСохранено в toponyms_filtered_final.csv ({len(df)} записей)")
        
        # Показываем пример
        print("\nПримеры записей:")
        print(df[['Название', 'Тип', 'Широта', 'Долгота']].head(5).to_string())
        
        # Также сохраняем все записи для отладки
        all_data = []
        for rec in records[:100]:
            all_data.append(rec)
        
        pd.DataFrame(all_data).to_csv('all_records_sample.csv', index=False, encoding='utf-8-sig')
        print("\nПервые 100 записей сохранены в all_records_sample.csv для отладки")
    else:
        print("Нет данных для сохранения!")

if __name__ == "__main__":
    main()