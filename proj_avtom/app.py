from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

DATABASE = 'music_store.db'

def get_db_connection():
    """Получение соединения с базой данных"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Главная страница"""
    conn = get_db_connection()
    
    # Получаем статистику
    stats = {
        'total_ensembles': conn.execute('SELECT COUNT(*) FROM ensembles').fetchone()[0],
        'total_compositions': conn.execute('SELECT COUNT(*) FROM compositions').fetchone()[0],
        'total_records': conn.execute('SELECT COUNT(*) FROM records').fetchone()[0],
        'total_musicians': conn.execute('SELECT COUNT(*) FROM musicians').fetchone()[0]
    }
    
    conn.close()
    return render_template('index.html', stats=stats)

@app.route('/compositions_count')
def compositions_count():
    """Функционал 1: Количество музыкальных произведений заданного ансамбля"""
    conn = get_db_connection()
    
    # Получаем список всех ансамблей
    ensembles = conn.execute('SELECT * FROM ensembles ORDER BY name').fetchall()
    
    ensemble_id = request.args.get('ensemble_id')
    compositions = []
    selected_ensemble = None
    
    if ensemble_id:
        # Получаем информацию об ансамбле
        selected_ensemble = conn.execute(
            'SELECT * FROM ensembles WHERE id = ?', (ensemble_id,)
        ).fetchone()
        
        # Получаем количество произведений ансамбля
        compositions = conn.execute('''
            SELECT DISTINCT c.title, c.genre, c.year_composed, m.name as composer_name
            FROM compositions c
            JOIN performances p ON c.id = p.composition_id
            JOIN ensemble_members em ON p.ensemble_id = em.ensemble_id
            LEFT JOIN musicians m ON c.composer_id = m.id
            WHERE p.ensemble_id = ?
            ORDER BY c.title
        ''', (ensemble_id,)).fetchall()
    
    conn.close()
    return render_template('compositions_count.html', 
                         ensembles=ensembles, 
                         compositions=compositions,
                         selected_ensemble=selected_ensemble)

@app.route('/ensemble_records')
def ensemble_records():
    """Функционал 2: Названия всех компакт-дисков заданного ансамбля"""
    conn = get_db_connection()
    
    # Получаем список всех ансамблей
    ensembles = conn.execute('SELECT * FROM ensembles ORDER BY name').fetchall()
    
    ensemble_id = request.args.get('ensemble_id')
    records = []
    selected_ensemble = None
    
    if ensemble_id:
        # Получаем информацию об ансамбле
        selected_ensemble = conn.execute(
            'SELECT * FROM ensembles WHERE id = ?', (ensemble_id,)
        ).fetchone()
        
        # Получаем все пластинки ансамбля
        records = conn.execute('''
            SELECT DISTINCT r.catalog_number, r.title, r.release_date, 
                   r.retail_price, comp.name as company_name
            FROM records r
            JOIN record_tracks rt ON r.id = rt.record_id
            JOIN performances p ON rt.performance_id = p.id
            JOIN companies comp ON r.company_id = comp.id
            WHERE p.ensemble_id = ?
            ORDER BY r.title
        ''', (ensemble_id,)).fetchall()
    
    conn.close()
    return render_template('ensemble_records.html', 
                         ensembles=ensembles, 
                         records=records,
                         selected_ensemble=selected_ensemble)

@app.route('/sales_leaders')
def sales_leaders():
    """Функционал 3: Лидеры продаж текущего года"""
    conn = get_db_connection()
    
    # Получаем текущий год
    current_year = datetime.now().year
    
    # Получаем лидеров продаж текущего года
    leaders = conn.execute('''
        SELECT r.catalog_number, r.title, r.sold_this_year, 
               comp.name as company_name, r.retail_price
        FROM records r
        JOIN companies comp ON r.company_id = comp.id
        WHERE r.sold_this_year > 0
        ORDER BY r.sold_this_year DESC
        LIMIT 10
    ''').fetchall()
    
    conn.close()
    return render_template('sales_leaders.html', leaders=leaders, current_year=current_year)

@app.route('/manage_records')
def manage_records():
    """Функционал 4: Управление данными о компакт-дисках"""
    conn = get_db_connection()
    
    # Получаем все пластинки с информацией о компаниях
    records = conn.execute('''
        SELECT r.*, comp.name as company_name
        FROM records r
        JOIN companies comp ON r.company_id = comp.id
        ORDER BY r.title
    ''').fetchall()
    
    # Получаем список компаний для формы
    companies = conn.execute('SELECT * FROM companies ORDER BY name').fetchall()
    
    conn.close()
    return render_template('manage_records.html', records=records, companies=companies)

