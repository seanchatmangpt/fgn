
from flask import Flask, request, render_template
from ddd.services.ReportService import ReportService
from ddd.repositories.ReportRepo import ReportRepo
from ddd.entities.Report import Report

app = Flask(__name__)
repo = ReportRepo()
service = ReportService(repo)

@app.route('/report', methods=['GET'])
def get_reports():
    entities = [entity for entity in repo.data.values()]
    return render_template('report.html', entities=entities)

@app.route('/report/create', methods=['POST'])
def create_report():
    # Logic to create a Report
    entity = Report()  # Initialize with proper parameters from request
    service.create(entity)
    return redirect('/report')

@app.route('/report/update/<id>', methods=['POST'])
def update_report(id):
    # Logic to update a Report
    entity = Report()  # Initialize with proper parameters from request
    service.update(id, entity)
    return redirect('/report')

@app.route('/report/delete/<id>', methods=['POST'])
def delete_report(id):
    service.delete(id)
    return redirect('/report')
    