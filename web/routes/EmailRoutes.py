
from flask import Flask, request, render_template
from ddd.services.EmailService import EmailService
from ddd.repositories.EmailRepo import EmailRepo
from ddd.entities.Email import Email

app = Flask(__name__)
repo = EmailRepo()
service = EmailService(repo)

@app.route('/email', methods=['GET'])
def get_emails():
    entities = [entity for entity in repo.data.values()]
    return render_template('email.html', entities=entities)

@app.route('/email/create', methods=['POST'])
def create_email():
    # Logic to create a Email
    entity = Email()  # Initialize with proper parameters from request
    service.create(entity)
    return redirect('/email')

@app.route('/email/update/<id>', methods=['POST'])
def update_email(id):
    # Logic to update a Email
    entity = Email()  # Initialize with proper parameters from request
    service.update(id, entity)
    return redirect('/email')

@app.route('/email/delete/<id>', methods=['POST'])
def delete_email(id):
    service.delete(id)
    return redirect('/email')
    