@app.route('/add_record', methods=['POST'])
def add_record():
    """Добавление новой пластинки"""
    conn = get_db_connection()
    
    try:
        conn.execute('''
            INSERT INTO records (catalog_number, title, company_id, release_date, 
                               wholesale_price, retail_price, current_stock, 
                               sold_last_year, sold_this_year)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            request.form['catalog_number'],
            request.form['title'],
            request.form['company_id'],
            request.form['release_date'],
            float(request.form['wholesale_price']),
            float(request.form['retail_price']),
            int(request.form['current_stock']),
            int(request.form['sold_last_year']),
            int(request.form['sold_this_year'])
        ))
        conn.commit()
        flash('Пластинка успешно добавлена!', 'success')
    except Exception as e:
        flash(f'Ошибка при добавлении пластинки: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_records'))

@app.route('/edit_record/<int:record_id>')
def edit_record(record_id):
    """Страница редактирования пластинки"""
    conn = get_db_connection()
    
    record = conn.execute('SELECT * FROM records WHERE id = ?', (record_id,)).fetchone()
    companies = conn.execute('SELECT * FROM companies ORDER BY name').fetchall()
    
    conn.close()
    return render_template('edit_record.html', record=record, companies=companies)

@app.route('/update_record/<int:record_id>', methods=['POST'])
def update_record(record_id):
    """Обновление данных пластинки"""
    conn = get_db_connection()
    
    try:
        conn.execute('''
            UPDATE records 
            SET catalog_number = ?, title = ?, company_id = ?, release_date = ?,
                wholesale_price = ?, retail_price = ?, current_stock = ?,
                sold_last_year = ?, sold_this_year = ?
            WHERE id = ?
        ''', (
            request.form['catalog_number'],
            request.form['title'],
            request.form['company_id'],
            request.form['release_date'],
            float(request.form['wholesale_price']),
            float(request.form['retail_price']),
            int(request.form['current_stock']),
            int(request.form['sold_last_year']),
            int(request.form['sold_this_year']),
            record_id
        ))
        conn.commit()
        flash('Пластинка успешно обновлена!', 'success')
    except Exception as e:
        flash(f'Ошибка при обновлении пластинки: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_records'))

@app.route('/delete_record/<int:record_id>')
def delete_record(record_id):
    """Удаление пластинки"""
    conn = get_db_connection()
    
    try:
        conn.execute('DELETE FROM records WHERE id = ?', (record_id,))
        conn.commit()
        flash('Пластинка успешно удалена!', 'success')
    except Exception as e:
        flash(f'Ошибка при удалении пластинки: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_records'))

@app.route('/manage_ensembles')
def manage_ensembles():
    """Функционал 5: Управление данными об ансамблях"""
    conn = get_db_connection()
    
    ensembles = conn.execute('SELECT * FROM ensembles ORDER BY name').fetchall()
    
    conn.close()
    return render_template('manage_ensembles.html', ensembles=ensembles)

@app.route('/add_ensemble', methods=['POST'])
def add_ensemble():
    """Добавление нового ансамбля"""
    conn = get_db_connection()
    
    try:
        conn.execute('''
            INSERT INTO ensembles (name, type, founded_year, country, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            request.form['name'],
            request.form['type'],
            request.form['founded_year'] if request.form['founded_year'] else None,
            request.form['country'],
            request.form['description']
        ))
        conn.commit()
        flash('Ансамбль успешно добавлен!', 'success')
    except Exception as e:
        flash(f'Ошибка при добавлении ансамбля: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_ensembles'))

@app.route('/edit_ensemble/<int:ensemble_id>')
def edit_ensemble(ensemble_id):
    """Страница редактирования ансамбля"""
    conn = get_db_connection()
    
    ensemble = conn.execute('SELECT * FROM ensembles WHERE id = ?', (ensemble_id,)).fetchone()
    
    conn.close()
    return render_template('edit_ensemble.html', ensemble=ensemble)

@app.route('/update_ensemble/<int:ensemble_id>', methods=['POST'])
def update_ensemble(ensemble_id):
    """Обновление данных ансамбля"""
    conn = get_db_connection()
    
    try:
        conn.execute('''
            UPDATE ensembles 
            SET name = ?, type = ?, founded_year = ?, country = ?, description = ?
            WHERE id = ?
        ''', (
            request.form['name'],
            request.form['type'],
            request.form['founded_year'] if request.form['founded_year'] else None,
            request.form['country'],
            request.form['description'],
            ensemble_id
        ))
        conn.commit()
        flash('Ансамбль успешно обновлен!', 'success')
    except Exception as e:
        flash(f'Ошибка при обновлении ансамбля: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_ensembles'))

@app.route('/delete_ensemble/<int:ensemble_id>')
def delete_ensemble(ensemble_id):
    """Удаление ансамбля"""
    conn = get_db_connection()
    
    try:
        conn.execute('DELETE FROM ensembles WHERE id = ?', (ensemble_id,))
        conn.commit()
        flash('Ансамбль успешно удален!', 'success')
    except Exception as e:
        flash(f'Ошибка при удалении ансамбля: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_ensembles'))

if __name__ == '__main__':
    # Инициализируем базу данных если её нет
    if not os.path.exists(DATABASE):
        from database import init_database
        init_database()
    
    app.run(debug=True)
