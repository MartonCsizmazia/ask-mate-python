from flask import Flask, render_template, request, redirect, url_for

import data_manager
import connection
import util

app = Flask(__name__)


@app.route('/question/<question_id>')
def route_question(question_id):
    question_headers = ['title', 'message', 'submission_time', 'view_number', 'vote_number', 'image']
    answer_headers = ['message', 'submission_time', 'vote_number', 'image', 'user_options']
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answer_by_question_id(question_id)

    return render_template('question.html',
                           question=question,
                           question_title='Question',
                           answers=answers,
                           question_headers=question_headers,
                           answer_headers=answer_headers,
                           )


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question = data_manager.get_question_by_id(question_id)

    if request.method == 'POST':

        my_new_data = {
            "id": request.form.get("question_id"),
            "title": request.form.get("title"),
            "message": request.form.get("message"),
        }

        data_manager.edit_question(my_new_data)

        return redirect('/')

    return render_template('edit_question.html', question=question,)


@app.route('/question/<question_id>/vote-<vote>')
def question_vote(question_id, vote):
    if vote == 'up':
        data_manager.question_vote_up(question_id)
    else:
        data_manager.question_vote_down(question_id)
    return redirect('/question/' + question_id)


@app.route('/answer/<answer_id>/vote-<vote>')
def answer_vote(answer_id, vote):
    if vote == 'up':
        data_manager.answer_vote_up(answer_id)
    else:
        data_manager.answer_vote_down(answer_id)
    changed_answer = data_manager.get_answer_by_id(answer_id)
    return redirect('/question/' + str(changed_answer['question_id']))


@app.route('/list')
@app.route("/")
def list():
    headers = ['title', 'submission_time', 'view_number', 'vote_number']
    questions = data_manager.get_all_questions()

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


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_new_answer(question_id):

    question = data_manager.get_question_by_id(question_id)
    if request.method == 'POST':

        new_submission_time = util.date_now()
        new_answer = {
                    "submission_time": new_submission_time,
                    "vote_number": 0,
                    "question_id": request.form.get("question_id"),
                    "message": request.form.get("answer-message"),
                    "image": ""}

        #func = request.environ.get('werkzeug.server.shutdown')
        data_manager.add_answer(new_answer)

        return redirect('/question/' + new_answer['question_id'])

    else:
        return render_template('post_answer.html',
                               question=question
                               )


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )