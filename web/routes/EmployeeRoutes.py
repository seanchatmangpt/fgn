
from flask import Flask, request, render_template
from ddd.services.EmployeeService import EmployeeService
from ddd.repositories.EmployeeRepo import EmployeeRepo
from ddd.entities.Employee import Employee

app = Flask(__name__)
repo = EmployeeRepo()
service = EmployeeService(repo)

@app.route('/employee', methods=['GET'])
def get_employees():
    entities = [entity for entity in repo.data.values()]
    return render_template('employee.html', entities=entities)

@app.route('/employee/create', methods=['POST'])
def create_employee():
    # Logic to create a Employee
    entity = Employee()  # Initialize with proper parameters from request
    service.create(entity)
    return redirect('/employee')

@app.route('/employee/update/<id>', methods=['POST'])
def update_employee(id):
    # Logic to update a Employee
    entity = Employee()  # Initialize with proper parameters from request
    service.update(id, entity)
    return redirect('/employee')

@app.route('/employee/delete/<id>', methods=['POST'])
def delete_employee(id):
    service.delete(id)
    return redirect('/employee')
    