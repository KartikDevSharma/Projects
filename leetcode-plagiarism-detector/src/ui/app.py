from flask import Flask, render_template, request, redirect, url_for
from src.data_collection.database_manager import DatabaseManager

app = Flask(__name__)

@app.route('/')
def index():
    db_manager = DatabaseManager()
    db_manager.connect()
    contests = db_manager.get_contests()
    db_manager.close()
    return render_template('index.html', contests=contests)

@app.route('/report', methods=['POST'])
def generate_report():
    contest_id = request.form['contest_id']
    similarity_threshold = float(request.form['similarity_threshold'])
    flag_threshold = int(request.form['flag_threshold'])

    db_manager = DatabaseManager()
    db_manager.connect()
    report = db_manager.generate_plagiarism_report(contest_id, similarity_threshold, flag_threshold)
    db_manager.close()

    return render_template('report.html', report=report, contest_id=contest_id)

if __name__ == '__main__':
    app.run(debug=True)