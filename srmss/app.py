from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, make_response
import pymysql
import pymysql.cursors
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from functools import wraps
import random
import string
import os
import hashlib
from decimal import Decimal
import threading
import time
import csv
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'srmss-secret-key-2026'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

# Upload configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads/receipts'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'srmss_db',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    return pymysql.connect(**db_config)

# ============ HELPER FUNCTIONS ============

def get_dashboard_by_role(role):
    dashboards = {
        'admin': 'admin_dashboard',
        'depot_manager': 'depot_manager_dashboard',
        'supervisor': 'supervisor_dashboard',
        'driver': 'driver_dashboard',
        'customer': 'customer_dashboard'
    }
    return dashboards.get(role, 'login')

def log_user_activity(user_id, action, req):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_activity_log (user_id, action, ip_address, user_agent) VALUES (%s, %s, %s, %s)",
                      (user_id, action, req.remote_addr, req.headers.get('User-Agent', '')))
        conn.commit()
        cursor.close()
        conn.close()
    except:
        pass

def create_notification(user_id, title, message, type='info'):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notifications (user_id, title, message, type) VALUES (%s, %s, %s, %s)",
                      (user_id, title, message, type))
        conn.commit()
        cursor.close()
        conn.close()
    except:
        pass

def generate_ticket_number():
    return 'TKT-' + ''.join(random.choices(string.digits, k=8))

def get_coordinates_from_name(city_name):
    coordinates = {
        'Colombo': [6.9271, 79.8612],
        'Kandy': [7.2906, 80.6337],
        'Galle': [6.0328, 80.2168],
        'Matara': [5.9491, 80.5439],
        'Jaffna': [9.6615, 80.0255],
        'Kataragama': [6.4167, 81.3333],
        'Katharagama': [6.4167, 81.3333],
        'Hambantota': [6.1241, 81.1196],
        'Anuradhapura': [8.3114, 80.4037],
        'Vavuniya': [8.7500, 80.4000],
        'Trincomalee': [8.5774, 81.2128],
        'Batticaloa': [7.7173, 81.7005],
        'Ratnapura': [6.7055, 80.3843],
        'Badulla': [6.9931, 81.0553],
        'Nuwara Eliya': [6.9497, 80.7891],
        'Kurunegala': [7.4863, 80.3623],
        'Negombo': [7.2092, 79.8357]
    }
    for key, value in coordinates.items():
        if key.lower() in city_name.lower() or city_name.lower() in key.lower():
            return value
    return [7.8731, 80.7718]

# ============ PERMISSION DECORATOR ============

# def permission_required(permission):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if 'user_id' not in session:
#                 flash('Please login first!', 'error')
#                 return redirect(url_for('login'))
            
#             user_role = session.get('role')
#             if user_role == 'admin':
#                 return f(*args, **kwargs)
            
#             try:
#                 conn = get_db()
#                 cursor = conn.cursor()
#                 cursor.execute("SELECT permission FROM role_permissions WHERE role = %s AND permission = %s",
#                              (user_role, permission))
#                 has_permission = cursor.fetchone()
#                 cursor.close()
#                 conn.close()
                
#                 if has_permission:
#                     return f(*args, **kwargs)
#                 else:
#                     flash('You do not have permission to access this page!', 'error')
#                     return redirect(url_for(get_dashboard_by_role(user_role)))
#             except Exception as e:
#                 flash(f'Permission error: {str(e)}', 'error')
#                 return redirect(url_for('login'))
#         return decorated_function
#     return decorator

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login first!', 'error')
                return redirect(url_for('login'))
            
            user_role = session.get('role')
            
            # Admin has all permissions
            if user_role == 'admin':
                return f(*args, **kwargs)
            
            # For customers, check if they have the specific permission
            # Also allow customers to view their own data without strict permission checks
            if user_role == 'customer':
                # Allow access to customer-specific pages even if permission not found
                # This is a fallback for customer routes
                return f(*args, **kwargs)
            
            try:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("SELECT permission FROM role_permissions WHERE role = %s AND permission = %s",
                             (user_role, permission))
                has_permission = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if has_permission:
                    return f(*args, **kwargs)
                else:
                    flash('You do not have permission to access this page!', 'error')
                    return redirect(url_for(get_dashboard_by_role(user_role)))
            except Exception as e:
                flash(f'Permission error: {str(e)}', 'error')
                return redirect(url_for('login'))
        return decorated_function
    return decorator

