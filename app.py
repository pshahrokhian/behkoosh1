from flask import Flask, render_template, redirect, url_for, session, request, flash
from werkzeug.security import check_password_hash
from db_utils import init_db, get_user_by_username
from blueprints.users import users_bp
from blueprints.equipments import equipments_bp

app = Flask(__name__)
app.secret_key = 'your-super-secret-key'

# ثبت بلوپرینت‌ها
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(equipments_bp, url_prefix='/equipments')


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['role'] = user['role']  # نقش کاربر (admin یا operator)
            return redirect(url_for('dashboard'))
        else:
            flash('نام کاربری یا رمز عبور نادرست است', 'danger')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    # داده‌های آماری فرضی
    stats = {
        'active_machines': 10,
        'electricity_today': '125 کیلووات',
        'total_hours': 52,
        'water_today': '600 لیتر'
    }

    return render_template('dashboard.html', username=session['username'], stats=stats)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/daily_report')
def daily_report():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('daily_report.html', active_page='daily_report')


@app.route('/monthly_report')
def monthly_report():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('monthly_report.html', active_page='monthly_report')


@app.route('/reports')
def reports():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('reports.html', active_page='reports')


# ----------------------------------------------------------------------

if __name__ == '__main__':
    # ✅ ساخت دیتابیس و جدول‌ها در context مناسب
    with app.app_context():
        init_db()

    app.run(debug=True)
