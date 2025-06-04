from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

users_bp = Blueprint('users', __name__, url_prefix='/users')


def get_db():
    return sqlite3.connect('factory.db')

# صفحه مدیریت کاربران
@users_bp.route('/', methods=['GET', 'POST'])
def manage_users():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user_code = request.form.get('user_code')
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', '')
        created_at = request.form.get('created_at') or datetime.now().strftime('%Y/%m/%d')

        if not full_name or not username:
            flash('نام کامل و نام کاربری الزامی است.', 'error')
        else:
            if user_id:  # ویرایش
                if password:
                    cursor.execute('''
                        UPDATE users SET full_name=?, username=?, password=?, role=?
                        WHERE id=?
                    ''', (full_name, username, password, role, user_id))
                else:
                    cursor.execute('''
                        UPDATE users SET full_name=?, username=?, role=?
                        WHERE id=?
                    ''', (full_name, username, role, user_id))
                flash('اطلاعات کاربر با موفقیت ویرایش شد.', 'success')
            else:  # افزودن
                cursor.execute('''
                    INSERT INTO users (user_code, full_name, username, password, role, created_at, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, 1)
                ''', (user_code, full_name, username, password, role, created_at))
                flash('کاربر جدید با موفقیت افزوده شد.', 'success')

        conn.commit()

    # خواندن لیست کاربران برای نمایش
    cursor.execute('SELECT id, user_code, full_name, username, role, created_at, is_active FROM users ORDER BY id DESC')
    users = [dict(id=row[0], user_code=row[1], full_name=row[2], username=row[3], role=row[4], created_at=row[5], active=bool(row[6])) for row in cursor.fetchall()]

    conn.close()
    return render_template('manage_users.html', users=users)


# تغییر فعال / غیرفعال بودن کاربر
@users_bp.route('/toggle_active/<int:user_id>', methods=['POST'])
def toggle_user_active(user_id):
    active = request.form.get('active') == '1'
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET is_active=? WHERE id=?', (1 if active else 0, user_id))
    conn.commit()
    conn.close()
    flash('وضعیت فعال‌بودن کاربر تغییر یافت.', 'success')
    return redirect(url_for('users.manage_users'))