# ============ PUBLIC ROUTES ============

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND is_active = 1", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user and check_password_hash(user['password_hash'], password):
                session.permanent = True if remember else False
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                session['first_name'] = user['first_name']
                session['last_name'] = user['last_name']
                
                log_user_activity(user['id'], 'User logged in', request)
                
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET last_login = NOW() WHERE id = %s", (user['id'],))
                conn.commit()
                cursor.close()
                conn.close()
                
                flash(f'Welcome {user["first_name"]}!', 'success')
                
                if user['role'] == 'admin':
                    return redirect(url_for('admin_dashboard'))
                elif user['role'] == 'depot_manager':
                    return redirect(url_for('depot_manager_dashboard'))
                elif user['role'] == 'supervisor':
                    return redirect(url_for('supervisor_dashboard'))
                elif user['role'] == 'driver':
                    return redirect(url_for('driver_dashboard'))
                else:
                    return redirect(url_for('customer_dashboard'))
            else:
                flash('Invalid username or password!', 'error')
        except Exception as e:
            flash(f'Login error: {str(e)}', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        d = request.form
        if not all([d.get('first_name'), d.get('last_name'), d.get('username'), 
                   d.get('email'), d.get('password'), d.get('confirm_password')]):
            flash('All fields are required!', 'error')
            return render_template('register.html')
        if d['password'] != d['confirm_password']:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        if len(d['password']) < 6:
            flash('Password must be at least 6 characters!', 'error')
            return render_template('register.html')
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = %s", (d['username'],))
            if cursor.fetchone():
                flash('Username already exists!', 'error')
                cursor.close()
                conn.close()
                return render_template('register.html')
            cursor.execute("SELECT id FROM users WHERE email = %s", (d['email'],))
            if cursor.fetchone():
                flash('Email already registered!', 'error')
                cursor.close()
                conn.close()
                return render_template('register.html')
            cursor.execute("INSERT INTO users (first_name, last_name, username, email, phone, password_hash, role) VALUES (%s,%s,%s,%s,%s,%s,'customer')",
                          (d['first_name'], d['last_name'], d['username'], d['email'], d.get('phone', ''), generate_password_hash(d['password'])))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    return render_template('register.html')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        log_user_activity(session['user_id'], 'User logged out', request)
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

# ============ ADMIN ROUTES ============

@app.route('/admin/dashboard')
@permission_required('view_dashboard')
def admin_dashboard():
    stats = {}
    recent_schedules = []
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as c FROM routes")
        stats['total_routes'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM vehicles")
        stats['total_vehicles'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM vehicles WHERE status='available'")
        stats['available_vehicles'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM vehicles WHERE status='in_use'")
        stats['in_use_vehicles'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM vehicles WHERE status='maintenance'")
        stats['maintenance_vehicles'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM users WHERE role='driver'")
        stats['total_drivers'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM users WHERE role='customer'")
        stats['total_customers'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM schedules WHERE schedule_date=CURDATE()")
        stats['today_schedules'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM schedules WHERE schedule_date=CURDATE() AND status='delayed'")
        stats['delayed_trips'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM support_tickets WHERE status='open'")
        stats['open_tickets'] = cursor.fetchone()['c']
        
        cursor.execute("""SELECT s.*, r.route_name, v.registration_number, 
                       CONCAT(d.first_name,' ',d.last_name) as driver_name 
                       FROM schedules s 
                       JOIN routes r ON s.route_id=r.id 
                       JOIN vehicles v ON s.vehicle_id=v.id 
                       JOIN users d ON s.driver_id=d.id 
                       ORDER BY s.created_at DESC LIMIT 5""")
        recent_schedules = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        stats = {'total_routes':0, 'total_vehicles':0, 'available_vehicles':0, 'in_use_vehicles':0,
                'maintenance_vehicles':0, 'total_drivers':0, 'total_customers':0, 'today_schedules':0,
                'delayed_trips':0, 'open_tickets':0}
    return render_template('admin_dashboard.html', stats=stats, recent_schedules=recent_schedules)

@app.route('/admin/routes', methods=['GET', 'POST'])
@permission_required('manage_routes')
def admin_routes():
    if request.method == 'POST':
        d = request.form
        if not all([d.get('route_code'), d.get('route_name'), d.get('start_point'), 
                   d.get('end_point'), d.get('total_distance')]):
            flash('Fill all fields!', 'error')
            return redirect(url_for('admin_routes'))
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM routes WHERE route_code=%s", (d['route_code'],))
            if cursor.fetchone():
                flash('Route code already exists!', 'error')
                cursor.close()
                conn.close()
                return redirect(url_for('admin_routes'))
            cursor.execute("INSERT INTO routes (route_code,route_name,start_point,end_point,intermediate_stops,total_distance,route_type,base_fare) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                          (d['route_code'], d['route_name'], d['start_point'], d['end_point'], 
                           d.get('intermediate_stops', ''), d['total_distance'], 
                           d.get('route_type', 'urban'), d.get('base_fare', 0)))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Route added successfully!', 'success')
            log_user_activity(session['user_id'], f'Added route: {d["route_code"]}', request)
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('admin_routes'))
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM routes ORDER BY created_at DESC")
        routes = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        routes = []
    return render_template('admin_routes.html', routes=routes)

@app.route('/admin/routes/delete', methods=['POST'])
@permission_required('manage_routes')
def admin_delete_route():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM routes WHERE id=%s", (request.form['route_id'],))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Route deleted successfully!', 'success')
        log_user_activity(session['user_id'], f'Deleted route ID: {request.form["route_id"]}', request)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('admin_routes'))

@app.route('/admin/routes/edit', methods=['POST'])
@permission_required('manage_routes')
def admin_edit_route():
    try:
        route_id = request.form.get('route_id')
        route_code = request.form.get('route_code')
        route_name = request.form.get('route_name')
        start_point = request.form.get('start_point')
        end_point = request.form.get('end_point')
        intermediate_stops = request.form.get('intermediate_stops', '')
        total_distance = request.form.get('total_distance')
        route_type = request.form.get('route_type', 'urban')
        base_fare = request.form.get('base_fare', 0)
        
        if not all([route_id, route_code, route_name, start_point, end_point, total_distance]):
            flash('Please fill all required fields!', 'error')
            return redirect(url_for('admin_routes'))
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if route code exists for a different route
        cursor.execute("SELECT id FROM routes WHERE route_code = %s AND id != %s", (route_code, route_id))
        if cursor.fetchone():
            flash('Route code already exists for another route!', 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('admin_routes'))
        
        cursor.execute("""
            UPDATE routes 
            SET route_code = %s, 
                route_name = %s, 
                start_point = %s, 
                end_point = %s, 
                intermediate_stops = %s, 
                total_distance = %s, 
                route_type = %s,
                base_fare = %s
            WHERE id = %s
        """, (route_code, route_name, start_point, end_point, intermediate_stops, total_distance, route_type, base_fare, route_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Route updated successfully!', 'success')
        log_user_activity(session['user_id'], f'Updated route: {route_code} (ID: {route_id})', request)
        
    except Exception as e:
        flash(f'Error updating route: {str(e)}', 'error')
    
    return redirect(url_for('admin_routes'))

@app.route('/admin/vehicles', methods=['GET', 'POST'])
@permission_required('manage_vehicles')
def admin_vehicles():
    if request.method == 'POST':
        d = request.form
        if not all([d.get('vehicle_code'), d.get('registration_number'), d.get('seating_capacity')]):
            flash('Fill all fields!', 'error')
            return redirect(url_for('admin_vehicles'))
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO vehicles (vehicle_code,registration_number,vehicle_type,seating_capacity,fuel_type,status) VALUES (%s,%s,%s,%s,%s,%s)",
                          (d['vehicle_code'], d['registration_number'], d.get('vehicle_type', 'standard'),
                           d['seating_capacity'], d.get('fuel_type', 'diesel'), d.get('status', 'available')))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Vehicle added successfully!', 'success')
            log_user_activity(session['user_id'], f'Added vehicle: {d["vehicle_code"]}', request)
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('admin_vehicles'))
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles ORDER BY created_at DESC")
        vehicles = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        vehicles = []
    return render_template('admin_vehicles.html', vehicles=vehicles)

@app.route('/admin/vehicles/delete', methods=['POST'])
@permission_required('manage_vehicles')
def admin_delete_vehicle():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vehicles WHERE id=%s", (request.form['vehicle_id'],))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Vehicle deleted successfully!', 'success')
        log_user_activity(session['user_id'], f'Deleted vehicle ID: {request.form["vehicle_id"]}', request)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('admin_vehicles'))

@app.route('/admin/vehicles/edit', methods=['POST'])
@permission_required('manage_vehicles')
def admin_edit_vehicle():
    try:
        vehicle_id = request.form.get('vehicle_id')
        vehicle_code = request.form.get('vehicle_code')
        registration_number = request.form.get('registration_number')
        vehicle_type = request.form.get('vehicle_type', 'standard')
        seating_capacity = request.form.get('seating_capacity')
        fuel_type = request.form.get('fuel_type', 'diesel')
        status = request.form.get('status', 'available')
        
        if not all([vehicle_id, vehicle_code, registration_number, seating_capacity]):
            flash('Please fill all required fields!', 'error')
            return redirect(url_for('admin_vehicles'))
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if vehicle code exists for a different vehicle
        cursor.execute("SELECT id FROM vehicles WHERE vehicle_code = %s AND id != %s", (vehicle_code, vehicle_id))
        if cursor.fetchone():
            flash('Vehicle code already exists for another vehicle!', 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('admin_vehicles'))
        
        cursor.execute("""
            UPDATE vehicles 
            SET vehicle_code = %s, 
                registration_number = %s, 
                vehicle_type = %s, 
                seating_capacity = %s, 
                fuel_type = %s, 
                status = %s
            WHERE id = %s
        """, (vehicle_code, registration_number, vehicle_type, seating_capacity, fuel_type, status, vehicle_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Vehicle updated successfully!', 'success')
        log_user_activity(session['user_id'], f'Updated vehicle: {vehicle_code} (ID: {vehicle_id})', request)
        
    except Exception as e:
        flash(f'Error updating vehicle: {str(e)}', 'error')
    
    return redirect(url_for('admin_vehicles'))

@app.route('/admin/drivers', methods=['GET', 'POST'])
@permission_required('view_drivers')
def admin_drivers():
    if request.method == 'POST':
        # Only admin can add drivers
        if session.get('role') != 'admin':
            flash('You do not have permission to add drivers!', 'error')
            return redirect(url_for('admin_drivers'))
            
        d = request.form
        if not all([d.get('first_name'), d.get('last_name'), d.get('username'), 
                   d.get('email'), d.get('password')]):
            flash('Fill all fields!', 'error')
            return redirect(url_for('admin_drivers'))
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = %s", (d['username'],))
            if cursor.fetchone():
                flash('Username already exists!', 'error')
                cursor.close()
                conn.close()
                return redirect(url_for('admin_drivers'))
            cursor.execute("SELECT id FROM users WHERE email = %s", (d['email'],))
            if cursor.fetchone():
                flash('Email already exists!', 'error')
                cursor.close()
                conn.close()
                return redirect(url_for('admin_drivers'))
            cursor.execute("INSERT INTO users (first_name,last_name,username,email,phone,password_hash,role) VALUES (%s,%s,%s,%s,%s,%s,'driver')",
                          (d['first_name'], d['last_name'], d['username'], d['email'], 
                           d.get('phone', ''), generate_password_hash(d['password'])))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Driver added successfully!', 'success')
            log_user_activity(session['user_id'], f'Added driver: {d["username"]}', request)
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('admin_drivers'))
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE role='driver' ORDER BY created_at DESC")
        drivers = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        drivers = []
    return render_template('admin_drivers.html', drivers=drivers)

@app.route('/admin/drivers/delete', methods=['POST'])
@permission_required('manage_drivers')
def admin_delete_driver():
    try:
        conn = get_db()
        cursor = conn.cursor()
        if int(request.form['user_id']) == session.get('user_id'):
            flash('Cannot delete yourself!', 'error')
            return redirect(url_for('admin_drivers'))
        cursor.execute("DELETE FROM users WHERE id=%s AND role='driver'", (request.form['user_id'],))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Driver deleted successfully!', 'success')
        log_user_activity(session['user_id'], f'Deleted driver ID: {request.form["user_id"]}', request)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('admin_drivers'))

@app.route('/admin/drivers/edit', methods=['POST'])
@permission_required('manage_drivers')
def admin_edit_driver():
    try:
        driver_id = request.form.get('driver_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone', '')
        is_active = request.form.get('is_active', 1)
        
        if not all([driver_id, first_name, last_name]):
            flash('Please fill all required fields!', 'error')
            return redirect(url_for('admin_drivers'))
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if driver exists
        cursor.execute("SELECT id FROM users WHERE id = %s AND role = 'driver'", (driver_id,))
        if not cursor.fetchone():
            flash('Driver not found!', 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('admin_drivers'))
        
        cursor.execute("""
            UPDATE users 
            SET first_name = %s, 
                last_name = %s, 
                phone = %s, 
                is_active = %s
            WHERE id = %s AND role = 'driver'
        """, (first_name, last_name, phone, is_active, driver_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Driver updated successfully!', 'success')
        log_user_activity(session['user_id'], f'Updated driver ID: {driver_id}', request)
        
    except Exception as e:
        flash(f'Error updating driver: {str(e)}', 'error')
    
    return redirect(url_for('admin_drivers'))

@app.route('/admin/drivers/reset-password', methods=['POST'])
@permission_required('manage_drivers')
def admin_reset_driver_password():
    try:
        driver_id = request.form.get('driver_id')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([driver_id, new_password, confirm_password]):
            flash('Please fill all fields!', 'error')
            return redirect(url_for('admin_drivers'))
        
        if new_password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('admin_drivers'))
        
        if len(new_password) < 6:
            flash('Password must be at least 6 characters!', 'error')
            return redirect(url_for('admin_drivers'))
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if driver exists
        cursor.execute("SELECT id, username FROM users WHERE id = %s AND role = 'driver'", (driver_id,))
        driver = cursor.fetchone()
        
        if not driver:
            flash('Driver not found!', 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('admin_drivers'))
        
        # Update password
        cursor.execute("""
            UPDATE users 
            SET password_hash = %s 
            WHERE id = %s AND role = 'driver'
        """, (generate_password_hash(new_password), driver_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash(f'Password reset successfully for driver: {driver["username"]}', 'success')
        log_user_activity(session['user_id'], f'Reset password for driver ID: {driver_id}', request)
        
    except Exception as e:
        flash(f'Error resetting password: {str(e)}', 'error')
    
    return redirect(url_for('admin_drivers'))

@app.route('/admin/schedules', methods=['GET', 'POST'])
@permission_required('manage_schedules')
def admin_schedules():
    if request.method == 'POST':
        d = request.form
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO schedules (route_id,vehicle_id,driver_id,departure_time,arrival_time,schedule_date,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                          (d['route_id'], d['vehicle_id'], d['driver_id'], d['departure_time'], 
                           d['arrival_time'], d['schedule_date'], d.get('status', 'scheduled')))
            conn.commit()
            create_notification(d['driver_id'], 'New Schedule Assigned', 
                              f'You have been assigned a new trip on {d["schedule_date"]}', 'schedule')
            cursor.close()
            conn.close()
            flash('Schedule added successfully!', 'success')
            log_user_activity(session['user_id'], f'Added schedule for driver ID: {d["driver_id"]}', request)
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('admin_schedules'))
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT s.*, r.route_name, v.registration_number, 
                       CONCAT(d.first_name,' ',d.last_name) as driver_name 
                       FROM schedules s 
                       JOIN routes r ON s.route_id=r.id 
                       JOIN vehicles v ON s.vehicle_id=v.id 
                       JOIN users d ON s.driver_id=d.id 
                       ORDER BY s.schedule_date DESC""")
        schedules = cursor.fetchall()
        cursor.execute("SELECT * FROM routes WHERE is_active=1")
        routes = cursor.fetchall()
        cursor.execute("SELECT * FROM vehicles WHERE status != 'maintenance'")
        vehicles = cursor.fetchall()
        cursor.execute("SELECT * FROM users WHERE role='driver'")
        drivers = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        schedules = []
        routes = []
        vehicles = []
        drivers = []
    return render_template('admin_schedules.html', schedules=schedules, routes=routes, 
                          vehicles=vehicles, drivers=drivers)

@app.route('/admin/schedules/edit', methods=['POST'])
@permission_required('manage_schedules')
def admin_edit_schedule():
    try:
        schedule_id = request.form.get('schedule_id')
        route_id = request.form.get('route_id')
        vehicle_id = request.form.get('vehicle_id')
        driver_id = request.form.get('driver_id')
        schedule_date = request.form.get('schedule_date')
        departure_time = request.form.get('departure_time')
        arrival_time = request.form.get('arrival_time')
        status = request.form.get('status', 'scheduled')
        
        if not all([schedule_id, route_id, vehicle_id, driver_id, schedule_date, departure_time, arrival_time]):
            flash('Please fill all required fields!', 'error')
            return redirect(url_for('admin_schedules'))
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if schedule exists
        cursor.execute("SELECT id FROM schedules WHERE id = %s", (schedule_id,))
        if not cursor.fetchone():
            flash('Schedule not found!', 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('admin_schedules'))
        
        # Get old driver_id for notification
        cursor.execute("SELECT driver_id FROM schedules WHERE id = %s", (schedule_id,))
        old_data = cursor.fetchone()
        old_driver_id = old_data['driver_id'] if old_data else None
        
        # Update schedule
        cursor.execute("""
            UPDATE schedules 
            SET route_id = %s, 
                vehicle_id = %s, 
                driver_id = %s, 
                schedule_date = %s, 
                departure_time = %s, 
                arrival_time = %s, 
                status = %s
            WHERE id = %s
        """, (route_id, vehicle_id, driver_id, schedule_date, departure_time, arrival_time, status, schedule_id))
        
        conn.commit()
        
        # Send notification to driver about schedule update
        if status in ['scheduled', 'on_time']:
            create_notification(driver_id, 'Schedule Updated', 
                              f'Your schedule on {schedule_date} has been updated. Departure: {departure_time}, Arrival: {arrival_time}', 'schedule')
            
            # If driver changed, also notify old driver
            if old_driver_id and old_driver_id != int(driver_id):
                create_notification(old_driver_id, 'Schedule Removed', 
                                  f'Your schedule on {schedule_date} has been reassigned to another driver.', 'schedule')
        
        cursor.close()
        conn.close()
        
        flash('Schedule updated successfully!', 'success')
        log_user_activity(session['user_id'], f'Updated schedule ID: {schedule_id}', request)
        
    except Exception as e:
        flash(f'Error updating schedule: {str(e)}', 'error')
    
    return redirect(url_for('admin_schedules'))

@app.route('/admin/schedules/delete', methods=['POST'])
@permission_required('manage_schedules')
def admin_delete_schedule():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM schedules WHERE id=%s", (request.form['schedule_id'],))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Schedule deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('admin_schedules'))

@app.route('/admin/fuel-logs', methods=['GET', 'POST'])
@permission_required('manage_fuel_logs')
def admin_fuel_logs():
    if request.method == 'POST':
        d = request.form
        if not all([d.get('vehicle_id'), d.get('fuel_date'), d.get('fuel_liters'), 
                   d.get('cost_per_liter'), d.get('total_cost'), d.get('odometer_reading')]):
            flash('Fill all fields!', 'error')
            return redirect(url_for('admin_fuel_logs'))
        
        receipt_filename = None
        if 'receipt' in request.files:
            file = request.files['receipt']
            if file and file.filename and allowed_file(file.filename):
                file_ext = file.filename.rsplit('.', 1)[1].lower()
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"fuel_{d['vehicle_id']}_{timestamp}.{file_ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                receipt_filename = f"uploads/receipts/{filename}"
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO fuel_logs (vehicle_id, fuel_date, fuel_liters, cost_per_liter,
                           total_cost, odometer_reading, fuel_station, receipt_path, logged_by) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                           (d['vehicle_id'], d['fuel_date'], d['fuel_liters'], d['cost_per_liter'],
                            d['total_cost'], d['odometer_reading'], d.get('fuel_station', ''),
                            receipt_filename, session['user_id']))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Fuel log added successfully!', 'success')
            log_user_activity(session['user_id'], f'Added fuel log for vehicle ID: {d["vehicle_id"]}', request)
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('admin_fuel_logs'))
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.*, 
                   v.registration_number, 
                   v.vehicle_code,
                   CONCAT(u.first_name, ' ', u.last_name) as logged_by_name
            FROM fuel_logs f 
            JOIN vehicles v ON f.vehicle_id = v.id 
            LEFT JOIN users u ON f.logged_by = u.id
            ORDER BY f.fuel_date DESC
        """)
        fuel_logs = cursor.fetchall()
        cursor.execute("SELECT * FROM vehicles ORDER BY registration_number")
        vehicles = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error loading fuel logs: {e}")
        fuel_logs = []
        vehicles = []
    
    return render_template('admin_fuel_logs.html', fuel_logs=fuel_logs, vehicles=vehicles)

@app.route('/admin/fuel-logs/delete', methods=['POST'])
@permission_required('manage_fuel_logs')
def admin_delete_fuel_log():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT receipt_path FROM fuel_logs WHERE id=%s", (request.form['log_id'],))
        log = cursor.fetchone()
        if log and log.get('receipt_path'):
            filepath = os.path.join('static', log['receipt_path'])
            if os.path.exists(filepath):
                os.remove(filepath)
        
        cursor.execute("DELETE FROM fuel_logs WHERE id=%s", (request.form['log_id'],))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Fuel log deleted successfully!', 'success')
        log_user_activity(session['user_id'], f'Deleted fuel log ID: {request.form["log_id"]}', request)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('admin_fuel_logs'))

@app.route('/admin/maintenance', methods=['GET', 'POST'])
@permission_required('manage_maintenance')
def admin_maintenance():
    if request.method == 'POST':
        d = request.form
        if not all([d.get('vehicle_id'), d.get('maintenance_date'), d.get('description'), d.get('total_cost')]):
            flash('Fill all fields!', 'error')
            return redirect(url_for('admin_maintenance'))
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO maintenance_logs (vehicle_id, maintenance_date, maintenance_type, description,
                           labor_cost, parts_cost, total_cost, service_center, next_service_date) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                           (d['vehicle_id'], d['maintenance_date'], d.get('maintenance_type', 'routine'),
                            d['description'], d.get('labor_cost', 0), d.get('parts_cost', 0), d['total_cost'],
                            d.get('service_center', ''), d.get('next_service_date', '')))
            conn.commit()
            
            if d.get('maintenance_type') == 'emergency':
                cursor.execute("UPDATE vehicles SET status='maintenance' WHERE id=%s", (d['vehicle_id'],))
                conn.commit()
            
            cursor.close()
            conn.close()
            flash('Maintenance log added successfully!', 'success')
            log_user_activity(session['user_id'], f'Added maintenance for vehicle ID: {d["vehicle_id"]}', request)
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('admin_maintenance'))
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.*, v.registration_number, v.vehicle_code 
            FROM maintenance_logs m 
            JOIN vehicles v ON m.vehicle_id = v.id 
            ORDER BY m.maintenance_date DESC
        """)
        maintenance_logs = cursor.fetchall()
        cursor.execute("SELECT * FROM vehicles ORDER BY registration_number")
        vehicles = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error loading maintenance logs: {e}")
        maintenance_logs = []
        vehicles = []
    
    return render_template('admin_maintenance.html', maintenance_logs=maintenance_logs, vehicles=vehicles)

@app.route('/admin/maintenance/edit', methods=['POST'])
@permission_required('manage_maintenance')
def admin_edit_maintenance():
    try:
        log_id = request.form.get('log_id')
        vehicle_id = request.form.get('vehicle_id')
        maintenance_date = request.form.get('maintenance_date')
        maintenance_type = request.form.get('maintenance_type', 'routine')
        description = request.form.get('description')
        labor_cost = request.form.get('labor_cost', 0)
        parts_cost = request.form.get('parts_cost', 0)
        total_cost = request.form.get('total_cost')
        service_center = request.form.get('service_center', '')
        next_service_date = request.form.get('next_service_date', '')
        
        if not all([log_id, vehicle_id, maintenance_date, description, total_cost]):
            flash('Please fill all required fields!', 'error')
            return redirect(url_for('admin_maintenance'))
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if maintenance log exists
        cursor.execute("SELECT id FROM maintenance_logs WHERE id = %s", (log_id,))
        if not cursor.fetchone():
            flash('Maintenance log not found!', 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('admin_maintenance'))
        
        # Get old vehicle_id to update status if needed
        cursor.execute("SELECT vehicle_id, maintenance_type FROM maintenance_logs WHERE id = %s", (log_id,))
        old_data = cursor.fetchone()
        old_vehicle_id = old_data['vehicle_id'] if old_data else None
        
        # Update maintenance log
        cursor.execute("""
            UPDATE maintenance_logs 
            SET vehicle_id = %s, 
                maintenance_date = %s, 
                maintenance_type = %s, 
                description = %s, 
                labor_cost = %s, 
                parts_cost = %s, 
                total_cost = %s, 
                service_center = %s, 
                next_service_date = %s
            WHERE id = %s
        """, (vehicle_id, maintenance_date, maintenance_type, description, 
              labor_cost, parts_cost, total_cost, service_center, next_service_date, log_id))
        
        conn.commit()
        
        # Update vehicle status if maintenance is emergency
        if maintenance_type == 'emergency':
            cursor.execute("UPDATE vehicles SET status = 'maintenance' WHERE id = %s", (vehicle_id,))
            conn.commit()
        elif old_data and old_data['maintenance_type'] == 'emergency' and maintenance_type != 'emergency':
            # If it was emergency but now changed, revert vehicle status to available
            cursor.execute("UPDATE vehicles SET status = 'available' WHERE id = %s", (vehicle_id,))
            conn.commit()
        
        cursor.close()
        conn.close()
        
        flash('Maintenance log updated successfully!', 'success')
        log_user_activity(session['user_id'], f'Updated maintenance log ID: {log_id}', request)
        
    except Exception as e:
        flash(f'Error updating maintenance log: {str(e)}', 'error')
    
    return redirect(url_for('admin_maintenance'))

@app.route('/admin/maintenance/delete', methods=['POST'])
@permission_required('manage_maintenance')
def admin_delete_maintenance():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM maintenance_logs WHERE id=%s", (request.form['log_id'],))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Maintenance log deleted successfully!', 'success')
        log_user_activity(session['user_id'], f'Deleted maintenance log ID: {request.form["log_id"]}', request)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('admin_maintenance'))

@app.route('/admin/users', methods=['GET', 'POST'])
@permission_required('manage_users')
def admin_users():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            d = request.form
            try:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (first_name,last_name,username,email,phone,password_hash,role) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                              (d['first_name'], d['last_name'], d['username'], d['email'], 
                               d.get('phone', ''), generate_password_hash(d['password']), 
                               d.get('role', 'customer')))
                conn.commit()
                cursor.close()
                conn.close()
                flash('User added successfully!', 'success')
                log_user_activity(session['user_id'], f'Added user: {d["username"]}', request)
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')
        elif action == 'delete':
            try:
                conn = get_db()
                cursor = conn.cursor()
                uid = int(request.form['user_id'])
                if uid == session.get('user_id'):
                    flash('Cannot delete yourself!', 'error')
                    return redirect(url_for('admin_users'))
                cursor.execute("DELETE FROM users WHERE id=%s", (uid,))
                conn.commit()
                cursor.close()
                conn.close()
                flash('User deleted successfully!', 'success')
                log_user_activity(session['user_id'], f'Deleted user ID: {uid}', request)
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('admin_users'))
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE role IN ('customer','driver') ORDER BY created_at DESC")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        users = []
    return render_template('admin_users.html', users=users)

@app.route('/admin/support')
@permission_required('manage_tickets')
def admin_support():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT t.*, CONCAT(u.first_name,' ',u.last_name) as user_name, u.email 
                       FROM support_tickets t JOIN users u ON t.user_id=u.id 
                       ORDER BY CASE WHEN t.status='open' THEN 1 ELSE 2 END, t.created_at DESC""")
        tickets = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        tickets = []
    return render_template('admin_support.html', tickets=tickets)

@app.route('/admin/support/reply', methods=['POST'])
@permission_required('manage_tickets')
def admin_support_reply():
    ticket_id = request.form.get('ticket_id')
    response = request.form.get('response')
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE support_tickets SET admin_response=%s, status='closed', updated_at=NOW() WHERE id=%s",
                      (response, ticket_id))
        conn.commit()
        
        cursor.execute("SELECT user_id FROM support_tickets WHERE id=%s", (ticket_id,))
        ticket = cursor.fetchone()
        if ticket:
            create_notification(ticket['user_id'], 'Support Ticket Response', 
                              'Your support ticket has been responded to by admin.', 'support')
        
        cursor.close()
        conn.close()
        flash('Response sent successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('admin_support'))

@app.route('/admin/settings')
@permission_required('view_dashboard')
def admin_settings():
    return render_template('admin_settings.html')

# ============ REPORTING AND ANALYTICS MODULE ============

@app.route('/admin/reports')
@permission_required('view_all_reports')
def admin_reports():
    """Main reports dashboard with analytics"""
    stats = {}
    monthly_trends = []
    route_performance = []
    fuel_trends = []
    driver_performance = []
    vehicle_efficiency = []
    booking_trends = []
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # ============ SUMMARY STATISTICS ============
        cursor.execute("SELECT COUNT(*) as c FROM routes WHERE is_active=1")
        stats['total_routes'] = cursor.fetchone()['c']
        
        cursor.execute("SELECT COUNT(*) as c FROM vehicles")
        stats['total_vehicles'] = cursor.fetchone()['c']
        
        cursor.execute("SELECT COUNT(*) as c FROM vehicles WHERE status='available'")
        stats['available_vehicles'] = cursor.fetchone()['c']
        
        cursor.execute("SELECT COUNT(*) as c FROM vehicles WHERE status='in_use'")
        stats['in_use_vehicles'] = cursor.fetchone()['c']
        
        cursor.execute("SELECT COUNT(*) as c FROM vehicles WHERE status='maintenance'")
        stats['maintenance_vehicles'] = cursor.fetchone()['c']
        
        cursor.execute("SELECT COUNT(*) as c FROM users WHERE role='driver' AND is_active=1")
        stats['active_drivers'] = cursor.fetchone()['c']
        
        cursor.execute("SELECT COUNT(*) as c FROM users WHERE role='customer'")
        stats['total_customers'] = cursor.fetchone()['c']
        
        # ============ CURRENT MONTH PERFORMANCE ============
        cursor.execute("""
            SELECT 
                COUNT(*) as total_trips,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_trips,
                SUM(CASE WHEN status = 'on_time' THEN 1 ELSE 0 END) as on_time_trips,
                SUM(CASE WHEN status = 'delayed' THEN 1 ELSE 0 END) as delayed_trips,
                SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled_trips
            FROM schedules 
            WHERE MONTH(schedule_date) = MONTH(CURDATE()) 
            AND YEAR(schedule_date) = YEAR(CURDATE())
        """)
        monthly_data = cursor.fetchone()
        
        stats['total_trips'] = monthly_data['total_trips'] or 0
        stats['completed_trips'] = monthly_data['completed_trips'] or 0
        stats['on_time_trips'] = monthly_data['on_time_trips'] or 0
        stats['delayed_trips'] = monthly_data['delayed_trips'] or 0
        stats['cancelled_trips'] = monthly_data['cancelled_trips'] or 0
        
        if stats['total_trips'] > 0:
            stats['completion_rate'] = round((stats['completed_trips'] / stats['total_trips']) * 100)
            stats['on_time_rate'] = round((stats['on_time_trips'] / stats['total_trips']) * 100)
            stats['delayed_rate'] = round((stats['delayed_trips'] / stats['total_trips']) * 100)
            stats['cancelled_rate'] = round((stats['cancelled_trips'] / stats['total_trips']) * 100)
        else:
            stats['completion_rate'] = stats['on_time_rate'] = stats['delayed_rate'] = stats['cancelled_rate'] = 0
        
        # ============ MONTHLY TRENDS (Last 6 Months) ============
        cursor.execute("""
            SELECT 
                DATE_FORMAT(schedule_date, '%Y-%m') as month,
                COUNT(*) as total_trips,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_trips,
                SUM(CASE WHEN status = 'on_time' THEN 1 ELSE 0 END) as on_time_trips
            FROM schedules 
            WHERE schedule_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(schedule_date, '%Y-%m')
            ORDER BY month ASC
        """)
        monthly_trends = cursor.fetchall()
        
        # ============ ROUTE PERFORMANCE ============
        cursor.execute("""
            SELECT 
                r.route_name,
                r.route_code,
                r.total_distance,
                COUNT(s.id) as total_trips,
                SUM(CASE WHEN s.status = 'completed' THEN 1 ELSE 0 END) as completed_trips,
                SUM(CASE WHEN s.status = 'on_time' THEN 1 ELSE 0 END) as on_time_trips,
                SUM(CASE WHEN s.status = 'delayed' THEN 1 ELSE 0 END) as delayed_trips,
                IFNULL(SUM(CASE WHEN s.status = 'on_time' THEN 1 ELSE 0 END) / NULLIF(COUNT(s.id), 0) * 100, 0) as reliability_score
            FROM routes r
            LEFT JOIN schedules s ON r.id = s.route_id
            WHERE MONTH(s.schedule_date) = MONTH(CURDATE()) OR s.schedule_date IS NULL
            GROUP BY r.id
            ORDER BY reliability_score DESC
        """)
        route_performance = cursor.fetchall()
        
        # ============ FUEL CONSUMPTION TRENDS ============
        cursor.execute("""
            SELECT 
                DATE_FORMAT(fuel_date, '%Y-%m') as month,
                SUM(fuel_liters) as total_liters,
                SUM(total_cost) as total_cost,
                AVG(cost_per_liter) as avg_cost_per_liter
            FROM fuel_logs 
            WHERE fuel_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(fuel_date, '%Y-%m')
            ORDER BY month ASC
        """)
        fuel_trends = cursor.fetchall()
        
        # ============ FUEL EFFICIENCY BY VEHICLE ============
        cursor.execute("""
            SELECT 
                v.registration_number,
                v.vehicle_type,
                COUNT(f.id) as fuel_logs,
                SUM(f.fuel_liters) as total_fuel,
                SUM(f.total_cost) as total_cost,
                MAX(f.odometer_reading) - MIN(f.odometer_reading) as distance_traveled,
                CASE 
                    WHEN (MAX(f.odometer_reading) - MIN(f.odometer_reading)) > 0 
                    THEN SUM(f.fuel_liters) / (MAX(f.odometer_reading) - MIN(f.odometer_reading)) * 100
                    ELSE 0 
                END as fuel_efficiency
            FROM vehicles v
            LEFT JOIN fuel_logs f ON v.id = f.vehicle_id
            WHERE f.fuel_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH) OR f.fuel_date IS NULL
            GROUP BY v.id
            ORDER BY fuel_efficiency ASC
        """)
        vehicle_efficiency = cursor.fetchall()
        
        # ============ DRIVER PERFORMANCE ============
        cursor.execute("""
            SELECT 
                CONCAT(u.first_name, ' ', u.last_name) as driver_name,
                COUNT(s.id) as total_trips,
                SUM(CASE WHEN s.status = 'completed' THEN 1 ELSE 0 END) as completed_trips,
                SUM(CASE WHEN s.status = 'on_time' THEN 1 ELSE 0 END) as on_time_trips,
                SUM(CASE WHEN s.status = 'delayed' THEN 1 ELSE 0 END) as delayed_trips,
                IFNULL(SUM(CASE WHEN s.status = 'on_time' THEN 1 ELSE 0 END) / NULLIF(COUNT(s.id), 0) * 100, 0) as punctuality_rate
            FROM users u
            JOIN schedules s ON u.id = s.driver_id
            WHERE MONTH(s.schedule_date) = MONTH(CURDATE())
            GROUP BY u.id
            ORDER BY punctuality_rate DESC
            LIMIT 10
        """)
        driver_performance = cursor.fetchall()
        
        # ============ FINANCIAL SUMMARY ============
        cursor.execute("""
            SELECT 
                COALESCE(SUM(total_cost), 0) as total_fuel_cost
            FROM fuel_logs 
            WHERE MONTH(fuel_date) = MONTH(CURDATE())
        """)
        fuel_cost = cursor.fetchone()
        stats['monthly_fuel_cost'] = float(fuel_cost['total_fuel_cost'])
        
        cursor.execute("""
            SELECT 
                COALESCE(SUM(total_cost), 0) as total_maintenance_cost
            FROM maintenance_logs 
            WHERE MONTH(maintenance_date) = MONTH(CURDATE())
        """)
        maint_cost = cursor.fetchone()
        stats['monthly_maintenance_cost'] = float(maint_cost['total_maintenance_cost'])
        
        stats['total_operational_cost'] = stats['monthly_fuel_cost'] + stats['monthly_maintenance_cost']
        
        # ============ BOOKING TRENDS ============
        cursor.execute("""
            SELECT 
                DATE_FORMAT(booking_date, '%Y-%m') as month,
                COUNT(*) as total_bookings,
                SUM(total_fare) as total_revenue
            FROM bookings 
            WHERE booking_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(booking_date, '%Y-%m')
            ORDER BY month ASC
        """)
        booking_trends = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Report error: {e}")
        stats = {'total_routes':0, 'total_vehicles':0, 'available_vehicles':0, 'in_use_vehicles':0,
                'maintenance_vehicles':0, 'active_drivers':0, 'total_customers':0, 'total_trips':0,
                'completed_trips':0, 'on_time_trips':0, 'delayed_trips':0, 'cancelled_trips':0,
                'completion_rate':0, 'on_time_rate':0, 'delayed_rate':0, 'cancelled_rate':0,
                'monthly_fuel_cost':0, 'monthly_maintenance_cost':0, 'total_operational_cost':0}
    
    return render_template('admin_reports.html', 
                          stats=stats, 
                          monthly_trends=monthly_trends,
                          route_performance=route_performance,
                          fuel_trends=fuel_trends,
                          driver_performance=driver_performance,
                          vehicle_efficiency=vehicle_efficiency,
                          booking_trends=booking_trends)

@app.route('/admin/reports/export-pdf')
@permission_required('view_all_reports')
def export_reports_pdf():
    """Export comprehensive report as PDF"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get current month data
        cursor.execute("""
            SELECT 
                COUNT(*) as total_trips,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_trips,
                SUM(CASE WHEN status = 'on_time' THEN 1 ELSE 0 END) as on_time_trips,
                SUM(CASE WHEN status = 'delayed' THEN 1 ELSE 0 END) as delayed_trips
            FROM schedules 
            WHERE MONTH(schedule_date) = MONTH(CURDATE())
        """)
        trip_data = cursor.fetchone()
        
        # Get fuel data
        cursor.execute("""
            SELECT 
                COALESCE(SUM(fuel_liters), 0) as total_fuel,
                COALESCE(SUM(total_cost), 0) as total_cost
            FROM fuel_logs 
            WHERE MONTH(fuel_date) = MONTH(CURDATE())
        """)
        fuel_data = cursor.fetchone()
        
        # Get top routes
        cursor.execute("""
            SELECT r.route_name, COUNT(s.id) as trip_count
            FROM routes r
            JOIN schedules s ON r.id = s.route_id
            WHERE MONTH(s.schedule_date) = MONTH(CURDATE())
            GROUP BY r.id
            ORDER BY trip_count DESC
            LIMIT 5
        """)
        top_routes = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, title='SRMSS Monthly Report')
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, alignment=TA_CENTER, spaceAfter=30)
        story.append(Paragraph("SRMSS Monthly Performance Report", title_style))
        story.append(Paragraph(f"Report Date: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Summary Section
        story.append(Paragraph("Executive Summary", styles['Heading2']))
        story.append(Spacer(1, 10))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Trips', str(trip_data['total_trips'] or 0)],
            ['Completed Trips', str(trip_data['completed_trips'] or 0)],
            ['On-Time Trips', str(trip_data['on_time_trips'] or 0)],
            ['Delayed Trips', str(trip_data['delayed_trips'] or 0)],
            ['Total Fuel Used', f"{float(fuel_data['total_fuel'] or 0):.2f} L"],
            ['Total Fuel Cost', f"Rs. {float(fuel_data['total_cost'] or 0):,.2f}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[200, 150])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Top Routes
        story.append(Paragraph("Top Performing Routes", styles['Heading2']))
        story.append(Spacer(1, 10))
        
        routes_data = [['Route Name', 'Number of Trips']]
        for route in top_routes:
            routes_data.append([route['route_name'], str(route['trip_count'])])
        
        routes_table = Table(routes_data, colWidths=[300, 100])
        routes_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(routes_table)
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph("This report is auto-generated by SRMSS System", styles['Normal']))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        
        return make_response(buffer.getvalue(), 200, {
            'Content-Type': 'application/pdf',
            'Content-Disposition': f'inline; filename=srmss_report_{datetime.now().strftime("%Y%m%d")}.pdf'
        })
        
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'error')
        return redirect(url_for('admin_reports'))

@app.route('/admin/reports/export-csv/<report_type>')
@permission_required('view_all_reports')
def export_reports_csv(report_type):
    """Export report as CSV"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        output = io.StringIO()
        
        if report_type == 'routes':
            cursor.execute("""
                SELECT 
                    r.route_code,
                    r.route_name,
                    r.start_point,
                    r.end_point,
                    r.total_distance,
                    r.route_type,
                    COUNT(s.id) as total_trips,
                    SUM(CASE WHEN s.status = 'completed' THEN 1 ELSE 0 END) as completed_trips
                FROM routes r
                LEFT JOIN schedules s ON r.id = s.route_id
                GROUP BY r.id
            """)
            data = cursor.fetchall()
            writer = csv.DictWriter(output, fieldnames=['route_code', 'route_name', 'start_point', 'end_point', 'total_distance', 'route_type', 'total_trips', 'completed_trips'])
            writer.writeheader()
            for row in data:
                writer.writerow(row)
            filename = f"routes_report_{datetime.now().strftime('%Y%m%d')}.csv"
            
        elif report_type == 'fuel':
            cursor.execute("""
                SELECT 
                    v.registration_number,
                    f.fuel_date,
                    f.fuel_liters,
                    f.cost_per_liter,
                    f.total_cost,
                    f.odometer_reading,
                    f.fuel_station
                FROM fuel_logs f
                JOIN vehicles v ON f.vehicle_id = v.id
                ORDER BY f.fuel_date DESC
            """)
            data = cursor.fetchall()
            writer = csv.DictWriter(output, fieldnames=['registration_number', 'fuel_date', 'fuel_liters', 'cost_per_liter', 'total_cost', 'odometer_reading', 'fuel_station'])
            writer.writeheader()
            for row in data:
                writer.writerow(row)
            filename = f"fuel_report_{datetime.now().strftime('%Y%m%d')}.csv"
            
        elif report_type == 'schedules':
            cursor.execute("""
                SELECT 
                    r.route_name,
                    v.registration_number,
                    CONCAT(d.first_name, ' ', d.last_name) as driver_name,
                    s.schedule_date,
                    s.departure_time,
                    s.arrival_time,
                    s.status
                FROM schedules s
                JOIN routes r ON s.route_id = r.id
                JOIN vehicles v ON s.vehicle_id = v.id
                JOIN users d ON s.driver_id = d.id
                ORDER BY s.schedule_date DESC
            """)
            data = cursor.fetchall()
            writer = csv.DictWriter(output, fieldnames=['route_name', 'registration_number', 'driver_name', 'schedule_date', 'departure_time', 'arrival_time', 'status'])
            writer.writeheader()
            for row in data:
                writer.writerow(row)
            filename = f"schedules_report_{datetime.now().strftime('%Y%m%d')}.csv"
            
        elif report_type == 'drivers':
            cursor.execute("""
                SELECT 
                    CONCAT(u.first_name, ' ', u.last_name) as driver_name,
                    u.email,
                    u.phone,
                    COUNT(s.id) as total_trips,
                    SUM(CASE WHEN s.status = 'completed' THEN 1 ELSE 0 END) as completed_trips,
                    SUM(CASE WHEN s.status = 'on_time' THEN 1 ELSE 0 END) as on_time_trips
                FROM users u
                LEFT JOIN schedules s ON u.id = s.driver_id
                WHERE u.role = 'driver'
                GROUP BY u.id
            """)
            data = cursor.fetchall()
            writer = csv.DictWriter(output, fieldnames=['driver_name', 'email', 'phone', 'total_trips', 'completed_trips', 'on_time_trips'])
            writer.writeheader()
            for row in data:
                writer.writerow(row)
            filename = f"drivers_report_{datetime.now().strftime('%Y%m%d')}.csv"
            
        else:
            flash('Invalid report type', 'error')
            return redirect(url_for('admin_reports'))
        
        cursor.close()
        conn.close()
        
        output.seek(0)
        return make_response(output.getvalue(), 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': f'attachment; filename={filename}'
        })
        
    except Exception as e:
        flash(f'Error exporting CSV: {str(e)}', 'error')
        return redirect(url_for('admin_reports'))

@app.route('/api/chart-data')
def chart_data():
    """API endpoint for chart data"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Trip trends for chart
        cursor.execute("""
            SELECT 
                DATE_FORMAT(schedule_date, '%Y-%m') as month,
                COUNT(*) as trips,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed
            FROM schedules 
            WHERE schedule_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(schedule_date, '%Y-%m')
            ORDER BY month ASC
        """)
        trip_trends = cursor.fetchall()
        
        # Fuel trends for chart
        cursor.execute("""
            SELECT 
                DATE_FORMAT(fuel_date, '%Y-%m') as month,
                SUM(fuel_liters) as fuel_liters,
                SUM(total_cost) as fuel_cost
            FROM fuel_logs 
            WHERE fuel_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(fuel_date, '%Y-%m')
            ORDER BY month ASC
        """)
        fuel_chart_data = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'trip_trends': trip_trends,
            'fuel_trends': fuel_chart_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ============ DEPOT MANAGER ROUTES ============

@app.route('/depot-manager/dashboard')
@permission_required('view_dashboard')
def depot_manager_dashboard():
    stats = {}
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as c FROM routes WHERE is_active=1")
        stats['total_routes'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM vehicles")
        stats['total_vehicles'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM schedules WHERE schedule_date = CURDATE()")
        stats['today_schedules'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM fuel_logs WHERE MONTH(fuel_date) = MONTH(CURDATE())")
        stats['monthly_fuel'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM maintenance_logs WHERE MONTH(maintenance_date) = MONTH(CURDATE())")
        stats['monthly_maintenance'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM schedules WHERE schedule_date > CURDATE()")
        stats['upcoming_schedules'] = cursor.fetchone()['c']
        cursor.close()
        conn.close()
    except Exception as e:
        stats = {'total_routes':0, 'total_vehicles':0, 'today_schedules':0, 
                'monthly_fuel':0, 'monthly_maintenance':0, 'upcoming_schedules':0}
    return render_template('depot_manager_dashboard.html', stats=stats)

@app.route('/depot-manager/schedules', methods=['GET', 'POST'])
@permission_required('manage_schedules')
def depot_manager_schedules():
    """Depot Manager schedule management - Create, Read, Update schedules"""
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        # CREATE SCHEDULE
        if action == 'add':
            route_id = request.form.get('route_id')
            vehicle_id = request.form.get('vehicle_id')
            driver_id = request.form.get('driver_id')
            departure_time = request.form.get('departure_time')
            arrival_time = request.form.get('arrival_time')
            schedule_date = request.form.get('schedule_date')
            status = request.form.get('status', 'scheduled')
            
            if not all([route_id, vehicle_id, driver_id, departure_time, arrival_time, schedule_date]):
                flash('Please fill all required fields!', 'error')
                return redirect(url_for('depot_manager_schedules'))
            
            try:
                conn = get_db()
                cursor = conn.cursor()
                
                # Check for conflicts (same vehicle at same time)
                cursor.execute("""
                    SELECT id FROM schedules 
                    WHERE vehicle_id = %s AND schedule_date = %s 
                    AND ((departure_time <= %s AND arrival_time > %s) OR (departure_time < %s AND arrival_time >= %s))
                """, (vehicle_id, schedule_date, arrival_time, departure_time, arrival_time, departure_time))
                
                conflict = cursor.fetchone()
                if conflict:
                    flash('Vehicle is already scheduled for another trip at this time!', 'error')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('depot_manager_schedules'))
                
                # Check driver availability
                cursor.execute("""
                    SELECT id FROM schedules 
                    WHERE driver_id = %s AND schedule_date = %s 
                    AND ((departure_time <= %s AND arrival_time > %s) OR (departure_time < %s AND arrival_time >= %s))
                """, (driver_id, schedule_date, arrival_time, departure_time, arrival_time, departure_time))
                
                driver_conflict = cursor.fetchone()
                if driver_conflict:
                    flash('Driver is already assigned to another trip at this time!', 'error')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('depot_manager_schedules'))
                
                cursor.execute("""
                    INSERT INTO schedules (route_id, vehicle_id, driver_id, departure_time, 
                                           arrival_time, schedule_date, status) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (route_id, vehicle_id, driver_id, departure_time, 
                      arrival_time, schedule_date, status))
                
                conn.commit()
                
                # Update vehicle status to in_use
                cursor.execute("UPDATE vehicles SET status = 'in_use' WHERE id = %s", (vehicle_id,))
                conn.commit()
                
                # Send notification to driver
                create_notification(driver_id, 'New Schedule Assigned', 
                                  f'You have been assigned a new trip on {schedule_date} at {departure_time}', 'schedule')
                
                cursor.close()
                conn.close()
                
                flash('Schedule created successfully!', 'success')
                log_user_activity(session['user_id'], f'Created schedule for driver ID: {driver_id}', request)
                
            except Exception as e:
                flash(f'Error creating schedule: {str(e)}', 'error')
            
            return redirect(url_for('depot_manager_schedules'))
        
        # UPDATE SCHEDULE
        elif action == 'edit':
            schedule_id = request.form.get('schedule_id')
            route_id = request.form.get('route_id')
            vehicle_id = request.form.get('vehicle_id')
            driver_id = request.form.get('driver_id')
            schedule_date = request.form.get('schedule_date')
            departure_time = request.form.get('departure_time')
            arrival_time = request.form.get('arrival_time')
            status = request.form.get('status', 'scheduled')
            
            if not all([schedule_id, route_id, vehicle_id, driver_id, schedule_date, departure_time, arrival_time]):
                flash('Please fill all required fields!', 'error')
                return redirect(url_for('depot_manager_schedules'))
            
            try:
                conn = get_db()
                cursor = conn.cursor()
                
                # Get old schedule data
                cursor.execute("SELECT driver_id, vehicle_id FROM schedules WHERE id = %s", (schedule_id,))
                old_data = cursor.fetchone()
                old_driver_id = old_data['driver_id'] if old_data else None
                old_vehicle_id = old_data['vehicle_id'] if old_data else None
                
                # Check for conflicts (excluding current schedule)
                cursor.execute("""
                    SELECT id FROM schedules 
                    WHERE vehicle_id = %s AND schedule_date = %s AND id != %s
                    AND ((departure_time <= %s AND arrival_time > %s) OR (departure_time < %s AND arrival_time >= %s))
                """, (vehicle_id, schedule_date, schedule_id, arrival_time, departure_time, arrival_time, departure_time))
                
                conflict = cursor.fetchone()
                if conflict:
                    flash('Vehicle is already scheduled for another trip at this time!', 'error')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('depot_manager_schedules'))
                
                # Check driver availability
                cursor.execute("""
                    SELECT id FROM schedules 
                    WHERE driver_id = %s AND schedule_date = %s AND id != %s
                    AND ((departure_time <= %s AND arrival_time > %s) OR (departure_time < %s AND arrival_time >= %s))
                """, (driver_id, schedule_date, schedule_id, arrival_time, departure_time, arrival_time, departure_time))
                
                driver_conflict = cursor.fetchone()
                if driver_conflict:
                    flash('Driver is already assigned to another trip at this time!', 'error')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('depot_manager_schedules'))
                
                # Update schedule
                cursor.execute("""
                    UPDATE schedules 
                    SET route_id = %s, vehicle_id = %s, driver_id = %s, 
                        schedule_date = %s, departure_time = %s, arrival_time = %s, status = %s
                    WHERE id = %s
                """, (route_id, vehicle_id, driver_id, schedule_date, departure_time, arrival_time, status, schedule_id))
                
                conn.commit()
                
                # Update vehicle status if changed
                if old_vehicle_id and old_vehicle_id != int(vehicle_id):
                    # Check if old vehicle has any other schedules today
                    cursor.execute("SELECT id FROM schedules WHERE vehicle_id = %s AND schedule_date = %s AND id != %s", 
                                 (old_vehicle_id, schedule_date, schedule_id))
                    if not cursor.fetchone():
                        cursor.execute("UPDATE vehicles SET status = 'available' WHERE id = %s", (old_vehicle_id,))
                        conn.commit()
                
                # Update new vehicle status
                cursor.execute("UPDATE vehicles SET status = 'in_use' WHERE id = %s", (vehicle_id,))
                conn.commit()
                
                # Send notification to driver about schedule update
                if status in ['scheduled', 'on_time']:
                    create_notification(driver_id, 'Schedule Updated', 
                                      f'Your schedule on {schedule_date} has been updated. Departure: {departure_time}, Arrival: {arrival_time}', 'schedule')
                    
                    # If driver changed, also notify old driver
                    if old_driver_id and old_driver_id != int(driver_id):
                        create_notification(old_driver_id, 'Schedule Removed', 
                                          f'Your schedule on {schedule_date} has been reassigned to another driver.', 'schedule')
                
                cursor.close()
                conn.close()
                
                flash('Schedule updated successfully!', 'success')
                log_user_activity(session['user_id'], f'Updated schedule ID: {schedule_id}', request)
                
            except Exception as e:
                flash(f'Error updating schedule: {str(e)}', 'error')
            
            return redirect(url_for('depot_manager_schedules'))
    
    # GET request - display schedules
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get all schedules with details - REMOVED created_by column
        cursor.execute("""
            SELECT s.*, r.route_name, r.start_point, r.end_point, r.total_distance, r.base_fare,
                   v.registration_number, v.vehicle_code, v.seating_capacity,
                   CONCAT(d.first_name, ' ', d.last_name) as driver_name
            FROM schedules s 
            JOIN routes r ON s.route_id = r.id 
            JOIN vehicles v ON s.vehicle_id = v.id 
            JOIN users d ON s.driver_id = d.id 
            ORDER BY s.schedule_date DESC, s.departure_time
        """)
        schedules = cursor.fetchall()
        
        # Get routes for dropdown
        cursor.execute("SELECT id, route_name, start_point, end_point FROM routes WHERE is_active = 1")
        routes = cursor.fetchall()
        
        # Get available vehicles (not in maintenance)
        cursor.execute("SELECT id, registration_number, vehicle_code, seating_capacity FROM vehicles WHERE status != 'maintenance'")
        vehicles = cursor.fetchall()
        
        # Get drivers
        cursor.execute("SELECT id, first_name, last_name, username FROM users WHERE role = 'driver' AND is_active = 1")
        drivers = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        schedules = []
        routes = []
        vehicles = []
        drivers = []
        flash(f'Error loading data: {str(e)}', 'error')
    
    return render_template('depot_manager_schedules.html', 
                          schedules=schedules, 
                          routes=routes, 
                          vehicles=vehicles, 
                          drivers=drivers)

