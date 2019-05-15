from flask import Flask, render_template, request, redirect, url_for

import data_manager

app = Flask(__name__)


@app.route('/question/<question_id>')
def route_question(question_id):
    question = data_manager.get_questions(question_id)
    answer = data_manager.get_answers_for_question(question_id)

    return render_template('question.html',
                           question=question,
                           question_title='Question',
                           answer=answer)


@app.route('/list')
def list():
    headers = ['title', 'submission_time', 'view_number', 'vote_number']
    questions = data_manager.get_questions()

    return render_template('list.html',
                           headers=headers,
                           questions=questions)


@app.route('/add-question', methods=['GET', 'POST'])
def route_add():
    return render_template('add.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )