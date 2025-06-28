from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'supermarket_secret_key_2024'

# Items and their prices (corrected spelling: Paneer)
items = {
    'rice': 50,
    'sugar': 30,
    'salt': 20,
    'oil': 110,
    'paneer': 400,
    'maggi': 80,
    'boost': 90,
    'colgate': 85,
    'soap': 20
}

# Item display list for UI
item_list = '''Rice     Rs 50/kg
Sugar    Rs 30/kg
Salt     Rs 20/kg
Oil      Rs 110/liter
Paneer   Rs 400/kg
Maggi    Rs 80/each
Boost    Rs 90/each
Colgate  Rs 85/each
Soap     Rs 20/each'''

@app.route('/')
def home():
    """Home page - Enter customer name"""
    return render_template('home.html', item_list=item_list)

@app.route('/start_shopping', methods=['POST'])
def start_shopping():
    """Initialize shopping session"""
    name = request.form.get('name', '').strip()
    if not name:
        flash('Please enter your name', 'error')
        return redirect(url_for('home'))
    
    # Initialize session variables
    session['customer_name'] = name
    session['cart'] = []
    session['total_price'] = 0
    session['shopping_active'] = True
    
    return redirect(url_for('shopping'))

@app.route('/shopping')
def shopping():
    """Main shopping interface"""
    if not session.get('shopping_active'):
        return redirect(url_for('home'))
    
    return render_template('shopping.html', 
                         items=items, 
                         cart=session.get('cart', []),
                         total_price=session.get('total_price', 0),
                         customer_name=session.get('customer_name', ''))

@app.route('/add_item', methods=['POST'])
def add_item():
    """Add item to cart"""
    if not session.get('shopping_active'):
        return redirect(url_for('home'))
    
    item_name = request.form.get('item', '').lower().strip()
    try:
        quantity = int(request.form.get('quantity', 0))
    except ValueError:
        flash('Please enter a valid quantity', 'error')
        return redirect(url_for('shopping'))
    
    if quantity <= 0:
        flash('Quantity must be greater than 0', 'error')
        return redirect(url_for('shopping'))
    
    if item_name in items:
        price = quantity * items[item_name]
        
        # Add to cart
        cart_item = {
            'name': item_name.title(),
            'quantity': quantity,
            'unit_price': items[item_name],
            'total_price': price
        }
        
        if 'cart' not in session:
            session['cart'] = []
        
        session['cart'].append(cart_item)
        session['total_price'] = session.get('total_price', 0) + price
        session.modified = True
        
        flash(f'{item_name.title()} added to cart successfully!', 'success')
    else:
        flash('Sorry, the item you entered is not available', 'error')
    
    return redirect(url_for('shopping'))

@app.route('/remove_item/<int:index>')
def remove_item(index):
    """Remove item from cart"""
    if not session.get('shopping_active'):
        return redirect(url_for('home'))
    
    cart = session.get('cart', [])
    if 0 <= index < len(cart):
        removed_item = cart.pop(index)
        session['total_price'] -= removed_item['total_price']
        session.modified = True
        flash(f'{removed_item["name"]} removed from cart', 'info')
    
    return redirect(url_for('shopping'))