@app.route('/depot-manager/fuel-logs', methods=['GET', 'POST'])
@permission_required('manage_fuel_logs')
def depot_manager_fuel_logs():
    """Depot Manager fuel log management - Create, Read fuel logs"""
    
    if request.method == 'POST':
        vehicle_id = request.form.get('vehicle_id')
        fuel_date = request.form.get('fuel_date')
        fuel_liters = request.form.get('fuel_liters')
        cost_per_liter = request.form.get('cost_per_liter')
        total_cost = request.form.get('total_cost')
        odometer_reading = request.form.get('odometer_reading')
        fuel_station = request.form.get('fuel_station', '')
        
        # Validation
        if not all([vehicle_id, fuel_date, fuel_liters, cost_per_liter, total_cost, odometer_reading]):
            flash('Please fill all required fields!', 'error')
            return redirect(url_for('depot_manager_fuel_logs'))
        
        # Handle receipt upload
        receipt_filename = None
        if 'receipt' in request.files:
            file = request.files['receipt']
            if file and file.filename and allowed_file(file.filename):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"fuel_{vehicle_id}_{timestamp}.{file_ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                receipt_filename = f"uploads/receipts/{filename}"
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            # Get previous odometer reading for validation
            cursor.execute("""
                SELECT odometer_reading FROM fuel_logs 
                WHERE vehicle_id = %s 
                ORDER BY fuel_date DESC, created_at DESC LIMIT 1
            """, (vehicle_id,))
            previous_log = cursor.fetchone()
            
            if previous_log and float(odometer_reading) < float(previous_log['odometer_reading']):
                flash(f'Warning: Odometer reading ({odometer_reading} km) is less than previous reading ({previous_log["odometer_reading"]} km). Please verify.', 'warning')
            
            cursor.execute("""
                INSERT INTO fuel_logs (vehicle_id, fuel_date, fuel_liters, cost_per_liter,
                                       total_cost, odometer_reading, fuel_station, receipt_path, logged_by) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (vehicle_id, fuel_date, fuel_liters, cost_per_liter,
                  total_cost, odometer_reading, fuel_station,
                  receipt_filename, session['user_id']))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Fuel log added successfully!', 'success')
            log_user_activity(session['user_id'], f'Added fuel log for vehicle ID: {vehicle_id}', request)
            
        except Exception as e:
            flash(f'Error adding fuel log: {str(e)}', 'error')
        
        return redirect(url_for('depot_manager_fuel_logs'))
    
    # GET request - display fuel logs
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get fuel logs with vehicle details and user who logged
        cursor.execute("""
            SELECT f.*, 
                   v.registration_number, 
                   v.vehicle_code,
                   v.vehicle_type,
                   CONCAT(u.first_name, ' ', u.last_name) as logged_by_name
            FROM fuel_logs f 
            JOIN vehicles v ON f.vehicle_id = v.id 
            LEFT JOIN users u ON f.logged_by = u.id
            ORDER BY f.fuel_date DESC, f.created_at DESC
            LIMIT 100
        """)
        fuel_logs = cursor.fetchall()
        
        # Get all vehicles for dropdown
        cursor.execute("SELECT id, registration_number, vehicle_code, vehicle_type FROM vehicles ORDER BY registration_number")
        vehicles = cursor.fetchall()
        
        # Get fuel statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_logs,
                COALESCE(SUM(fuel_liters), 0) as total_fuel,
                COALESCE(SUM(total_cost), 0) as total_cost,
                COALESCE(AVG(cost_per_liter), 0) as avg_cost
            FROM fuel_logs 
            WHERE MONTH(fuel_date) = MONTH(CURDATE()) AND YEAR(fuel_date) = YEAR(CURDATE())
        """)
        monthly_stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error loading fuel logs: {e}")
        fuel_logs = []
        vehicles = []
        monthly_stats = {'total_logs': 0, 'total_fuel': 0, 'total_cost': 0, 'avg_cost': 0}
    
    return render_template('depot_manager_fuel_logs.html', 
                          fuel_logs=fuel_logs, 
                          vehicles=vehicles,
                          monthly_stats=monthly_stats)

