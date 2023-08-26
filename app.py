
from flask import Flask, render_template
from web.routes.EmailRoutes import app as email_app
from web.routes.EmployeeRoutes import app as employee_app
from web.routes.FeedbackRoutes import app as feedback_app
from web.routes.ReportRoutes import app as report_app

app = Flask(__name__)

app.register_blueprint(email_app, url_prefix='/email')
app.register_blueprint(employee_app, url_prefix='/employee')
app.register_blueprint(feedback_app, url_prefix='/feedback')
app.register_blueprint(report_app, url_prefix='/report')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    