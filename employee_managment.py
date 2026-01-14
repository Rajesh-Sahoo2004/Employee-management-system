from flask import Flask, render_template_string, request, redirect
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100))


with app.app_context():
    db.create_all()


# -------------------- TEMPLATES --------------------
layout = """
<!DOCTYPE html>
<html>
<head>
    <title>Employee Management System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 20px;
        }

        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            animation: fadeIn 0.6s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .header-section {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            text-align: center;
        }

        .header-section h2 {
            color: #667eea;
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }

        .header-section p {
            color: #6c757d;
            font-size: 1.1rem;
        }

        .nav-buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 30px;
        }

        .nav-buttons .btn {
            padding: 12px 30px;
            border-radius: 50px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            border: none;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-decoration: none;
        }

        .nav-buttons .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            text-decoration: none;
            color: white;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-success {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }

        .btn-info {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }

        .content-card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            animation: slideUp 0.5s ease-out;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .welcome-card {
            text-align: center;
            padding: 60px 40px;
        }

        .welcome-card h4 {
            color: #667eea;
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 20px;
        }

        .welcome-card p {
            color: #6c757d;
            font-size: 1.2rem;
            margin-bottom: 30px;
        }

        .welcome-features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }

        .feature-box {
            padding: 25px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            transition: all 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
            display: block;
            border: 2px solid transparent;
        }

        .feature-box:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 30px rgba(102, 126, 234, 0.3);
            border-color: #667eea;
            text-decoration: none;
            color: inherit;
        }

        .feature-box i {
            font-size: 2.5rem;
            color: #667eea;
            margin-bottom: 10px;
            transition: all 0.3s ease;
        }

        .feature-box:hover i {
            color: #764ba2;
            font-size: 3rem;
        }

        .feature-box h5 {
            color: #333;
            font-weight: 600;
            margin-bottom: 5px;
            transition: all 0.3s ease;
        }

        .feature-box:hover h5 {
            color: #667eea;
        }

        .feature-box p {
            color: #6c757d;
            font-size: 0.9rem;
            margin: 0;
        }

        .table-container {
            overflow-x: auto;
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(0,0,0,0.05);
        }

        .table {
            margin: 0;
            border-radius: 15px;
            overflow: hidden;
        }

        .table thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .table thead th {
            padding: 18px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border: none;
            font-size: 0.9rem;
        }

        .table tbody tr {
            transition: all 0.3s ease;
            border-bottom: 1px solid #f0f0f0;
        }

        .table tbody tr:hover {
            background: #f8f9fa;
            transform: scale(1.01);
            box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        }

        .table tbody td {
            padding: 18px;
            vertical-align: middle;
            color: #333;
        }

        .table .btn-sm {
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin: 0 3px;
            border: none;
            transition: all 0.3s ease;
            text-decoration: none;
        }

        .table .btn-warning {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }

        .table .btn-danger {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
            color: white;
        }

        .table .btn-sm:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            text-decoration: none;
            color: white;
        }

        .form-card {
            max-width: 600px;
            margin: 0 auto;
        }

        .form-card h4 {
            color: #667eea;
            font-weight: 600;
            margin-bottom: 30px;
            text-align: center;
            font-size: 1.8rem;
        }

        .form-control {
            padding: 14px 20px;
            border-radius: 12px;
            border: 2px solid #e0e0e0;
            margin-bottom: 20px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        .form-control:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
            outline: none;
        }

        .form-control::placeholder {
            color: #adb5bd;
        }

        .form-label {
            font-weight: 600;
            color: #495057;
            margin-bottom: 8px;
            display: block;
        }

        .submit-btn {
            width: 100%;
            padding: 15px;
            border-radius: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            border: none;
            margin-top: 10px;
            transition: all 0.3s ease;
            font-size: 1.1rem;
            cursor: pointer;
        }

        .submit-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }

        .btn-success.submit-btn {
            background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
            color: white;
        }

        .btn-warning.submit-btn {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #6c757d;
        }

        .empty-state i {
            font-size: 5rem;
            color: #dee2e6;
            margin-bottom: 20px;
        }

        .empty-state h5 {
            font-size: 1.5rem;
            margin-bottom: 10px;
        }

        .empty-state .btn {
            margin-top: 10px;
            display: inline-block;
            padding: 12px 30px;
            border-radius: 50px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            text-decoration: none;
            transition: all 0.3s ease;
        }

        .empty-state .btn:hover {
            transform: translateY(-3px);
            text-decoration: none;
            color: white;
        }

        @media (max-width: 768px) {
            .header-section h2 {
                font-size: 1.8rem;
            }

            .nav-buttons {
                flex-direction: column;
            }

            .nav-buttons .btn {
                width: 100%;
                justify-content: center;
            }

            .welcome-features {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
<div class="main-container">
    <div class="header-section">
        <h2><i class="fas fa-users-cog"></i> Employee Management System</h2>
        <p>Streamline your workforce management with ease</p>
    </div>

    <div class="nav-buttons">
        <a href="/" class="btn btn-primary"><i class="fas fa-home"></i> Home</a>
        <a href="/add" class="btn btn-success"><i class="fas fa-user-plus"></i> Add Employee</a>
        <a href="/employees" class="btn btn-info"><i class="fas fa-list"></i> View Employees</a>
    </div>

    <div class="content-card">
        {{content|safe}}
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""


@app.route('/')
def index():
    home_content = """
    <div class="welcome-card">
        <h4><i class="fas fa-rocket"></i> Welcome to Employee Management!</h4>
        <p>Manage your team efficiently with our powerful and intuitive system</p>

        <div class="welcome-features">
            <a href="/add" class="feature-box">
                <i class="fas fa-user-plus"></i>
                <h5>Add Employees</h5>
                <p>Quick and easy employee registration</p>
            </a>
            <a href="/employees" class="feature-box">
                <i class="fas fa-edit"></i>
                <h5>Update Records</h5>
                <p>Modify employee information anytime</p>
            </a>
            <a href="/employees" class="feature-box">
                <i class="fas fa-search"></i>
                <h5>View All</h5>
                <p>Access complete employee database</p>
            </a>
            <a href="/employees" class="feature-box">
                <i class="fas fa-trash-alt"></i>
                <h5>Remove Entries</h5>
                <p>Delete records when needed</p>
            </a>
        </div>
    </div>
    """
    return render_template_string(layout, content=home_content)


@app.route('/employees')
def employees():
    data = Employee.query.all()

    if not data:
        empty_content = """
        <div class="empty-state">
            <i class="fas fa-users-slash"></i>
            <h5>No Employees Found</h5>
            <p>Start by adding your first employee to the system</p>
            <a href="/add" class="btn btn-success"><i class="fas fa-user-plus"></i> Add Employee</a>
        </div>
        """
        return render_template_string(layout, content=empty_content)

    table = """
    <div class="table-container">
        <table class="table table-hover">
            <thead>
                <tr>
                    <th><i class="fas fa-user"></i> Name</th>
                    <th><i class="fas fa-envelope"></i> Email</th>
                    <th><i class="fas fa-phone"></i> Phone</th>
                    <th><i class="fas fa-building"></i> Department</th>
                    <th><i class="fas fa-cog"></i> Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for emp in employees %}
                <tr>
                    <td><strong>{{emp.name}}</strong></td>
                    <td>{{emp.email}}</td>
                    <td>{{emp.phone}}</td>
                    <td><span class="badge bg-primary">{{emp.department}}</span></td>
                    <td>
                        <a href="/update/{{emp.id}}" class="btn btn-warning btn-sm">
                            <i class="fas fa-edit"></i> Edit
                        </a>
                        <a href="/delete/{{emp.id}}" class="btn btn-danger btn-sm" 
                           onclick="return confirm('Are you sure you want to delete this employee?')">
                            <i class="fas fa-trash"></i> Delete
                        </a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    """
    return render_template_string(layout, content=render_template_string(table, employees=data))


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = """
    <div class="form-card">
        <h4><i class="fas fa-user-plus"></i> Add New Employee</h4>
        <form method="POST">
            <div>
                <label class="form-label"><i class="fas fa-user"></i> Full Name</label>
                <input name="name" class="form-control" placeholder="Enter employee name" required>
            </div>

            <div>
                <label class="form-label"><i class="fas fa-envelope"></i> Email Address</label>
                <input name="email" type="email" class="form-control" placeholder="Enter email address" required>
            </div>

            <div>
                <label class="form-label"><i class="fas fa-phone"></i> Phone Number</label>
                <input name="phone" class="form-control" placeholder="Enter phone number" required>
            </div>

            <div>
                <label class="form-label"><i class="fas fa-building"></i> Department</label>
                <input name="department" class="form-control" placeholder="Enter department" required>
            </div>

            <button class="btn btn-success submit-btn">
                <i class="fas fa-check-circle"></i> Add Employee
            </button>
        </form>
    </div>
    """
    if request.method == 'POST':
        emp = Employee(name=request.form['name'], email=request.form['email'],
                       phone=request.form['phone'], department=request.form['department'])
        db.session.add(emp)
        db.session.commit()
        return redirect('/employees')
    return render_template_string(layout, content=form)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    emp = Employee.query.get(id)
    form = f"""
    <div class="form-card">
        <h4><i class="fas fa-edit"></i> Update Employee Details</h4>
        <form method="POST">
            <div>
                <label class="form-label"><i class="fas fa-user"></i> Full Name</label>
                <input name="name" class="form-control" value="{emp.name}" required>
            </div>

            <div>
                <label class="form-label"><i class="fas fa-envelope"></i> Email Address</label>
                <input name="email" type="email" class="form-control" value="{emp.email}" required>
            </div>

            <div>
                <label class="form-label"><i class="fas fa-phone"></i> Phone Number</label>
                <input name="phone" class="form-control" value="{emp.phone}" required>
            </div>

            <div>
                <label class="form-label"><i class="fas fa-building"></i> Department</label>
                <input name="department" class="form-control" value="{emp.department}" required>
            </div>

            <button class="btn btn-warning submit-btn">
                <i class="fas fa-save"></i> Update Employee
            </button>
        </form>
    </div>
    """
    if request.method == 'POST':
        emp.name = request.form['name']
        emp.email = request.form['email']
        emp.phone = request.form['phone']
        emp.department = request.form['department']
        db.session.commit()
        return redirect('/employees')
    return render_template_string(layout, content=form)


@app.route('/delete/<int:id>')
def delete(id):
    emp = Employee.query.get(id)
    db.session.delete(emp)
    db.session.commit()
    return redirect('/employees')


if __name__ == '__main__':
    app.run(debug=True)