@app.route('/depot-manager/maintenance', methods=['GET', 'POST'])
@permission_required('manage_maintenance')
def depot_manager_maintenance():
    """Depot Manager maintenance management - View and Add only (No Edit/Delete)"""
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        # ONLY ALLOW ADD - NO EDIT OR DELETE FOR DEPOT MANAGER
        if action == 'add':
            vehicle_id = request.form.get('vehicle_id')
            maintenance_date = request.form.get('maintenance_date')
            maintenance_type = request.form.get('maintenance_type', 'routine')
            description = request.form.get('description')
            labor_cost = request.form.get('labor_cost', 0)
            parts_cost = request.form.get('parts_cost', 0)
            total_cost = request.form.get('total_cost')
            service_center = request.form.get('service_center', '')
            next_service_date = request.form.get('next_service_date', '')
            
            if not all([vehicle_id, maintenance_date, description, total_cost]):
                flash('Please fill all required fields!', 'error')
                return redirect(url_for('depot_manager_maintenance'))
            
            try:
                conn = get_db()
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO maintenance_logs (vehicle_id, maintenance_date, maintenance_type, 
                                                   description, labor_cost, parts_cost, total_cost, 
                                                   service_center, next_service_date) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (vehicle_id, maintenance_date, maintenance_type, description,
                      labor_cost, parts_cost, total_cost, service_center, next_service_date))
                
                conn.commit()
                
                # If emergency maintenance, update vehicle status
                if maintenance_type == 'emergency':
                    cursor.execute("UPDATE vehicles SET status = 'maintenance' WHERE id = %s", (vehicle_id,))
                    conn.commit()
                    flash('⚠️ Emergency maintenance recorded. Vehicle status set to Maintenance.', 'warning')
                else:
                    flash('Maintenance record added successfully!', 'success')
                
                cursor.close()
                conn.close()
                
                log_user_activity(session['user_id'], f'Added maintenance for vehicle ID: {vehicle_id}', request)
                
            except Exception as e:
                flash(f'Error adding maintenance record: {str(e)}', 'error')
            
            return redirect(url_for('depot_manager_maintenance'))
        
        # BLOCK EDIT AND DELETE FOR DEPOT MANAGER
        elif action == 'edit':
            flash('You do not have permission to edit maintenance records. Only view and add are allowed.', 'error')
            return redirect(url_for('depot_manager_maintenance'))
        
        elif action == 'delete':
            flash('You do not have permission to delete maintenance records. Only view and add are allowed.', 'error')
            return redirect(url_for('depot_manager_maintenance'))
    
    # GET request - display maintenance records (VIEW ONLY)
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get all maintenance logs with vehicle details
        cursor.execute("""
            SELECT m.*, 
                   v.registration_number, 
                   v.vehicle_code,
                   v.vehicle_type,
                   v.status as vehicle_status
            FROM maintenance_logs m 
            JOIN vehicles v ON m.vehicle_id = v.id 
            ORDER BY m.maintenance_date DESC, m.created_at DESC
        """)
        maintenance_logs = cursor.fetchall()
        
        # Get all vehicles for dropdown
        cursor.execute("SELECT id, registration_number, vehicle_code, vehicle_type, status FROM vehicles ORDER BY registration_number")
        vehicles = cursor.fetchall()
        
        # Get maintenance statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_records,
                SUM(CASE WHEN maintenance_type = 'routine' THEN 1 ELSE 0 END) as routine_count,
                SUM(CASE WHEN maintenance_type = 'emergency' THEN 1 ELSE 0 END) as emergency_count,
                SUM(CASE WHEN maintenance_type = 'corrective' THEN 1 ELSE 0 END) as corrective_count,
                SUM(CASE WHEN maintenance_type = 'preventive' THEN 1 ELSE 0 END) as preventive_count,
                COALESCE(SUM(total_cost), 0) as total_cost,
                COALESCE(AVG(total_cost), 0) as avg_cost
            FROM maintenance_logs 
            WHERE MONTH(maintenance_date) = MONTH(CURDATE()) AND YEAR(maintenance_date) = YEAR(CURDATE())
        """)
        monthly_stats = cursor.fetchone()
        
        # Get vehicles currently in maintenance
        cursor.execute("""
            SELECT COUNT(*) as count FROM vehicles WHERE status = 'maintenance'
        """)
        maintenance_vehicles = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error loading maintenance logs: {e}")
        maintenance_logs = []
        vehicles = []
        monthly_stats = {'total_records': 0, 'routine_count': 0, 'emergency_count': 0, 
                        'corrective_count': 0, 'preventive_count': 0, 'total_cost': 0, 'avg_cost': 0}
        maintenance_vehicles = {'count': 0}
    
    return render_template('depot_manager_maintenance.html', 
                          maintenance_logs=maintenance_logs, 
                          vehicles=vehicles,
                          monthly_stats=monthly_stats,
                          maintenance_vehicles=maintenance_vehicles)

@app.route('/depot-manager/reports')
@permission_required('view_reports')
def depot_manager_reports():
    stats = {}
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total_schedules FROM schedules WHERE MONTH(schedule_date) = MONTH(CURDATE())")
        stats['total_schedules'] = cursor.fetchone()['total_schedules']
        cursor.execute("SELECT COUNT(*) as completed_schedules FROM schedules WHERE MONTH(schedule_date) = MONTH(CURDATE()) AND status='completed'")
        stats['completed_schedules'] = cursor.fetchone()['completed_schedules']
        cursor.execute("SELECT COALESCE(SUM(total_cost),0) as total_fuel_cost FROM fuel_logs WHERE MONTH(fuel_date) = MONTH(CURDATE())")
        stats['total_fuel_cost'] = float(cursor.fetchone()['total_fuel_cost'])
        cursor.execute("SELECT COALESCE(SUM(total_cost),0) as total_maintenance_cost FROM maintenance_logs WHERE MONTH(maintenance_date) = MONTH(CURDATE())")
        stats['total_maintenance_cost'] = float(cursor.fetchone()['total_maintenance_cost'])
        stats['total_operational_cost'] = stats['total_fuel_cost'] + stats['total_maintenance_cost']
        cursor.close()
        conn.close()
    except:
        stats = {'total_schedules':0, 'completed_schedules':0, 'total_fuel_cost':0, 'total_maintenance_cost':0, 'total_operational_cost':0}
    return render_template('depot_manager_reports.html', stats=stats)

# ============ SUPERVISOR ROUTES ============

@app.route('/supervisor/dashboard')
@permission_required('view_dashboard')
def supervisor_dashboard():
    stats = {}
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as c FROM routes WHERE is_active=1")
        stats['total_routes'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM vehicles")
        stats['total_vehicles'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM users WHERE role='driver' AND is_active=1")
        stats['total_drivers'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM schedules WHERE schedule_date = CURDATE()")
        stats['today_schedules'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM support_tickets WHERE status = 'open'")
        stats['open_tickets'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM driver_locations WHERE updated_at >= DATE_SUB(NOW(), INTERVAL 30 MINUTE)")
        stats['active_buses'] = cursor.fetchone()['c']
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Supervisor dashboard error: {e}")
        stats = {'total_routes':0, 'total_vehicles':0, 'total_drivers':0, 
                'today_schedules':0, 'open_tickets':0, 'active_buses':0}
    return render_template('supervisor_dashboard.html', stats=stats)

@app.route('/supervisor/tickets')
@permission_required('manage_tickets')
def supervisor_tickets():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT t.*, CONCAT(u.first_name,' ',u.last_name) as user_name, u.email 
                       FROM support_tickets t JOIN users u ON t.user_id=u.id 
                       ORDER BY CASE WHEN t.status='open' THEN 1 ELSE 2 END, t.created_at DESC""")
        tickets = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        tickets = []
    return render_template('supervisor_tickets.html', tickets=tickets)

