# Структура базы данных музыкального магазина

## Схема связей между таблицами

```
musicians (музыканты)
├── id (PK)
├── name
├── role (исполнитель, композитор, дирижер, руководитель)
├── instruments
├── birth_year
└── country

ensembles (ансамбли)
├── id (PK)
├── name
├── type (оркестр, джазовая группа, квартет, квинтет и т.д.)
├── founded_year
├── country
└── description

ensemble_members (участники ансамблей)
├── id (PK)
├── ensemble_id (FK -> ensembles.id)
├── musician_id (FK -> musicians.id)
├── role_in_ensemble
└── joined_year

compositions (музыкальные произведения)
├── id (PK)
├── title
├── composer_id (FK -> musicians.id)
├── genre
├── year_composed
└── duration_minutes

performances (исполнения произведений)
├── id (PK)
├── composition_id (FK -> compositions.id)
├── ensemble_id (FK -> ensembles.id)
├── conductor_id (FK -> musicians.id)
├── recording_date
└── venue

companies (компании-производители)
├── id (PK)
├── name
├── address
├── phone
├── email
└── is_wholesaler

records (пластинки/компакт-диски)
├── id (PK)
├── catalog_number (уникальный номер)
├── title
├── company_id (FK -> companies.id)
├── release_date
├── wholesale_price
├── retail_price
├── current_stock
├── sold_last_year
└── sold_this_year

record_tracks (записи на пластинках)
├── id (PK)
├── record_id (FK -> records.id)
├── performance_id (FK -> performances.id)
└── track_number
```

## Связи между таблицами

1. **musicians ↔ ensembles** (многие-ко-многим через ensemble_members)
   - Музыкант может участвовать в нескольких ансамблях
   - Ансамбль может состоять из нескольких музыкантов

2. **musicians → compositions** (один-ко-многим)
   - Композитор может написать несколько произведений
   - Произведение имеет одного композитора

3. **ensembles → performances** (один-ко-многим)
   - Ансамбль может исполнить несколько произведений
   - Исполнение принадлежит одному ансамблю

4. **compositions → performances** (один-ко-многим)
   - Произведение может быть исполнено несколько раз
   - Исполнение относится к одному произведению

5. **musicians → performances** (один-ко-многим как дирижер)
   - Дирижер может дирижировать несколькими исполнениями
   - Исполнение может иметь одного дирижера

6. **companies → records** (один-ко-многим)
   - Компания может выпустить несколько пластинок
   - Пластинка выпущена одной компанией

7. **records ↔ performances** (многие-ко-многим через record_tracks)
   - Пластинка может содержать несколько исполнений
   - Исполнение может быть записано на нескольких пластинках

## Основные запросы для функционала

### 1. Количество произведений ансамбля
```sql
SELECT DISTINCT c.title, c.genre, c.year_composed, m.name as composer_name
FROM compositions c
JOIN performances p ON c.id = p.composition_id
JOIN ensemble_members em ON p.ensemble_id = em.ensemble_id
LEFT JOIN musicians m ON c.composer_id = m.id
WHERE p.ensemble_id = ?
ORDER BY c.title
```

### 2. Названия дисков ансамбля
```sql
SELECT DISTINCT r.catalog_number, r.title, r.release_date, 
       r.retail_price, comp.name as company_name
FROM records r
JOIN record_tracks rt ON r.id = rt.record_id
JOIN performances p ON rt.performance_id = p.id
JOIN companies comp ON r.company_id = comp.id
WHERE p.ensemble_id = ?
ORDER BY r.title
```

### 3. Лидеры продаж текущего года
```sql
SELECT r.catalog_number, r.title, r.sold_this_year, 
       comp.name as company_name, r.retail_price
FROM records r
JOIN companies comp ON r.company_id = comp.id
WHERE r.sold_this_year > 0
ORDER BY r.sold_this_year DESC
LIMIT 10
```

