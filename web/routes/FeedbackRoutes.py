
from flask import Flask, request, render_template
from ddd.services.FeedbackService import FeedbackService
from ddd.repositories.FeedbackRepo import FeedbackRepo
from ddd.entities.Feedback import Feedback

app = Flask(__name__)
repo = FeedbackRepo()
service = FeedbackService(repo)

@app.route('/feedback', methods=['GET'])
def get_feedbacks():
    entities = [entity for entity in repo.data.values()]
    return render_template('feedback.html', entities=entities)

@app.route('/feedback/create', methods=['POST'])
def create_feedback():
    # Logic to create a Feedback
    entity = Feedback()  # Initialize with proper parameters from request
    service.create(entity)
    return redirect('/feedback')

@app.route('/feedback/update/<id>', methods=['POST'])
def update_feedback(id):
    # Logic to update a Feedback
    entity = Feedback()  # Initialize with proper parameters from request
    service.update(id, entity)
    return redirect('/feedback')

@app.route('/feedback/delete/<id>', methods=['POST'])
def delete_feedback(id):
    service.delete(id)
    return redirect('/feedback')
    