@app.route('/supervisor/tickets/reply', methods=['POST'])
@permission_required('manage_tickets')
def supervisor_tickets_reply():
    ticket_id = request.form.get('ticket_id')
    response = request.form.get('response')
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE support_tickets SET admin_response=%s, status='closed', updated_at=NOW() WHERE id=%s",
                      (response, ticket_id))
        conn.commit()
        cursor.execute("SELECT user_id FROM support_tickets WHERE id=%s", (ticket_id,))
        ticket = cursor.fetchone()
        if ticket:
            create_notification(ticket['user_id'], 'Support Ticket Response', 'Your support ticket has been responded to.', 'support')
        cursor.close()
        conn.close()
        flash('Response sent successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('supervisor_tickets'))

@app.route('/supervisor/reports')
@permission_required('view_reports')
def supervisor_reports():
    stats = {}
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total_schedules FROM schedules WHERE MONTH(schedule_date) = MONTH(CURDATE())")
        stats['total_schedules'] = cursor.fetchone()['total_schedules']
        cursor.execute("SELECT COUNT(*) as completed_schedules FROM schedules WHERE MONTH(schedule_date) = MONTH(CURDATE()) AND status='completed'")
        stats['completed_schedules'] = cursor.fetchone()['completed_schedules']
        cursor.execute("SELECT COUNT(*) as on_time_schedules FROM schedules WHERE MONTH(schedule_date) = MONTH(CURDATE()) AND status='on_time'")
        stats['on_time_schedules'] = cursor.fetchone()['on_time_schedules']
        if stats['total_schedules'] > 0:
            stats['completion_rate'] = round((stats['completed_schedules'] / stats['total_schedules']) * 100)
            stats['on_time_rate'] = round((stats['on_time_schedules'] / stats['total_schedules']) * 100)
        else:
            stats['completion_rate'] = 0
            stats['on_time_rate'] = 0
        cursor.close()
        conn.close()
    except:
        stats = {'total_schedules':0, 'completed_schedules':0, 'on_time_schedules':0, 'completion_rate':0, 'on_time_rate':0}
    return render_template('supervisor_reports.html', stats=stats)

@app.route('/supervisor/reports/export-pdf')
@permission_required('view_reports')
def supervisor_export_pdf():
    """Export supervisor report as PDF"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get current month data
        cursor.execute("""
            SELECT 
                COUNT(*) as total_trips,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_trips,
                SUM(CASE WHEN status = 'on_time' THEN 1 ELSE 0 END) as on_time_trips,
                SUM(CASE WHEN status = 'delayed' THEN 1 ELSE 0 END) as delayed_trips
            FROM schedules 
            WHERE MONTH(schedule_date) = MONTH(CURDATE())
        """)
        trip_data = cursor.fetchone()
        
        # Get recent schedules
        cursor.execute("""
            SELECT s.*, r.route_name, v.registration_number, 
                   CONCAT(d.first_name,' ',d.last_name) as driver_name 
            FROM schedules s 
            JOIN routes r ON s.route_id=r.id 
            JOIN vehicles v ON s.vehicle_id=v.id 
            JOIN users d ON s.driver_id=d.id 
            ORDER BY s.created_at DESC LIMIT 10
        """)
        recent_schedules = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, title='SRMSS Supervisor Report')
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, alignment=TA_CENTER, spaceAfter=30)
        story.append(Paragraph("SRMSS Supervisor Performance Report", title_style))
        story.append(Paragraph(f"Report Date: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Summary Section
        story.append(Paragraph("Executive Summary", styles['Heading2']))
        story.append(Spacer(1, 10))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Trips', str(trip_data['total_trips'] or 0)],
            ['Completed Trips', str(trip_data['completed_trips'] or 0)],
            ['On-Time Trips', str(trip_data['on_time_trips'] or 0)],
            ['Delayed Trips', str(trip_data['delayed_trips'] or 0)],
        ]
        
        summary_table = Table(summary_data, colWidths=[200, 150])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Recent Schedules
        story.append(Paragraph("Recent Schedule Activity", styles['Heading2']))
        story.append(Spacer(1, 10))
        
        schedules_data = [['Date', 'Route', 'Vehicle', 'Driver', 'Status']]
        for schedule in recent_schedules[:10]:
            schedules_data.append([
                str(schedule['schedule_date']),
                schedule['route_name'],
                schedule['registration_number'],
                schedule['driver_name'],
                schedule['status']
            ])
        
        schedules_table = Table(schedules_data, colWidths=[80, 100, 80, 100, 60])
        schedules_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        story.append(schedules_table)
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph("This report is auto-generated by SRMSS System", styles['Normal']))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        
        return make_response(buffer.getvalue(), 200, {
            'Content-Type': 'application/pdf',
            'Content-Disposition': f'inline; filename=srmss_supervisor_report_{datetime.now().strftime("%Y%m%d")}.pdf'
        })
        
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'error')
        return redirect(url_for('supervisor_reports'))

@app.route('/supervisor/reports/export-csv')
@permission_required('view_reports')
def supervisor_export_csv():
    """Export supervisor report as CSV"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        output = io.StringIO()
        
        cursor.execute("""
            SELECT 
                s.schedule_date,
                r.route_name,
                v.registration_number,
                CONCAT(d.first_name, ' ', d.last_name) as driver_name,
                s.departure_time,
                s.arrival_time,
                s.status
            FROM schedules s
            JOIN routes r ON s.route_id = r.id
            JOIN vehicles v ON s.vehicle_id = v.id
            JOIN users d ON s.driver_id = d.id
            WHERE MONTH(s.schedule_date) = MONTH(CURDATE())
            ORDER BY s.schedule_date DESC
        """)
        data = cursor.fetchall()
        
        writer = csv.DictWriter(output, fieldnames=['schedule_date', 'route_name', 'registration_number', 'driver_name', 'departure_time', 'arrival_time', 'status'])
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        
        cursor.close()
        conn.close()
        
        output.seek(0)
        return make_response(output.getvalue(), 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': f'attachment; filename=supervisor_report_{datetime.now().strftime("%Y%m%d")}.csv'
        })
        
    except Exception as e:
        flash(f'Error exporting CSV: {str(e)}', 'error')
        return redirect(url_for('supervisor_reports'))

# ============ PROFILE ROUTES (All Roles) ============

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET first_name=%s, last_name=%s, phone=%s, address=%s WHERE id=%s",
                          (first_name, last_name, phone, address, session['user_id']))
            conn.commit()
            cursor.close()
            conn.close()
            
            session['first_name'] = first_name
            session['last_name'] = last_name
            
            flash('Profile updated successfully!', 'success')
            log_user_activity(session['user_id'], 'Profile updated', request)
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('profile'))
    
    user = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
    except:
        user = None
    
    role = session.get('role')
    template_map = {
        'admin': 'admin_profile.html',
        'depot_manager': 'depot_manager_profile.html',
        'supervisor': 'supervisor_profile.html',
        'driver': 'driver_profile.html',
        'customer': 'customer_profile.html'
    }
    return render_template(template_map.get(role, 'profile.html'), user=user)

# ============ NOTIFICATIONS (All Roles) ============

@app.route('/notifications')
def view_notifications():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    notifications = []
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notifications WHERE user_id=%s ORDER BY created_at DESC LIMIT 50", 
                      (session['user_id'],))
        notifications = cursor.fetchall()
        cursor.execute("UPDATE notifications SET is_read=1 WHERE user_id=%s AND is_read=0", (session['user_id'],))
        conn.commit()
        cursor.close()
        conn.close()
    except:
        pass
    
    role = session.get('role')
    template_map = {
        'admin': 'admin_notifications.html',
        'depot_manager': 'depot_manager_notifications.html',
        'supervisor': 'supervisor_notifications.html',
        'driver': 'driver_notifications.html',
        'customer': 'customer_notifications.html'
    }
    return render_template(template_map.get(role, 'notifications.html'), notifications=notifications)

@app.route('/notifications/mark-read', methods=['POST'])
def mark_notifications_read():
    if 'user_id' not in session:
        return jsonify({'success': False})
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE notifications SET is_read=1 WHERE user_id=%s", (session['user_id'],))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})

# ============ DRIVER ROUTES ============

@app.route('/driver/dashboard')
@permission_required('view_dashboard')
def driver_dashboard():
    driver_id = session.get('user_id')
    stats = {}
    today_schedules = []
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as c FROM schedules WHERE driver_id=%s AND MONTH(schedule_date)=MONTH(CURDATE())", (driver_id,))
        stats['monthly_trips'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM schedules WHERE driver_id=%s AND schedule_date=CURDATE()", (driver_id,))
        stats['today_trips'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM schedules WHERE driver_id=%s AND schedule_date=CURDATE() AND status IN ('scheduled','on_time')", (driver_id,))
        stats['pending_trips'] = cursor.fetchone()['c']
        
        cursor.execute("""SELECT s.*, r.route_name, r.start_point, r.end_point, v.registration_number 
                       FROM schedules s 
                       JOIN routes r ON s.route_id=r.id 
                       JOIN vehicles v ON s.vehicle_id=v.id 
                       WHERE s.driver_id=%s AND s.schedule_date >= CURDATE() 
                       ORDER BY s.schedule_date, s.departure_time LIMIT 5""", (driver_id,))
        today_schedules = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        stats = {'monthly_trips':0, 'today_trips':0, 'pending_trips':0}
    return render_template('driver_dashboard.html', stats=stats, today_schedules=today_schedules)

@app.route('/driver/schedule')
@permission_required('view_assigned_schedules')
def driver_schedule():
    driver_id = session.get('user_id')
    schedules = []
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT s.*, r.route_name, r.start_point, r.end_point, r.total_distance, v.registration_number 
                       FROM schedules s 
                       JOIN routes r ON s.route_id=r.id 
                       JOIN vehicles v ON s.vehicle_id=v.id 
                       WHERE s.driver_id=%s 
                       ORDER BY s.schedule_date DESC, s.departure_time""", (driver_id,))
        schedules = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        schedules = []
    return render_template('driver_schedule.html', schedules=schedules)

@app.route('/driver/today-route')
@permission_required('view_assigned_schedules')
def driver_today_route():
    driver_id = session.get('user_id')
    today_schedule = None
    all_today = []
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT s.*, r.route_name, r.start_point, r.end_point, r.intermediate_stops,
                       r.total_distance, r.route_type, r.base_fare,
                       v.registration_number, v.vehicle_code, v.vehicle_type, v.seating_capacity, v.fuel_type 
                       FROM schedules s 
                       JOIN routes r ON s.route_id=r.id 
                       JOIN vehicles v ON s.vehicle_id=v.id 
                       WHERE s.driver_id=%s AND s.schedule_date=CURDATE() 
                       ORDER BY s.departure_time""", (driver_id,))
        all_today = cursor.fetchall()
        if all_today:
            today_schedule = all_today[0]
        cursor.close()
        conn.close()
    except:
        pass
    return render_template('driver_today_route.html', today_schedule=today_schedule, all_today=all_today)

@app.route('/driver/fuel-log', methods=['GET', 'POST'])
@permission_required('manage_own_fuel_logs')
def driver_fuel_log():
    driver_id = session.get('user_id')
    fuel_logs = []
    vehicles = []
    
    if request.method == 'POST':
        d = request.form
        if not all([d.get('vehicle_id'), d.get('fuel_date'), d.get('fuel_liters'), 
                   d.get('cost_per_liter'), d.get('total_cost'), d.get('odometer_reading')]):
            flash('Fill all fields!', 'error')
            return redirect(url_for('driver_fuel_log'))
        
        receipt_filename = None
        if 'receipt' in request.files:
            file = request.files['receipt']
            if file and file.filename and allowed_file(file.filename):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"fuel_{driver_id}_{timestamp}.{file.filename.rsplit('.', 1)[1].lower()}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                receipt_filename = f"uploads/receipts/{filename}"
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO fuel_logs (vehicle_id, fuel_date, fuel_liters, cost_per_liter, total_cost, odometer_reading, fuel_station, logged_by, receipt_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                          (d['vehicle_id'], d['fuel_date'], d['fuel_liters'], d['cost_per_liter'], d['total_cost'], 
                           d['odometer_reading'], d.get('fuel_station', ''), driver_id, receipt_filename))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Fuel log added successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('driver_fuel_log'))
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT f.*, v.registration_number, v.vehicle_code 
                       FROM fuel_logs f 
                       JOIN vehicles v ON f.vehicle_id = v.id 
                       WHERE f.logged_by = %s 
                       ORDER BY f.fuel_date DESC""", (driver_id,))
        fuel_logs = cursor.fetchall()
        cursor.execute("SELECT id, registration_number, vehicle_code FROM vehicles")
        vehicles = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        fuel_logs = []
        vehicles = []
    
    return render_template('driver_fuel_log.html', fuel_logs=fuel_logs, vehicles=vehicles)

@app.route('/driver/reports')
@permission_required('view_own_reports')
def driver_reports():
    driver_id = session.get('user_id')
    stats = {}
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total_trips FROM schedules WHERE driver_id=%s", (driver_id,))
        stats['total_trips'] = cursor.fetchone()['total_trips']
        cursor.execute("SELECT COUNT(*) as completed FROM schedules WHERE driver_id=%s AND status='completed'", (driver_id,))
        stats['completed'] = cursor.fetchone()['completed']
        cursor.execute("SELECT COUNT(*) as on_time FROM schedules WHERE driver_id=%s AND status='on_time'", (driver_id,))
        stats['on_time'] = cursor.fetchone()['on_time']
        cursor.execute("SELECT COALESCE(SUM(total_cost),0) as total_fuel_cost FROM fuel_logs WHERE logged_by=%s", (driver_id,))
        stats['total_fuel_cost'] = cursor.fetchone()['total_fuel_cost']
        cursor.execute("SELECT COALESCE(SUM(fuel_liters),0) as total_fuel FROM fuel_logs WHERE logged_by=%s", (driver_id,))
        stats['total_fuel'] = cursor.fetchone()['total_fuel']
        cursor.close()
        conn.close()
    except:
        stats = {'total_trips':0, 'completed':0, 'on_time':0, 'total_fuel_cost':0, 'total_fuel':0}
    return render_template('driver_reports.html', stats=stats)

@app.route('/driver/profile', methods=['GET', 'POST'])
@permission_required('update_profile')
def driver_profile():
    driver_id = session.get('user_id')
    
    if request.method == 'POST':
        phone = request.form.get('phone')
        address = request.form.get('address')
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET phone=%s, address=%s WHERE id=%s", (phone, address, driver_id))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('driver_profile'))
    
    user = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (driver_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
    except:
        user = None
    return render_template('driver_profile.html', user=user)

@app.route('/driver/update-location', methods=['POST'])
@permission_required('update_live_location')
def driver_update_location():
    data = request.get_json()
    if not data.get('latitude') or not data.get('longitude'):
        return jsonify({'success': False}), 400
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM driver_locations WHERE driver_id=%s AND schedule_id=%s", 
                      (session['user_id'], data.get('schedule_id')))
        if cursor.fetchone():
            cursor.execute("UPDATE driver_locations SET latitude=%s, longitude=%s, speed=%s, heading=%s, updated_at=NOW() WHERE driver_id=%s AND schedule_id=%s",
                          (data['latitude'], data['longitude'], data.get('speed', 0), data.get('heading', 'N'), 
                           session['user_id'], data.get('schedule_id')))
        else:
            cursor.execute("INSERT INTO driver_locations (driver_id, schedule_id, latitude, longitude, speed, heading) VALUES (%s, %s, %s, %s, %s, %s)",
                          (session['user_id'], data.get('schedule_id'), data['latitude'], data['longitude'], 
                           data.get('speed', 0), data.get('heading', 'N')))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ============ CUSTOMER ROUTES ============

@app.route('/customer/dashboard')
@permission_required('view_dashboard')
def customer_dashboard():
    customer_id = session.get('user_id')
    stats = {}
    popular_routes = []
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as c FROM bookings WHERE customer_id=%s AND status='confirmed'", (customer_id,))
        stats['active_bookings'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM routes WHERE is_active=1")
        stats['total_routes'] = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM driver_locations WHERE updated_at >= DATE_SUB(NOW(), INTERVAL 5 MINUTE)")
        stats['active_buses'] = cursor.fetchone()['c']
        cursor.execute("SELECT * FROM routes WHERE is_active=1 LIMIT 4")
        popular_routes = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        stats = {'active_bookings':0, 'total_routes':0, 'active_buses':0}
    return render_template('customer_dashboard.html', stats=stats, popular_routes=popular_routes)

# @app.route('/customer/routes')
# @permission_required('view_routes')
# def customer_routes():
#     routes = []
#     try:
#         conn = get_db()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM routes WHERE is_active=1 ORDER BY route_name")
#         routes = cursor.fetchall()
#         cursor.close()
#         conn.close()
#     except:
#         routes = []
#     return render_template('customer_routes.html', routes=routes)

@app.route('/customer/routes')
@permission_required('view_routes')
def customer_routes():
    """Customer routes page with search functionality"""
    search_from = request.args.get('from', '').strip()
    search_to = request.args.get('to', '').strip()
    
    routes = []
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Base query
        query = "SELECT * FROM routes WHERE is_active = 1"
        params = []
        
        # Add search filters
        if search_from and search_to:
            # Search for routes that match both start and end points (case insensitive)
            query += " AND (LOWER(start_point) LIKE %s OR LOWER(end_point) LIKE %s OR LOWER(route_name) LIKE %s)"
            search_pattern = f"%{search_from.lower()}%"
            search_pattern2 = f"%{search_to.lower()}%"
            params.extend([search_pattern, search_pattern2, search_pattern])
            
            # Also try to match exact start and end
            query2 = "SELECT * FROM routes WHERE is_active = 1 AND LOWER(start_point) LIKE %s AND LOWER(end_point) LIKE %s"
            params2 = [f"%{search_from.lower()}%", f"%{search_to.lower()}%"]
            
            cursor.execute(query2, params2)
            exact_matches = cursor.fetchall()
            
            if exact_matches:
                routes = exact_matches
            else:
                cursor.execute(query, params)
                routes = cursor.fetchall()
                
        elif search_from:
            # Search by starting point only
            query += " AND (LOWER(start_point) LIKE %s OR LOWER(route_name) LIKE %s)"
            search_pattern = f"%{search_from.lower()}%"
            cursor.execute(query, [search_pattern, search_pattern])
            routes = cursor.fetchall()
            
        elif search_to:
            # Search by destination only
            query += " AND (LOWER(end_point) LIKE %s OR LOWER(route_name) LIKE %s)"
            search_pattern = f"%{search_to.lower()}%"
            cursor.execute(query, [search_pattern, search_pattern])
            routes = cursor.fetchall()
            
        else:
            # No search - show all routes
            cursor.execute(query)
            routes = cursor.fetchall()
        
        # Get schedule count for each route
        for route in routes:
            cursor.execute("SELECT COUNT(*) as count FROM schedules WHERE route_id = %s AND schedule_date >= CURDATE()", (route['id'],))
            count_result = cursor.fetchone()
            route['schedule_count'] = count_result['count'] if count_result else 0
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error loading routes: {e}")
        routes = []
        flash('Error loading routes. Please try again.', 'error')
    
    return render_template('customer_routes.html', 
                          routes=routes, 
                          search_from=search_from, 
                          search_to=search_to)

@app.route('/customer/bookings', methods=['GET', 'POST'])
@permission_required('book_tickets')
def customer_bookings():
    customer_id = session.get('user_id')
    
    if request.method == 'POST':
        schedule_id = request.form.get('schedule_id')
        passenger_count = request.form.get('passenger_count', 1)
        travel_date = request.form.get('travel_date')
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT s.*, r.base_fare FROM schedules s JOIN routes r ON s.route_id=r.id WHERE s.id=%s", (schedule_id,))
            schedule = cursor.fetchone()
            
            if schedule:
                total_fare = float(schedule.get('base_fare', 0)) * int(passenger_count)
                cursor.execute("INSERT INTO bookings (customer_id, schedule_id, travel_date, passenger_count, total_fare, status) VALUES (%s, %s, %s, %s, %s, 'confirmed')",
                              (customer_id, schedule_id, travel_date, passenger_count, total_fare))
                conn.commit()
                create_notification(customer_id, 'Booking Confirmed', f'Your booking has been confirmed. Total fare: Rs. {total_fare}', 'booking')
                flash(f'Booking confirmed! Total: Rs. {total_fare}', 'success')
            else:
                flash('Schedule not found!', 'error')
            cursor.close()
            conn.close()
        except Exception as e:
            flash(f'Booking error: {str(e)}', 'error')
        return redirect(url_for('customer_bookings'))
    
    bookings = []
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT b.*, r.route_name, r.start_point, r.end_point, s.departure_time, s.arrival_time, s.schedule_date, v.registration_number
                       FROM bookings b 
                       JOIN schedules s ON b.schedule_id=s.id 
                       JOIN routes r ON s.route_id=r.id 
                       JOIN vehicles v ON s.vehicle_id=v.id
                       WHERE b.customer_id=%s 
                       ORDER BY b.booking_date DESC""", (customer_id,))
        bookings = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        bookings = []
    return render_template('customer_bookings.html', bookings=bookings)

