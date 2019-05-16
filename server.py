from flask import Flask, render_template, request, redirect, url_for

import data_manager
import connection
import util

app = Flask(__name__)


@app.route('/question/<question_id>')
def route_question(question_id):
    question_headers = ['title', 'message', 'submission_time', 'view_number', 'vote_number', 'image']
    answer_headers = ['message', 'submission_time', 'vote_number', 'image']
    question = data_manager.get_questions(question_id)
    answers = data_manager.get_answers(question_id)

    return render_template('question.html',
                           question=question,
                           question_title='Question',
                           answers=answers,
                           question_headers=question_headers,
                           answer_headers=answer_headers)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):

    questions = data_manager.get_questions()
    QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
    QUESTION = 'sample_data/question.csv'
    if request.method == 'POST':

        new_submission_time = util.unix_date_now()
        my_new_data = {
            "id": question_id,
            "submission_time": new_submission_time,
            "view_number": 0,
            "vote_number": 0,
            "title": request.form.get("title"),
            "message": request.form.get("message"),
            "image": "",
        }

        connection.export_data_to_csv(QUESTION, my_new_data, QUESTION_HEADER)
        return redirect('/')

    else:
        return render_template('edit_question.html')



@app.route('/list')
@app.route("/")
def list():
    headers = ['title', 'submission_time', 'view_number', 'vote_number']
    questions = data_manager.get_questions()

    return render_template('list.html',
                           headers=headers,
                           questions=questions)





@app.route('/add-question', methods=['GET', 'POST'])
def route_add():
    questions = data_manager.get_questions()
    QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
    QUESTION = 'sample_data/question.csv'
    if request.method == 'POST':
        new_id = data_manager.generate_id(questions)
        new_submission_time = util.unix_date_now()
        my_new_data = {
                    "id": new_id,
                    "submission_time": new_submission_time,
                    "view_number": 0,
                    "vote_number": 0,
                    "title": request.form.get("title"),
                    "message": request.form.get("message"),
                    "image": "",
         }

        connection.export_data_to_csv(QUESTION, my_new_data, QUESTION_HEADER)
        return redirect('/')

    else:
        return render_template('add.html')


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    fieldnames = data_manager.ANSWER_HEADER
    connection.delete_data_from_csv(data_manager.ANSWER, answer_id, fieldnames)

    return redirect('/list')


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    connecting_answers = data_manager.get_answers(question_id)
    answer_fieldnames = data_manager.ANSWER_HEADER
    for answer in connecting_answers:
        connection.delete_data_from_csv(data_manager.ANSWER, answer['id'], answer_fieldnames)

    question_fieldnames = data_manager.QUESTION_HEADER
    connection.delete_data_from_csv(data_manager.QUESTION, question_id, question_fieldnames)

    return redirect('/list')
"""
@app.route()
def cancel():
    return redirect('/list')
"""
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )