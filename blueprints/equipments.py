from flask import Blueprint, render_template, request, redirect, url_for, flash
from db_utils import get_db

equipments_bp = Blueprint('equipments', __name__, template_folder='templates')

@equipments_bp.route('/manage', methods=['GET', 'POST'])
def manage_equipments():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        equip_id = request.form.get('id')
        name = request.form['name']
        type_ = request.form.get('type')
        location = request.form.get('location')
        upstream_equipment = request.form.get('upstream_equipment')
        responsible_unit = request.form.get('responsible_unit')
        install_date = request.form.get('install_date')
        active = 1 if request.form.get('active') == 'on' else 0

        # محاسبه خودکار کد تجهیز فقط برای اضافه کردن
        if not equip_id:
            max_code = cursor.execute('SELECT MAX(code) FROM equipments').fetchone()[0]
            new_code = (max_code or 0) + 1
        else:
            new_code = None

        if equip_id:  # ویرایش
            cursor.execute('''
                UPDATE equipments SET
                name=?, type=?, location=?, upstream_equipment=?, responsible_unit=?, install_date=?, active=?
                WHERE id=?
            ''', (name, type_, location, upstream_equipment, responsible_unit, install_date, active, equip_id))
            flash('Equipment updated successfully.')
        else:  # اضافه کردن
            cursor.execute('''
                INSERT INTO equipments (code, name, type, location, upstream_equipment, responsible_unit, install_date, active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (new_code, name, type_, location, upstream_equipment, responsible_unit, install_date, active))
            flash('Equipment added successfully.')

        db.commit()
        return redirect(url_for('equipments.manage_equipments'))

    equipments = cursor.execute('SELECT * FROM equipments').fetchall()
    return render_template('manage_equipments.html', equipments=equipments)