@app.route('/customer/bookings/cancel', methods=['POST'])
@permission_required('cancel_own_bookings')
def customer_cancel_booking():
    booking_id = request.form.get('booking_id')
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE bookings SET status='cancelled' WHERE id=%s AND customer_id=%s",
                      (booking_id, session.get('user_id')))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Booking cancelled successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('customer_bookings'))

@app.route('/customer/schedules')
# @permission_required('view_schedules')
def customer_schedules():
    
    """Customer view schedules - Allow all logged in customers"""
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    schedules = []
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.*, r.route_name, r.start_point, r.end_point, r.total_distance, r.base_fare,
                   v.registration_number, v.seating_capacity,
                   CONCAT(d.first_name,' ',d.last_name) as driver_name
            FROM schedules s
            JOIN routes r ON s.route_id = r.id
            JOIN vehicles v ON s.vehicle_id = v.id
            JOIN users d ON s.driver_id = d.id
            WHERE s.schedule_date >= CURDATE() 
            AND s.status IN ('scheduled', 'on_time')
            ORDER BY s.schedule_date ASC, s.departure_time ASC
            LIMIT 20
        """)
        schedules = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error loading schedules: {e}")
        schedules = []
    
    return render_template('customer_schedules.html', schedules=schedules)
    # schedules = []
    # try:
    #     conn = get_db()
    #     cursor = conn.cursor()
    #     cursor.execute("""SELECT s.*, r.route_name, r.start_point, r.end_point, r.total_distance, r.base_fare,
    #                    v.registration_number, v.seating_capacity,
    #                    CONCAT(d.first_name,' ',d.last_name) as driver_name
    #                    FROM schedules s
    #                    JOIN routes r ON s.route_id = r.id
    #                    JOIN vehicles v ON s.vehicle_id = v.id
    #                    JOIN users d ON s.driver_id = d.id
    #                    WHERE s.schedule_date >= CURDATE() AND s.status IN ('scheduled', 'on_time')
    #                    ORDER BY s.schedule_date, s.departure_time""")
    #     schedules = cursor.fetchall()
    #     cursor.close()
    #     conn.close()
    # except:
    #     schedules = []
    # return render_template('customer_schedules.html', schedules=schedules)

@app.route('/customer/track')
@permission_required('track_buses')
def customer_track():
    return render_template('customer_track.html')

@app.route('/customer/track-schedule/<int:schedule_id>')
@permission_required('track_buses')
def customer_track_schedule(schedule_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.*, r.route_name, r.start_point, r.end_point, r.total_distance,
                   v.registration_number, v.vehicle_code,
                   CONCAT(d.first_name, ' ', d.last_name) as driver_name
            FROM schedules s
            JOIN routes r ON s.route_id = r.id
            JOIN vehicles v ON s.vehicle_id = v.id
            JOIN users d ON s.driver_id = d.id
            WHERE s.id = %s
        """, (schedule_id,))
        schedule = cursor.fetchone()
        cursor.close()
        conn.close()
        if not schedule:
            flash('Schedule not found!', 'error')
            return redirect(url_for('customer_schedules'))
        return render_template('customer_track_schedule.html', schedule=schedule)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('customer_schedules'))

@app.route('/customer/profile', methods=['GET', 'POST'])
@permission_required('update_profile')
def customer_profile():
    customer_id = session.get('user_id')
    
    if request.method == 'POST':
        phone = request.form.get('phone')
        address = request.form.get('address')
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET phone=%s, address=%s WHERE id=%s", (phone, address, customer_id))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('customer_profile'))
    
    user = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (customer_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
    except:
        user = None
    return render_template('customer_profile.html', user=user)

@app.route('/customer/history')
@permission_required('view_own_bookings')
def customer_history():
    bookings = []
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT b.*, r.route_name, r.start_point, r.end_point, s.departure_time, s.schedule_date
                       FROM bookings b 
                       JOIN schedules s ON b.schedule_id=s.id 
                       JOIN routes r ON s.route_id=r.id 
                       WHERE b.customer_id=%s AND b.status IN ('completed', 'cancelled')
                       ORDER BY b.booking_date DESC LIMIT 20""", (session.get('user_id'),))
        bookings = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        bookings = []
    return render_template('customer_history.html', bookings=bookings)

@app.route('/customer/support', methods=['GET', 'POST'])
@permission_required('create_tickets')
def customer_support():
    if request.method == 'POST':
        subject = request.form.get('subject')
        message = request.form.get('message')
        ticket_number = generate_ticket_number()
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO support_tickets (user_id, ticket_number, subject, message, status, priority) VALUES (%s, %s, %s, %s, 'open', 'normal')",
                          (session.get('user_id'), ticket_number, subject, message))
            conn.commit()
            cursor.close()
            conn.close()
            flash(f'Ticket #{ticket_number} created successfully! We will respond shortly.', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('customer_support'))
    
    tickets = []
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM support_tickets WHERE user_id=%s ORDER BY created_at DESC", (session.get('user_id'),))
        tickets = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        tickets = []
    return render_template('customer_support.html', tickets=tickets)

# ============ API ENDPOINTS ============

