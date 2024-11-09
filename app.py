from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'
db = SQLAlchemy(app)

# Database Model for Student
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def _repr_(self):
        return f"<Student {self.name}>"

# Function to create database tables
def create_tables():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

# Call the create_tables function to ensure tables are created
create_tables()

# Route to view all students
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Route to add a new student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']
        email = request.form['email']
        new_student = Student(name=name, age=age, grade=grade, email=email)
        db.session.add(new_student)
        db.session.commit()
        flash("Student added successfully!", "success")
        return redirect(url_for('index'))
    return render_template('add_student.html')

# Route to update a student's details
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.age = request.form['age']
        student.grade = request.form['grade']
        student.email = request.form['email']
        db.session.commit()
        flash("Student updated successfully!", "success")
        return redirect(url_for('index'))
    return render_template('edit_student.html', student=student)

# Route to delete a student
@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully!", "success")
    return redirect(url_for('index'))

if _name_ == '_main_':
    app.run(debug=True, host='0.0.0.0', port=5000)