@app.route('/generate_bill')
def generate_bill():
    """Generate final bill"""
    if not session.get('shopping_active') or not session.get('cart'):
        flash('No items in cart to bill', 'error')
        return redirect(url_for('shopping'))
    
    total_price = session.get('total_price', 0)
    gst = (total_price * 5) / 100
    final_amount = total_price + gst
    
    bill_data = {
        'customer_name': session.get('customer_name', ''),
        'cart': session.get('cart', []),
        'total_price': total_price,
        'gst': round(gst, 2),
        'final_amount': round(final_amount, 2),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Mark shopping as complete
    session['shopping_active'] = False
    
    return render_template('bill.html', **bill_data)

@app.route('/new_customer')
def new_customer():
    """Start fresh with new customer"""
    session.clear()
    return redirect(url_for('home'))

# Create templates directory if it doesn't exist
if not os.path.exists('templates'):
    os.makedirs('templates')

# Template files content
templates = {
    'base.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Optimus SuperMarket{% endblock %}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(45deg, #2c3e50, #3498db);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header .location {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
            font-size: 1.1em;
        }
        
        input, select {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: #3498db;
            box-shadow: 0 0 10px rgba(52, 152, 219, 0.3);
        }
        
        .btn {
            display: inline-block;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 5px;
        }
        
        .btn-primary {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(52, 152, 219, 0.3);
        }
        
        .btn-success {
            background: linear-gradient(45deg, #27ae60, #229954);
            color: white;
        }
        
        .btn-success:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(39, 174, 96, 0.3);
        }
        
        .btn-danger {
            background: linear-gradient(45deg, #e74c3c, #c0392b);
            color: white;
        }
        
        .btn-danger:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(231, 76, 60, 0.3);
        }
        
        .btn-warning {
            background: linear-gradient(45deg, #f39c12, #e67e22);
            color: white;
        }
        
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-weight: 500;
        }
        
        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert-error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .alert-info {
            background-color: #cce7ff;
            color: #004085;
            border: 1px solid #b3d7ff;
        }
        
        .items-display {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 5px solid #3498db;
        }
        
        .items-display h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .items-display pre {
            font-family: 'Courier New', monospace;
            line-height: 1.8;
            color: #555;
            font-size: 1.1em;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        th {
            background: linear-gradient(45deg, #34495e, #2c3e50);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }
        
        tr:hover {
            background-color: #f8f9fa;
        }
        
        .cart-summary {
            background: #e8f5e8;
            padding: 25px;
            border-radius: 10px;
            margin-top: 30px;
            border-left: 5px solid #27ae60;
        }
        
        .total-section {
            background: #f0f8ff;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
            border-left: 5px solid #3498db;
        }
        
        .bill-header {
            text-align: center;
            padding: 30px;
            background: #f8f9fa;
            margin-bottom: 30px;
            border-radius: 10px;
        }
        
        .bill-header h2 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 10px;
            }
            
            .content {
                padding: 20px;
            }
            
            .header {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛒 Optimus SuperMarket</h1>
            <div class="location">📍 Vijayawada</div>
        </div>
        <div class="content">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ 'error' if category == 'error' else category }}">
                            {{ message }}
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            {% block content %}{% endblock %}
        </div>
    </div>
</body>
</html>''',

    'home.html': '''{% extends "base.html" %}
{% block title %}Welcome - Optimus SuperMarket{% endblock %}
{% block content %}
<h2 style="color: #2c3e50; margin-bottom: 30px; text-align: center;">🎉 Welcome to Our Store!</h2>

<div class="items-display">
    <h3>📋 Available Items & Prices:</h3>
    <pre>{{ item_list }}</pre>
</div>

<form method="POST" action="{{ url_for('start_shopping') }}">
    <div class="form-group">
        <label for="name">👤 Enter Your Name:</label>
        <input type="text" id="name" name="name" placeholder="Enter your full name" required>
    </div>
    <div style="text-align: center;">
        <button type="submit" class="btn btn-primary">🛍️ Start Shopping</button>
    </div>
</form>
{% endblock %}''',

    'shopping.html': '''{% extends "base.html" %}
{% block title %}Shopping Cart - Optimus SuperMarket{% endblock %}
{% block content %}
<h2 style="color: #2c3e50; margin-bottom: 20px;">🛍️ Shopping Cart</h2>
<p style="font-size: 1.2em; margin-bottom: 30px;"><strong>Customer:</strong> {{ customer_name }}</p>

<form method="POST" action="{{ url_for('add_item') }}">
    <div style="display: grid; grid-template-columns: 2fr 1fr auto; gap: 15px; align-items: end; margin-bottom: 30px;">
        <div class="form-group" style="margin-bottom: 0;">
            <label for="item">🛒 Select Item:</label>
            <select id="item" name="item" required>
                <option value="">Choose an item...</option>
                {% for item_name, price in items.items() %}
                    <option value="{{ item_name }}">{{ item_name.title() }} - Rs {{ price }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="form-group" style="margin-bottom: 0;">
            <label for="quantity">📦 Quantity:</label>
            <input type="number" id="quantity" name="quantity" min="1" placeholder="Enter qty" required>
        </div>
        <button type="submit" class="btn btn-success" style="height: fit-content;">➕ Add to Cart</button>
    </div>
</form>

{% if cart %}
<div class="cart-summary">
    <h3>🛒 Your Shopping Cart:</h3>
    <table>
        <thead>
            <tr>
                <th>S.No</th>
                <th>Item</th>
                <th>Quantity</th>
                <th>Unit Price</th>
                <th>Total Price</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            {% for i in range(cart|length) %}
            <tr>
                <td>{{ i + 1 }}</td>
                <td>{{ cart[i].name }}</td>
                <td>{{ cart[i].quantity }}</td>
                <td>Rs {{ cart[i].unit_price }}</td>
                <td>Rs {{ cart[i].total_price }}</td>
                <td>
                    <a href="{{ url_for('remove_item', index=i) }}" class="btn btn-danger" style="padding: 8px 15px; font-size: 14px;">🗑️ Remove</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <div style="text-align: right; margin-top: 20px; font-size: 1.3em;">
        <strong>💰 Current Total: Rs {{ total_price }}</strong>
    </div>
    
    <div style="text-align: center; margin-top: 25px;">
        <a href="{{ url_for('generate_bill') }}" class="btn btn-success" style="font-size: 1.1em; padding: 18px 35px;">
            🧾 Generate Bill
        </a>
    </div>
</div>
{% else %}
<div style="text-align: center; padding: 40px; color: #7f8c8d;">
    <h3>🛒 Your cart is empty</h3>
    <p>Add some items to get started!</p>
</div>
{% endif %}

<div style="text-align: center; margin-top: 30px;">
    <a href="{{ url_for('new_customer') }}" class="btn btn-warning">👤 New Customer</a>
</div>
{% endblock %}''',

    'bill.html': '''{% extends "base.html" %}
{% block title %}Bill - Optimus SuperMarket{% endblock %}
{% block content %}
<div class="bill-header">
    <h2>🧾 INVOICE</h2>
    <h3>========================</h3>
    <h3>Optimus SuperMarket</h3>
    <h3>========================</h3>
    <p style="margin-top: 15px;">📍 Vijayawada</p>
</div>

<div style="margin-bottom: 30px; display: flex; justify-content: space-between; font-size: 1.1em;">
    <div><strong>👤 Customer:</strong> {{ customer_name }}</div>
    <div><strong>📅 Date:</strong> {{ date }}</div>
</div>

<table>
    <thead>
        <tr>
            <th>S.No</th>
            <th>Items</th>
            <th>Quantity</th>
            <th>Unit Price</th>
            <th>Total Price</th>
        </tr>
    </thead>
    <tbody>
        {% for i in range(cart|length) %}
        <tr>
            <td>{{ i + 1 }}</td>
            <td>{{ cart[i].name }}</td>
            <td>{{ cart[i].quantity }}</td>
            <td>Rs {{ cart[i].unit_price }}</td>
            <td>Rs {{ cart[i].total_price }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<div class="total-section">
    <div style="text-align: right; font-size: 1.2em; line-height: 1.8;">
        <div><strong>💰 Total Amount: Rs {{ total_price }}</strong></div>
        <div><strong>📊 GST (5%): Rs {{ gst }}</strong></div>
        <div style="font-size: 1.4em; color: #27ae60; border-top: 2px solid #27ae60; padding-top: 10px; margin-top: 10px;">
            <strong>🎯 Final Amount: Rs {{ final_amount }}</strong>
        </div>
    </div>
</div>

<div style="text-align: center; margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
    <h3 style="color: #27ae60;">🙏 Thanks for visiting!</h3>
    <p style="margin-top: 10px; color: #7f8c8d;">Have a great day!</p>
</div>

<div style="text-align: center; margin-top: 30px;">
    <a href="{{ url_for('new_customer') }}" class="btn btn-primary" style="font-size: 1.1em; padding: 15px 30px;">
        👤 New Customer
    </a>
    <button onclick="window.print()" class="btn btn-success" style="font-size: 1.1em; padding: 15px 30px;">
        🖨️ Print Bill
    </button>
</div>

<style>
    @media print {
        .btn { display: none; }
        .header { background: white !important; color: black !important; }
        body { background: white !important; }
        .container { box-shadow: none !important; }
    }
</style>
{% endblock %}'''
}

# Write template files
for filename, content in templates.items():
    with open(f'templates/{filename}', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    print("🚀 Flask Supermarket Application Setup Complete!")
    print("📁 Templates created successfully!")
    print("\n📋 To run the application:")
    print("1. Install Flask: pip install flask")
    print("2. Run: python app.py")
    print("3. Open browser: http://127.0.0.1:5000")
    print("\n🎉 Features:")
    print("✅ Beautiful responsive UI")
    print("✅ Session-based cart management")
    print("✅ Real-time total calculation")
    print("✅ Professional bill generation")
    print("✅ Print functionality")
    print("✅ Mobile-friendly design")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