@app.route('/api/active-buses')
def api_active_buses():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT dl.*, u.first_name, u.last_name,
                   COALESCE(r.route_name, CONCAT('Route ', dl.driver_id)) as route_name,
                   COALESCE(r.start_point, 'Current Location') as start_point,
                   COALESCE(r.end_point, 'Destination') as end_point,
                   COALESCE(v.registration_number, CONCAT('BUS-', dl.driver_id)) as vehicle
            FROM driver_locations dl 
            JOIN users u ON dl.driver_id = u.id 
            LEFT JOIN schedules s ON dl.schedule_id = s.id 
            LEFT JOIN routes r ON s.route_id = r.id 
            LEFT JOIN vehicles v ON s.vehicle_id = v.id 
            WHERE dl.updated_at >= DATE_SUB(NOW(), INTERVAL 30 MINUTE)
            ORDER BY dl.updated_at DESC
        """)
        locations = cursor.fetchall()
        cursor.close()
        conn.close()
        
        buses = []
        for loc in locations:
            buses.append({
                'driver_id': loc['driver_id'],
                'driver_name': f"{loc['first_name']} {loc['last_name']}",
                'route_name': loc['route_name'] or f'Route {loc["driver_id"]}',
                'from': loc['start_point'] or 'Current Location',
                'to': loc['end_point'] or 'Destination',
                'vehicle': loc['vehicle'] or f'BUS-{loc["driver_id"]}',
                'latitude': float(loc['latitude']),
                'longitude': float(loc['longitude']),
                'speed': float(loc['speed']),
                'heading': loc['heading'],
                'updated_at': loc['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if loc['updated_at'] else None
            })
        return jsonify({'success': True, 'buses': buses, 'count': len(buses)})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/schedule-location/<int:schedule_id>')
def api_schedule_location(schedule_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT dl.*, u.first_name, u.last_name, r.route_name, r.start_point, r.end_point
            FROM driver_locations dl
            JOIN users u ON dl.driver_id = u.id
            LEFT JOIN schedules s ON dl.schedule_id = s.id
            LEFT JOIN routes r ON s.route_id = r.id
            WHERE dl.schedule_id = %s
            ORDER BY dl.updated_at DESC LIMIT 1
        """, (schedule_id,))
        location = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if location:
            return jsonify({
                'success': True,
                'location': {
                    'driver_name': f"{location['first_name']} {location['last_name']}",
                    'route_name': location['route_name'],
                    'from': location['start_point'],
                    'to': location['end_point'],
                    'latitude': float(location['latitude']),
                    'longitude': float(location['longitude']),
                    'speed': float(location['speed']),
                    'heading': location['heading'],
                    'updated_at': location['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if location['updated_at'] else None
                }
            })
        else:
            return jsonify({'success': True, 'no_location': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/today-schedules-status')
def api_today_schedules_status():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM schedules WHERE schedule_date = CURDATE()")
        total = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as completed FROM schedules WHERE schedule_date = CURDATE() AND status IN ('completed', 'on_time')")
        completed = cursor.fetchone()['completed']
        cursor.close()
        conn.close()
        return jsonify({'total': total, 'completed': completed})
    except:
        return jsonify({'total': 0, 'completed': 0})

@app.route('/api/recent-tickets')
def api_recent_tickets():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.*, CONCAT(u.first_name,' ',u.last_name) as user_name 
            FROM support_tickets t 
            JOIN users u ON t.user_id = u.id 
            ORDER BY t.created_at DESC LIMIT 5
        """)
        tickets = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({'tickets': tickets})
    except:
        return jsonify({'tickets': []})

# ============ LIVE TRACKING PAGE (All Roles) ============

@app.route('/live-track')
def live_track():
    """Live bus tracking page for all roles - Admin, Depot Manager, Supervisor, Customer"""
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    return render_template('customer_track.html')

# ============ TEST ENDPOINTS FOR BUS MOVEMENT ============

@app.route('/test/start-bus-simulation/<int:schedule_id>', methods=['GET'])
def start_bus_simulation(schedule_id):
    def move_bus():
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.start_point, r.end_point, r.total_distance, s.driver_id
                FROM schedules s
                JOIN routes r ON s.route_id = r.id
                WHERE s.id = %s
            """, (schedule_id,))
            route = cursor.fetchone()
            if not route:
                return
            start_coords = get_coordinates_from_name(route['start_point'])
            end_coords = get_coordinates_from_name(route['end_point'])
            steps = 50
            lat_step = (end_coords[0] - start_coords[0]) / steps
            lng_step = (end_coords[1] - start_coords[1]) / steps
            for i in range(steps + 1):
                current_lat = start_coords[0] + (lat_step * i)
                current_lng = start_coords[1] + (lng_step * i)
                speed = random.randint(40, 80)
                cursor.execute("SELECT id FROM driver_locations WHERE driver_id=%s AND schedule_id=%s", 
                              (route['driver_id'], schedule_id))
                if cursor.fetchone():
                    cursor.execute("UPDATE driver_locations SET latitude=%s, longitude=%s, speed=%s, updated_at=NOW() WHERE driver_id=%s AND schedule_id=%s",
                                  (current_lat, current_lng, speed, route['driver_id'], schedule_id))
                else:
                    cursor.execute("INSERT INTO driver_locations (driver_id, schedule_id, latitude, longitude, speed, heading) VALUES (%s, %s, %s, %s, %s, 'NE')",
                                  (route['driver_id'], schedule_id, current_lat, current_lng, speed))
                conn.commit()
                time.sleep(2)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Simulation error: {e}")
    thread = threading.Thread(target=move_bus)
    thread.daemon = True
    thread.start()
    return jsonify({'success': True, 'message': 'Bus simulation started!'})

@app.route('/test/reset-bus-position/<int:schedule_id>', methods=['GET'])
def reset_bus_position(schedule_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.start_point, s.driver_id
            FROM schedules s
            JOIN routes r ON s.route_id = r.id
            WHERE s.id = %s
        """, (schedule_id,))
        schedule = cursor.fetchone()
        if schedule:
            start_coords = get_coordinates_from_name(schedule['start_point'])
            cursor.execute("UPDATE driver_locations SET latitude=%s, longitude=%s, speed=0, updated_at=NOW() WHERE schedule_id=%s",
                          (start_coords[0], start_coords[1], schedule_id))
            conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Bus reset to start position'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/test/move-bus-step/<int:schedule_id>', methods=['GET'])
def move_bus_step(schedule_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.start_point, r.end_point, s.driver_id
            FROM schedules s
            JOIN routes r ON s.route_id = r.id
            WHERE s.id = %s
        """, (schedule_id,))
        route = cursor.fetchone()
        if not route:
            return jsonify({'success': False, 'message': 'Route not found'})
        start_coords = get_coordinates_from_name(route['start_point'])
        end_coords = get_coordinates_from_name(route['end_point'])
        cursor.execute("SELECT latitude, longitude FROM driver_locations WHERE schedule_id=%s ORDER BY updated_at DESC LIMIT 1", (schedule_id,))
        current = cursor.fetchone()
        if current:
            new_lat = float(current['latitude']) + (end_coords[0] - start_coords[0]) / 50
            new_lng = float(current['longitude']) + (end_coords[1] - start_coords[1]) / 50
            speed = random.randint(40, 80)
            cursor.execute("UPDATE driver_locations SET latitude=%s, longitude=%s, speed=%s, updated_at=NOW() WHERE schedule_id=%s",
                          (new_lat, new_lng, speed, schedule_id))
        else:
            cursor.execute("INSERT INTO driver_locations (driver_id, schedule_id, latitude, longitude, speed, heading) VALUES (%s, %s, %s, %s, %s, 'NE')",
                          (route['driver_id'], schedule_id, start_coords[0], start_coords[1], 0))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Bus moved one step'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# ============ WEEKLY AND MONTHLY REPORTS ============

@app.route('/admin/reports/weekly')
@permission_required('view_all_reports')
def admin_reports_weekly():
    """Weekly Report - Monday to Sunday of current week"""
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    return get_report_data(start_of_week, end_of_week, 'weekly')

@app.route('/admin/reports/monthly')
@permission_required('view_all_reports')
def admin_reports_monthly():
    """Monthly Report - Current month"""
    today = datetime.now().date()
    start_date = today.replace(day=1)
    
    if today.month == 12:
        end_date = today.replace(year=today.year+1, month=1, day=1) - timedelta(days=1)
    else:
        end_date = today.replace(month=today.month+1, day=1) - timedelta(days=1)
    
    return get_report_data(start_date, end_date, 'monthly')

def get_report_data(start_date, end_date, report_type):
    """Helper function to get report data for a date range"""
    stats = {}
    monthly_trends = []
    route_performance = []
    fuel_trends = []
    driver_performance = []
    vehicle_efficiency = []
    
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Summary statistics
        cursor.execute("SELECT COUNT(*) as c FROM routes WHERE is_active=1")
        stats['total_routes'] = cursor.fetchone()['c']
        
        cursor.execute("SELECT COUNT(*) as c FROM vehicles")
        stats['total_vehicles'] = cursor.fetchone()['c']
        
        cursor.execute("SELECT COUNT(*) as c FROM users WHERE role='driver' AND is_active=1")
        stats['active_drivers'] = cursor.fetchone()['c']
        
        cursor.execute("SELECT COUNT(*) as c FROM users WHERE role='customer'")
        stats['total_customers'] = cursor.fetchone()['c']
        
        # Performance for selected period
        cursor.execute("""
            SELECT 
                COUNT(*) as total_trips,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_trips,
                SUM(CASE WHEN status = 'on_time' THEN 1 ELSE 0 END) as on_time_trips,
                SUM(CASE WHEN status = 'delayed' THEN 1 ELSE 0 END) as delayed_trips,
                SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled_trips
            FROM schedules 
            WHERE schedule_date BETWEEN %s AND %s
        """, (start_date_str, end_date_str))
        period_data = cursor.fetchone()
        
        stats['total_trips'] = period_data['total_trips'] or 0
        stats['completed_trips'] = period_data['completed_trips'] or 0
        stats['on_time_trips'] = period_data['on_time_trips'] or 0
        stats['delayed_trips'] = period_data['delayed_trips'] or 0
        stats['cancelled_trips'] = period_data['cancelled_trips'] or 0
        
        if stats['total_trips'] > 0:
            stats['completion_rate'] = round((stats['completed_trips'] / stats['total_trips']) * 100)
            stats['on_time_rate'] = round((stats['on_time_trips'] / stats['total_trips']) * 100)
            stats['delayed_rate'] = round((stats['delayed_trips'] / stats['total_trips']) * 100)
            stats['cancelled_rate'] = round((stats['cancelled_trips'] / stats['total_trips']) * 100)
        else:
            stats['completion_rate'] = stats['on_time_rate'] = stats['delayed_rate'] = stats['cancelled_rate'] = 0
        
        # Monthly trends (last 6 months)
        cursor.execute("""
            SELECT 
                DATE_FORMAT(schedule_date, '%%Y-%%m') as month,
                COUNT(*) as total_trips,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_trips
            FROM schedules 
            WHERE schedule_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(schedule_date, '%%Y-%%m')
            ORDER BY month ASC
        """)
        monthly_trends = cursor.fetchall()
        
        # Route performance
        cursor.execute("""
            SELECT 
                r.route_name,
                r.route_code,
                r.total_distance,
                COUNT(s.id) as total_trips,
                SUM(CASE WHEN s.status = 'completed' THEN 1 ELSE 0 END) as completed_trips,
                SUM(CASE WHEN s.status = 'on_time' THEN 1 ELSE 0 END) as on_time_trips,
                SUM(CASE WHEN s.status = 'delayed' THEN 1 ELSE 0 END) as delayed_trips,
                ROUND(IFNULL(SUM(CASE WHEN s.status = 'on_time' THEN 1 ELSE 0 END) / NULLIF(COUNT(s.id), 0) * 100, 0), 1) as reliability_score
            FROM routes r
            LEFT JOIN schedules s ON r.id = s.route_id AND s.schedule_date BETWEEN %s AND %s
            GROUP BY r.id
            ORDER BY reliability_score DESC
        """, (start_date_str, end_date_str))
        route_performance = cursor.fetchall()
        
        # Fuel trends
        cursor.execute("""
            SELECT 
                DATE_FORMAT(fuel_date, '%%Y-%%m') as month,
                SUM(fuel_liters) as total_liters,
                SUM(total_cost) as total_cost
            FROM fuel_logs 
            WHERE fuel_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(fuel_date, '%%Y-%%m')
            ORDER BY month ASC
        """)
        fuel_trends = cursor.fetchall()
        
        # Driver performance - FIXED
        cursor.execute("""
            SELECT 
                TRIM(CONCAT(COALESCE(u.first_name, ''), ' ', COALESCE(u.last_name, ''))) as driver_name,
                COUNT(s.id) as total_trips,
                SUM(CASE WHEN s.status = 'completed' THEN 1 ELSE 0 END) as completed_trips,
                SUM(CASE WHEN s.status = 'on_time' THEN 1 ELSE 0 END) as on_time_trips,
                SUM(CASE WHEN s.status = 'delayed' THEN 1 ELSE 0 END) as delayed_trips,
                ROUND(IFNULL(SUM(CASE WHEN s.status = 'on_time' THEN 1 ELSE 0 END) / NULLIF(COUNT(s.id), 0) * 100, 0), 1) as punctuality_rate
            FROM users u
            LEFT JOIN schedules s ON u.id = s.driver_id 
                AND s.schedule_date BETWEEN %s AND %s
                AND s.status IS NOT NULL
            WHERE u.role = 'driver'
            GROUP BY u.id
            ORDER BY total_trips DESC, punctuality_rate DESC
        """, (start_date_str, end_date_str))
        driver_performance = cursor.fetchall()
        
        # Vehicle fuel efficiency
        cursor.execute("""
            SELECT 
                v.registration_number,
                v.vehicle_type,
                COUNT(f.id) as fuel_logs,
                SUM(f.fuel_liters) as total_fuel,
                SUM(f.total_cost) as total_cost,
                ROUND(CASE 
                    WHEN (MAX(f.odometer_reading) - MIN(f.odometer_reading)) > 0 
                    THEN SUM(f.fuel_liters) / (MAX(f.odometer_reading) - MIN(f.odometer_reading)) * 100
                    ELSE 0 
                END, 1) as fuel_efficiency
            FROM vehicles v
            LEFT JOIN fuel_logs f ON v.id = f.vehicle_id
                AND f.fuel_date BETWEEN %s AND %s
            GROUP BY v.id
            ORDER BY fuel_efficiency ASC
        """, (start_date_str, end_date_str))
        vehicle_efficiency = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Report error: {e}")
        stats = {'total_routes':0, 'total_vehicles':0, 'active_drivers':0, 'total_customers':0,
                'total_trips':0, 'completed_trips':0, 'on_time_trips':0, 'delayed_trips':0,
                'cancelled_trips':0, 'completion_rate':0, 'on_time_rate':0, 'delayed_rate':0, 'cancelled_rate':0}
    
    # Choose template based on report type
    if report_type == 'weekly':
        template = 'admin_reports_weekly.html'
    elif report_type == 'monthly':
        template = 'admin_reports_monthly.html'
    else:
        template = 'admin_reports.html'
    
    return render_template(template,
                          stats=stats,
                          monthly_trends=monthly_trends,
                          route_performance=route_performance,
                          fuel_trends=fuel_trends,
                          driver_performance=driver_performance,
                          vehicle_efficiency=vehicle_efficiency,
                          start_date=start_date_str,
                          end_date=end_date_str,
                          period=report_type)

# ============ DEPOT MANAGER ROUTE MANAGEMENT ============

@app.route('/depot-manager/routes', methods=['GET', 'POST'])
@permission_required('manage_routes')
def depot_manager_routes():
    """Depot Manager route management - Create, Read, Update, Delete routes"""
    if request.method == 'POST':
        action = request.form.get('action')
        
        # CREATE ROUTE
        if action == 'add':
            route_code = request.form.get('route_code')
            route_name = request.form.get('route_name')
            start_point = request.form.get('start_point')
            end_point = request.form.get('end_point')
            intermediate_stops = request.form.get('intermediate_stops', '')
            total_distance = request.form.get('total_distance')
            route_type = request.form.get('route_type', 'urban')
            base_fare = request.form.get('base_fare', 0)
            
            if not all([route_code, route_name, start_point, end_point, total_distance]):
                flash('Please fill all required fields!', 'error')
                return redirect(url_for('depot_manager_routes'))
            
            try:
                conn = get_db()
                cursor = conn.cursor()
                
                # Check if route code exists
                cursor.execute("SELECT id FROM routes WHERE route_code = %s", (route_code,))
                if cursor.fetchone():
                    flash('Route code already exists!', 'error')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('depot_manager_routes'))
                
                cursor.execute("""
                    INSERT INTO routes (route_code, route_name, start_point, end_point, 
                                       intermediate_stops, total_distance, route_type, base_fare, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1)
                """, (route_code, route_name, start_point, end_point, intermediate_stops, 
                      total_distance, route_type, base_fare))
                
                conn.commit()
                cursor.close()
                conn.close()
                
                flash(f'Route "{route_name}" added successfully!', 'success')
                log_user_activity(session['user_id'], f'Added route: {route_code}', request)
                
            except Exception as e:
                flash(f'Error adding route: {str(e)}', 'error')
            
            return redirect(url_for('depot_manager_routes'))
        
        # UPDATE ROUTE
        elif action == 'edit':
            route_id = request.form.get('route_id')
            route_code = request.form.get('route_code')
            route_name = request.form.get('route_name')
            start_point = request.form.get('start_point')
            end_point = request.form.get('end_point')
            intermediate_stops = request.form.get('intermediate_stops', '')
            total_distance = request.form.get('total_distance')
            route_type = request.form.get('route_type', 'urban')
            base_fare = request.form.get('base_fare', 0)
            is_active = request.form.get('is_active', 1)
            
            if not all([route_id, route_code, route_name, start_point, end_point, total_distance]):
                flash('Please fill all required fields!', 'error')
                return redirect(url_for('depot_manager_routes'))
            
            try:
                conn = get_db()
                cursor = conn.cursor()
                
                # Check if route code exists for a different route
                cursor.execute("SELECT id FROM routes WHERE route_code = %s AND id != %s", (route_code, route_id))
                if cursor.fetchone():
                    flash('Route code already exists for another route!', 'error')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('depot_manager_routes'))
                
                cursor.execute("""
                    UPDATE routes 
                    SET route_code = %s, route_name = %s, start_point = %s, end_point = %s,
                        intermediate_stops = %s, total_distance = %s, route_type = %s, 
                        base_fare = %s, is_active = %s
                    WHERE id = %s
                """, (route_code, route_name, start_point, end_point, intermediate_stops,
                      total_distance, route_type, base_fare, is_active, route_id))
                
                conn.commit()
                cursor.close()
                conn.close()
                
                flash(f'Route "{route_name}" updated successfully!', 'success')
                log_user_activity(session['user_id'], f'Updated route: {route_code} (ID: {route_id})', request)
                
            except Exception as e:
                flash(f'Error updating route: {str(e)}', 'error')
            
            return redirect(url_for('depot_manager_routes'))
        
        # DELETE ROUTE
        elif action == 'delete':
            route_id = request.form.get('route_id')
            
            if not route_id:
                flash('Invalid route ID!', 'error')
                return redirect(url_for('depot_manager_routes'))
            
            try:
                conn = get_db()
                cursor = conn.cursor()
                
                # Check if route exists
                cursor.execute("SELECT route_name FROM routes WHERE id = %s", (route_id,))
                route = cursor.fetchone()
                
                if not route:
                    flash('Route not found!', 'error')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('depot_manager_routes'))
                
                # Check if route has any schedules
                cursor.execute("SELECT COUNT(*) as count FROM schedules WHERE route_id = %s", (route_id,))
                schedule_count = cursor.fetchone()
                
                if schedule_count and schedule_count['count'] > 0:
                    flash(f'Cannot delete route "{route["route_name"]}" because it has {schedule_count["count"]} associated schedules. Archive it instead.', 'error')
                else:
                    cursor.execute("DELETE FROM routes WHERE id = %s", (route_id,))
                    conn.commit()
                    flash(f'Route "{route["route_name"]}" deleted successfully!', 'success')
                    log_user_activity(session['user_id'], f'Deleted route ID: {route_id}', request)
                
                cursor.close()
                conn.close()
                
            except Exception as e:
                flash(f'Error deleting route: {str(e)}', 'error')
            
            return redirect(url_for('depot_manager_routes'))
    
    # GET request - display routes
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM routes ORDER BY created_at DESC")
        routes = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        routes = []
        flash(f'Error loading routes: {str(e)}', 'error')
    
    return render_template('depot_manager_routes.html', routes=routes)

@app.route('/depot-manager/assign-drivers', methods=['GET', 'POST'])
@permission_required('assign_drivers')
def depot_manager_assign_drivers():
    """Depot Manager driver assignment - Assign drivers to routes and schedules"""
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        # ASSIGN DRIVER TO SCHEDULE
        if action == 'assign_to_schedule':
            schedule_id = request.form.get('schedule_id')
            driver_id = request.form.get('driver_id')
            
            if not all([schedule_id, driver_id]):
                flash('Please select both schedule and driver!', 'error')
                return redirect(url_for('depot_manager_assign_drivers'))
            
            try:
                conn = get_db()
                cursor = conn.cursor()
                
                # Get schedule details
                cursor.execute("""
                    SELECT s.*, r.route_name, s.departure_time, s.schedule_date 
                    FROM schedules s 
                    JOIN routes r ON s.route_id = r.id 
                    WHERE s.id = %s
                """, (schedule_id,))
                schedule = cursor.fetchone()
                
                if not schedule:
                    flash('Schedule not found!', 'error')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('depot_manager_assign_drivers'))
                
                # Check if driver is already assigned to another schedule at same time
                cursor.execute("""
                    SELECT id FROM schedules 
                    WHERE driver_id = %s AND schedule_date = %s 
                    AND ((departure_time <= %s AND arrival_time > %s) 
                         OR (departure_time < %s AND arrival_time >= %s))
                    AND id != %s
                """, (driver_id, schedule['schedule_date'], schedule['arrival_time'], 
                      schedule['departure_time'], schedule['arrival_time'], 
                      schedule['departure_time'], schedule_id))
                
                conflict = cursor.fetchone()
                if conflict:
                    # Get driver name
                    cursor.execute("SELECT first_name, last_name FROM users WHERE id = %s", (driver_id,))
                    driver = cursor.fetchone()
                    flash(f'Driver {driver["first_name"]} {driver["last_name"]} is already assigned to another trip at this time!', 'error')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('depot_manager_assign_drivers'))
                
                # Update schedule with new driver
                cursor.execute("UPDATE schedules SET driver_id = %s WHERE id = %s", (driver_id, schedule_id))
                conn.commit()
                
                # Get driver name for notification
                cursor.execute("SELECT first_name, last_name FROM users WHERE id = %s", (driver_id,))
                driver = cursor.fetchone()
                
                # Send notification to driver
                create_notification(driver_id, 'Driver Assignment', 
                                  f'You have been assigned to route "{schedule["route_name"]}" on {schedule["schedule_date"]} at {schedule["departure_time"]}', 
                                  'schedule')
                
                cursor.close()
                conn.close()
                
                flash(f'Driver {driver["first_name"]} {driver["last_name"]} assigned to schedule successfully!', 'success')
                log_user_activity(session['user_id'], f'Assigned driver {driver_id} to schedule {schedule_id}', request)
                
            except Exception as e:
                flash(f'Error assigning driver: {str(e)}', 'error')
            
            return redirect(url_for('depot_manager_assign_drivers'))
        
        # BULK ASSIGN DRIVERS TO MULTIPLE SCHEDULES
        elif action == 'bulk_assign':
            schedule_ids = request.form.getlist('schedule_ids')
            driver_id = request.form.get('driver_id')
            
            if not schedule_ids or not driver_id:
                flash('Please select at least one schedule and a driver!', 'error')
                return redirect(url_for('depot_manager_assign_drivers'))
            
            success_count = 0
            error_count = 0
            
            try:
                conn = get_db()
                cursor = conn.cursor()
                
                for schedule_id in schedule_ids:
                    try:
                        # Check for conflicts
                        cursor.execute("""
                            SELECT s.*, r.route_name 
                            FROM schedules s 
                            JOIN routes r ON s.route_id = r.id 
                            WHERE s.id = %s
                        """, (schedule_id,))
                        schedule = cursor.fetchone()
                        
                        if schedule:
                            # Check if driver is available
                            cursor.execute("""
                                SELECT id FROM schedules 
                                WHERE driver_id = %s AND schedule_date = %s AND id != %s
                                AND ((departure_time <= %s AND arrival_time > %s) 
                                     OR (departure_time < %s AND arrival_time >= %s))
                            """, (driver_id, schedule['schedule_date'], schedule_id, 
                                  schedule['arrival_time'], schedule['departure_time'],
                                  schedule['arrival_time'], schedule['departure_time']))
                            
                            if not cursor.fetchone():
                                cursor.execute("UPDATE schedules SET driver_id = %s WHERE id = %s", (driver_id, schedule_id))
                                conn.commit()
                                success_count += 1
                            else:
                                error_count += 1
                    except:
                        error_count += 1
                
                cursor.close()
                conn.close()
                
                # Get driver name
                conn2 = get_db()
                cursor2 = conn2.cursor()
                cursor2.execute("SELECT first_name, last_name FROM users WHERE id = %s", (driver_id,))
                driver = cursor2.fetchone()
                cursor2.close()
                conn2.close()
                
                flash(f'Successfully assigned {success_count} schedules to driver {driver["first_name"]} {driver["last_name"]}. {error_count} failed due to conflicts.', 'success')
                log_user_activity(session['user_id'], f'Bulk assigned driver {driver_id} to {success_count} schedules', request)
                
            except Exception as e:
                flash(f'Error in bulk assignment: {str(e)}', 'error')
            
            return redirect(url_for('depot_manager_assign_drivers'))
    
    # GET request - display assignment interface
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get unassigned or upcoming schedules
        cursor.execute("""
            SELECT s.*, r.route_name, r.start_point, r.end_point, r.total_distance,
                   v.registration_number, v.vehicle_code,
                   COALESCE(CONCAT(d.first_name, ' ', d.last_name), 'Not Assigned') as driver_name,
                   d.id as current_driver_id
            FROM schedules s 
            JOIN routes r ON s.route_id = r.id 
            JOIN vehicles v ON s.vehicle_id = v.id 
            LEFT JOIN users d ON s.driver_id = d.id
            WHERE s.schedule_date >= CURDATE() OR s.driver_id IS NULL
            ORDER BY s.schedule_date ASC, s.departure_time ASC
            LIMIT 50
        """)
        schedules = cursor.fetchall()
        
        # Get all active drivers
        cursor.execute("""
            SELECT id, first_name, last_name, username, phone 
            FROM users 
            WHERE role = 'driver' AND is_active = 1 
            ORDER BY first_name
        """)
        drivers = cursor.fetchall()
        
        # Get statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_schedules,
                SUM(CASE WHEN driver_id IS NULL THEN 1 ELSE 0 END) as unassigned_schedules,
                COUNT(DISTINCT driver_id) as drivers_assigned
            FROM schedules 
            WHERE schedule_date >= CURDATE()
        """)
        stats = cursor.fetchone()
        
        # Get schedules grouped by date
        cursor.execute("""
            SELECT 
                s.schedule_date,
                COUNT(*) as total,
                SUM(CASE WHEN s.driver_id IS NULL THEN 1 ELSE 0 END) as unassigned
            FROM schedules s
            WHERE s.schedule_date >= CURDATE()
            GROUP BY s.schedule_date
            ORDER BY s.schedule_date
            LIMIT 14
        """)
        date_summary = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        schedules = []
        drivers = []
        stats = {'total_schedules': 0, 'unassigned_schedules': 0, 'drivers_assigned': 0}
        date_summary = []
        flash(f'Error loading data: {str(e)}', 'error')
    
    return render_template('depot_manager_assign_drivers.html', 
                          schedules=schedules, 
                          drivers=drivers, 
                          stats=stats,
                          date_summary=date_summary)

# ============ DEPOT MANAGER VEHICLE MANAGEMENT ============

@app.route('/depot-manager/vehicles', methods=['GET', 'POST'])
@permission_required('manage_vehicles')
def depot_manager_vehicles():
    """Depot Manager vehicle management - Create, Read, Update vehicles"""
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        # CREATE VEHICLE
        if action == 'add':
            vehicle_code = request.form.get('vehicle_code')
            registration_number = request.form.get('registration_number')
            vehicle_type = request.form.get('vehicle_type', 'standard')
            seating_capacity = request.form.get('seating_capacity')
            fuel_type = request.form.get('fuel_type', 'diesel')
            status = request.form.get('status', 'available')
            
            if not all([vehicle_code, registration_number, seating_capacity]):
                flash('Please fill all required fields!', 'error')
                return redirect(url_for('depot_manager_vehicles'))
            
            try:
                conn = get_db()
                cursor = conn.cursor()
                
                # Check if vehicle code exists
                cursor.execute("SELECT id FROM vehicles WHERE vehicle_code = %s", (vehicle_code,))
                if cursor.fetchone():
                    flash('Vehicle code already exists!', 'error')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('depot_manager_vehicles'))
                
                # Check if registration number exists
                cursor.execute("SELECT id FROM vehicles WHERE registration_number = %s", (registration_number,))
                if cursor.fetchone():
                    flash('Registration number already exists!', 'error')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('depot_manager_vehicles'))
                
                cursor.execute("""
                    INSERT INTO vehicles (vehicle_code, registration_number, vehicle_type, 
                                         seating_capacity, fuel_type, status) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (vehicle_code, registration_number, vehicle_type, 
                      seating_capacity, fuel_type, status))
                
                conn.commit()
                cursor.close()
                conn.close()
                
                flash(f'Vehicle "{vehicle_code}" added successfully!', 'success')
                log_user_activity(session['user_id'], f'Added vehicle: {vehicle_code}', request)
                
            except Exception as e:
                flash(f'Error adding vehicle: {str(e)}', 'error')
            
            return redirect(url_for('depot_manager_vehicles'))
        
        # UPDATE VEHICLE
        elif action == 'edit':
            vehicle_id = request.form.get('vehicle_id')
            vehicle_code = request.form.get('vehicle_code')
            registration_number = request.form.get('registration_number')
            vehicle_type = request.form.get('vehicle_type', 'standard')
            seating_capacity = request.form.get('seating_capacity')
            fuel_type = request.form.get('fuel_type', 'diesel')
            status = request.form.get('status', 'available')
            
            if not all([vehicle_id, vehicle_code, registration_number, seating_capacity]):
                flash('Please fill all required fields!', 'error')
                return redirect(url_for('depot_manager_vehicles'))
            
            try:
                conn = get_db()
                cursor = conn.cursor()
                
                # Check if vehicle code exists for a different vehicle
                cursor.execute("SELECT id FROM vehicles WHERE vehicle_code = %s AND id != %s", (vehicle_code, vehicle_id))
                if cursor.fetchone():
                    flash('Vehicle code already exists for another vehicle!', 'error')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('depot_manager_vehicles'))
                
                # Check if registration number exists for a different vehicle
                cursor.execute("SELECT id FROM vehicles WHERE registration_number = %s AND id != %s", (registration_number, vehicle_id))
                if cursor.fetchone():
                    flash('Registration number already exists for another vehicle!', 'error')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('depot_manager_vehicles'))
                
                cursor.execute("""
                    UPDATE vehicles 
                    SET vehicle_code = %s, registration_number = %s, vehicle_type = %s,
                        seating_capacity = %s, fuel_type = %s, status = %s
                    WHERE id = %s
                """, (vehicle_code, registration_number, vehicle_type, seating_capacity, fuel_type, status, vehicle_id))
                
                conn.commit()
                cursor.close()
                conn.close()
                
                flash(f'Vehicle "{vehicle_code}" updated successfully!', 'success')
                log_user_activity(session['user_id'], f'Updated vehicle: {vehicle_code} (ID: {vehicle_id})', request)
                
            except Exception as e:
                flash(f'Error updating vehicle: {str(e)}', 'error')
            
            return redirect(url_for('depot_manager_vehicles'))
        
        # DELETE VEHICLE
        elif action == 'delete':
            vehicle_id = request.form.get('vehicle_id')
            
            if not vehicle_id:
                flash('Invalid vehicle ID!', 'error')
                return redirect(url_for('depot_manager_vehicles'))
            
            try:
                conn = get_db()
                cursor = conn.cursor()
                
                # Check if vehicle exists
                cursor.execute("SELECT vehicle_code FROM vehicles WHERE id = %s", (vehicle_id,))
                vehicle = cursor.fetchone()
                
                if not vehicle:
                    flash('Vehicle not found!', 'error')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('depot_manager_vehicles'))
                
                # Check if vehicle has any schedules
                cursor.execute("SELECT COUNT(*) as count FROM schedules WHERE vehicle_id = %s", (vehicle_id,))
                schedule_count = cursor.fetchone()
                
                if schedule_count and schedule_count['count'] > 0:
                    # Instead of deleting, mark as maintenance
                    cursor.execute("UPDATE vehicles SET status = 'maintenance' WHERE id = %s", (vehicle_id,))
                    conn.commit()
                    flash(f'Vehicle "{vehicle["vehicle_code"]}" has active schedules. Status changed to Maintenance instead.', 'warning')
                else:
                    cursor.execute("DELETE FROM vehicles WHERE id = %s", (vehicle_id,))
                    conn.commit()
                    flash(f'Vehicle "{vehicle["vehicle_code"]}" deleted successfully!', 'success')
                    log_user_activity(session['user_id'], f'Deleted vehicle ID: {vehicle_id}', request)
                
                cursor.close()
                conn.close()
                
            except Exception as e:
                flash(f'Error deleting vehicle: {str(e)}', 'error')
            
            return redirect(url_for('depot_manager_vehicles'))
    
    # GET request - display vehicles
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get all vehicles
        cursor.execute("SELECT * FROM vehicles ORDER BY created_at DESC")
        vehicles = cursor.fetchall()
        
        # Get vehicle statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'available' THEN 1 ELSE 0 END) as available,
                SUM(CASE WHEN status = 'in_use' THEN 1 ELSE 0 END) as in_use,
                SUM(CASE WHEN status = 'maintenance' THEN 1 ELSE 0 END) as maintenance
            FROM vehicles
        """)
        stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        vehicles = []
        stats = {'total': 0, 'available': 0, 'in_use': 0, 'maintenance': 0}
        flash(f'Error loading vehicles: {str(e)}', 'error')
    
    return render_template('depot_manager_vehicles.html', vehicles=vehicles, stats=stats)

@app.route('/depot-manager/assign-vehicles', methods=['GET', 'POST'])
@permission_required('assign_vehicles')
def depot_manager_assign_vehicles():
    """Depot Manager vehicle assignment - Assign vehicles to schedules"""
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        # ASSIGN VEHICLE TO SCHEDULE
        if action == 'assign_to_schedule':
            schedule_id = request.form.get('schedule_id')
            vehicle_id = request.form.get('vehicle_id')
            
            if not all([schedule_id, vehicle_id]):
                flash('Please select both schedule and vehicle!', 'error')
                return redirect(url_for('depot_manager_assign_vehicles'))
            
            try:
                conn = get_db()
                cursor = conn.cursor()
                
                # Get schedule details
                cursor.execute("""
                    SELECT s.*, r.route_name, s.departure_time, s.schedule_date 
                    FROM schedules s 
                    JOIN routes r ON s.route_id = r.id 
                    WHERE s.id = %s
                """, (schedule_id,))
                schedule = cursor.fetchone()
                
                if not schedule:
                    flash('Schedule not found!', 'error')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('depot_manager_assign_vehicles'))
                
                # Check if vehicle is already assigned to another schedule at same time
                cursor.execute("""
                    SELECT id FROM schedules 
                    WHERE vehicle_id = %s AND schedule_date = %s 
                    AND ((departure_time <= %s AND arrival_time > %s) 
                         OR (departure_time < %s AND arrival_time >= %s))
                    AND id != %s
                """, (vehicle_id, schedule['schedule_date'], schedule['arrival_time'], 
                      schedule['departure_time'], schedule['arrival_time'], 
                      schedule['departure_time'], schedule_id))
                
                conflict = cursor.fetchone()
                if conflict:
                    # Get vehicle name
                    cursor.execute("SELECT vehicle_code, registration_number FROM vehicles WHERE id = %s", (vehicle_id,))
                    vehicle = cursor.fetchone()
                    flash(f'Vehicle {vehicle["vehicle_code"]} is already assigned to another trip at this time!', 'error')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('depot_manager_assign_vehicles'))
                
                # Get old vehicle_id to update status
                cursor.execute("SELECT vehicle_id FROM schedules WHERE id = %s", (schedule_id,))
                old_data = cursor.fetchone()
                old_vehicle_id = old_data['vehicle_id'] if old_data else None
                
                # Update schedule with new vehicle
                cursor.execute("UPDATE schedules SET vehicle_id = %s WHERE id = %s", (vehicle_id, schedule_id))
                conn.commit()
                
                # Update vehicle statuses
                if old_vehicle_id and old_vehicle_id != int(vehicle_id):
                    # Check if old vehicle has any other schedules today
                    cursor.execute("""
                        SELECT id FROM schedules 
                        WHERE vehicle_id = %s AND schedule_date = %s AND id != %s
                    """, (old_vehicle_id, schedule['schedule_date'], schedule_id))
                    if not cursor.fetchone():
                        cursor.execute("UPDATE vehicles SET status = 'available' WHERE id = %s", (old_vehicle_id,))
                        conn.commit()
                
                # Update new vehicle status to in_use
                cursor.execute("UPDATE vehicles SET status = 'in_use' WHERE id = %s", (vehicle_id,))
                conn.commit()
                
                # Get vehicle name for notification
                cursor.execute("SELECT vehicle_code, registration_number FROM vehicles WHERE id = %s", (vehicle_id,))
                vehicle = cursor.fetchone()
                
                cursor.close()
                conn.close()
                
                flash(f'Vehicle {vehicle["vehicle_code"]} ({vehicle["registration_number"]}) assigned to schedule successfully!', 'success')
                log_user_activity(session['user_id'], f'Assigned vehicle {vehicle_id} to schedule {schedule_id}', request)
                
            except Exception as e:
                flash(f'Error assigning vehicle: {str(e)}', 'error')
            
            return redirect(url_for('depot_manager_assign_vehicles'))
        
        # BULK ASSIGN VEHICLES
        elif action == 'bulk_assign':
            schedule_ids = request.form.getlist('schedule_ids')
            vehicle_id = request.form.get('vehicle_id')
            
            if not schedule_ids or not vehicle_id:
                flash('Please select at least one schedule and a vehicle!', 'error')
                return redirect(url_for('depot_manager_assign_vehicles'))
            
            success_count = 0
            error_count = 0
            
            try:
                conn = get_db()
                cursor = conn.cursor()
                
                for schedule_id in schedule_ids:
                    try:
                        # Get schedule details
                        cursor.execute("""
                            SELECT s.*, r.route_name 
                            FROM schedules s 
                            JOIN routes r ON s.route_id = r.id 
                            WHERE s.id = %s
                        """, (schedule_id,))
                        schedule = cursor.fetchone()
                        
                        if schedule:
                            # Check if vehicle is available
                            cursor.execute("""
                                SELECT id FROM schedules 
                                WHERE vehicle_id = %s AND schedule_date = %s AND id != %s
                                AND ((departure_time <= %s AND arrival_time > %s) 
                                     OR (departure_time < %s AND arrival_time >= %s))
                            """, (vehicle_id, schedule['schedule_date'], schedule_id, 
                                  schedule['arrival_time'], schedule['departure_time'],
                                  schedule['arrival_time'], schedule['departure_time']))
                            
                            if not cursor.fetchone():
                                # Get old vehicle_id
                                cursor.execute("SELECT vehicle_id FROM schedules WHERE id = %s", (schedule_id,))
                                old_data = cursor.fetchone()
                                old_vehicle_id = old_data['vehicle_id'] if old_data else None
                                
                                cursor.execute("UPDATE schedules SET vehicle_id = %s WHERE id = %s", (vehicle_id, schedule_id))
                                conn.commit()
                                
                                # Update old vehicle status if needed
                                if old_vehicle_id and old_vehicle_id != int(vehicle_id):
                                    cursor.execute("""
                                        SELECT id FROM schedules 
                                        WHERE vehicle_id = %s AND schedule_date = %s AND id != %s
                                    """, (old_vehicle_id, schedule['schedule_date'], schedule_id))
                                    if not cursor.fetchone():
                                        cursor.execute("UPDATE vehicles SET status = 'available' WHERE id = %s", (old_vehicle_id,))
                                        conn.commit()
                                
                                success_count += 1
                            else:
                                error_count += 1
                    except:
                        error_count += 1
                
                # Update new vehicle status
                cursor.execute("UPDATE vehicles SET status = 'in_use' WHERE id = %s", (vehicle_id,))
                conn.commit()
                
                cursor.close()
                conn.close()
                
                # Get vehicle name
                conn2 = get_db()
                cursor2 = conn2.cursor()
                cursor2.execute("SELECT vehicle_code, registration_number FROM vehicles WHERE id = %s", (vehicle_id,))
                vehicle = cursor2.fetchone()
                cursor2.close()
                conn2.close()
                
                flash(f'Successfully assigned {success_count} schedules to vehicle {vehicle["vehicle_code"]}. {error_count} failed due to conflicts.', 'success')
                log_user_activity(session['user_id'], f'Bulk assigned vehicle {vehicle_id} to {success_count} schedules', request)
                
            except Exception as e:
                flash(f'Error in bulk assignment: {str(e)}', 'error')
            
            return redirect(url_for('depot_manager_assign_vehicles'))
    
    # GET request - display assignment interface
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get schedules needing vehicles (upcoming or unassigned)
        cursor.execute("""
            SELECT s.*, r.route_name, r.start_point, r.end_point, r.total_distance,
                   v.registration_number as current_vehicle_number, v.vehicle_code as current_vehicle_code,
                   COALESCE(CONCAT(d.first_name, ' ', d.last_name), 'Not Assigned') as driver_name
            FROM schedules s 
            JOIN routes r ON s.route_id = r.id 
            LEFT JOIN vehicles v ON s.vehicle_id = v.id
            LEFT JOIN users d ON s.driver_id = d.id
            WHERE s.schedule_date >= CURDATE() OR s.vehicle_id IS NULL
            ORDER BY s.schedule_date ASC, s.departure_time ASC
            LIMIT 50
        """)
        schedules = cursor.fetchall()
        
        # Get all available vehicles (not in maintenance)
        cursor.execute("""
            SELECT id, vehicle_code, registration_number, vehicle_type, seating_capacity, status
            FROM vehicles 
            WHERE status != 'maintenance'
            ORDER BY vehicle_code
        """)
        vehicles = cursor.fetchall()
        
        # Get statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_schedules,
                SUM(CASE WHEN vehicle_id IS NULL THEN 1 ELSE 0 END) as unassigned_schedules,
                COUNT(DISTINCT vehicle_id) as vehicles_assigned
            FROM schedules 
            WHERE schedule_date >= CURDATE()
        """)
        stats = cursor.fetchone()
        
        # Get vehicle status summary
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'available' THEN 1 ELSE 0 END) as available,
                SUM(CASE WHEN status = 'in_use' THEN 1 ELSE 0 END) as in_use,
                SUM(CASE WHEN status = 'maintenance' THEN 1 ELSE 0 END) as maintenance
            FROM vehicles
        """)
        vehicle_stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        schedules = []
        vehicles = []
        stats = {'total_schedules': 0, 'unassigned_schedules': 0, 'vehicles_assigned': 0}
        vehicle_stats = {'total': 0, 'available': 0, 'in_use': 0, 'maintenance': 0}
        flash(f'Error loading data: {str(e)}', 'error')
    
    return render_template('depot_manager_assign_vehicles.html', 
                          schedules=schedules, 
                          vehicles=vehicles, 
                          stats=stats,
                          vehicle_stats=vehicle_stats)

if __name__ == '__main__':
    print("=" * 60)
    print("🚍 SRMSS Server Starting...")
    print("=" * 60)

    print("Access the application at: http://127.0.0.1:5000")
    print("-" * 60)
    print("👤 Login Credentials:")
    print("   • Admin: username='admin', password='admin123'")
    print("   • Depot Manager: username='manager', password='manager123'")
    print("   • Supervisor: username='supervisor', password='supervisor123'")
    print("   • Driver: username='rishu', password='rishu123'")
    print("   • Customer: username='binidu', password='binidu123'")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5000)