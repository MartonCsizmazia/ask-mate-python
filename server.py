from flask import Flask, render_template, request, redirect, url_for

import data_manager
import util

app = Flask(__name__)


@app.route('/question/<question_id>')
def route_question(question_id):
    question_headers = ['title', 'message', 'submission_time', 'view_number', 'vote_number', 'image']
    answer_headers = ['message', 'submission_time', 'vote_number', 'image', 'user_options']
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answer_by_question_id(question_id)
    answer_ids = tuple([answer['id'] for answer in answers])
    if len(answer_ids) > 0:
        answer_comments = data_manager.get_comments_by_answer_idlist(answer_ids)
    else:
        answer_comments = None
    tags = data_manager.get_tags_by_question_id(question_id)
    question_comments = data_manager.get_comments_by_question_id(question_id)

    return render_template('question.html',
                           question=question,
                           question_title='Question',
                           answers=answers,
                           question_headers=question_headers,
                           answer_headers=answer_headers,
                           tags=tags,
                           question_comments=question_comments,
                           answer_comments=answer_comments
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

        return redirect('/question/' + str(my_new_data['id']))

    return render_template('edit_question.html', question=question, )


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
def route_list():
    headers = ['view_number', 'vote_number', 'title']
    questions = data_manager.get_all_questions()

    return render_template('list.html',
                           headers=headers,
                           questions=questions,
                           type='list_all')


@app.route("/")
def index():
    headers = ['view_number', 'vote_number', 'title']
    questions = data_manager.get_last_5_questions()

    return render_template('list.html',
                           headers=headers,
                           questions=questions,
                           type='limit_5')


@app.route('/add-question', methods=['GET', 'POST'])
def route_add():
    questions = data_manager.get_all_questions()

    if request.method == 'POST':
        new_submission_time = util.date_now()
        my_new_data = {

            "submission_time": new_submission_time,
            "view_number": 0,
            "vote_number": 0,
            "title": request.form.get("title"),
            "message": request.form.get("message"),
            "image": ""
        }

        data_manager.add_question(my_new_data)
        return redirect('/')

    else:
        return render_template('add.html', questions=questions)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    data_manager.delete_answer_by_id(answer_id)
    data_manager.delete_comment_by_answer_id(answer_id)

    return redirect('/question/' + str(answer['question_id']))


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_answer_by_question_id(question_id)
    data_manager.delete_question_tag(question_id)
    data_manager.delete_question(question_id)
    data_manager.delete_comment_by_question_id(question_id)

    return redirect('/list')


@app.route('/comment/<comment_id>/delete')
def delete_comment(comment_id):
    comment = data_manager.get_comment_by_id(comment_id)
    question_id = comment['question_id']
    if question_id is None:
        question_id = data_manager.get_answer_by_id(comment['answer_id'])['question_id']

    data_manager.delete_comment_by_id(comment_id)

    return redirect('/question/' + str(question_id))


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

        data_manager.add_answer(new_answer)

        return redirect('/question/' + new_answer['question_id'])

    else:
        return render_template('post_answer.html',
                               question=question)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)

    if request.method == 'POST':
        my_new_data = {
            "id": request.form.get("answer_id"),
            "question_id": request.form.get("question_id"),
            "message": request.form.get("message"),
        }

        data_manager.edit_answer(my_new_data)

        return redirect('/question/' + str(my_new_data['question_id']))

    return render_template('edit_answer.html', answer=answer)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    question_headers = ['title', 'message', 'submission_time', 'view_number', 'vote_number', 'image']

    if request.method == 'POST':
        new_comment = {
            "submission_time": util.date_now(),
            "question_id": request.form.get("question_id"),
            "message": request.form.get("comment-message"),
            "edited_count": 0
        }
        data_manager.add_comment_to_question(new_comment)

        return redirect('/question/' + new_comment['question_id'])

    return render_template('add_comment_to_question.html', question_headers=question_headers, question=question)


@app.route('/search', methods=['POST'])
def search_question():
    headers = ['title', 'submission_time', 'view_number', 'vote_number']

    search_phrase = '%' + request.form.get('search_text') + '%'

    question = data_manager.search_question(search_phrase)

    return render_template('search_question.html',
                           headers=headers,
                           question=question,
                           )


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    answer_headers = ['message', 'submission_time', 'vote_number', 'image']
    answer = data_manager.get_answer_by_id(answer_id)
    if request.method == 'POST':

        new_submission_time = util.date_now()
        new_comment = {
            "submission_time": new_submission_time,
            "answer_id": request.form.get("answer_id"),
            "message": request.form.get("comment-message"),
            "edited_count": 0
        }

        data_manager.add_comment_to_answer(new_comment)

        return redirect('/question/' + str(request.form.get('question_id')))

    else:
        return render_template('post_comment_to_answer.html',
                               answer=answer,
                               answer_headers=answer_headers
                               )


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def add_tag_to_question(question_id):
    question_headers = ['title', 'message', 'submission_time', 'view_number', 'vote_number', 'image']
    question = data_manager.get_question_by_id(question_id)
    tags = data_manager.get_all_tags()

    if request.method == 'POST':
        if request.form.get("selector") == "custom":
            question_id = request.form.get("question_id")
            name = request.form.get("tag_message").strip().lower()
            data_manager.add_new_tag_to_tags(name)
            id = data_manager.get_tag_id(name)
            data_manager.add_new_tag_to_question(request.form.get("question_id"), id['id'])
        else:
            question_id = request.form.get("question_id")
            name = request.form.get("selector")
            id = data_manager.get_tag_id(name)
            data_manager.add_new_tag_to_question(request.form.get("question_id"), id['id'])

        return redirect('/question/' + str(question_id))

    return render_template('add_tag_to_question.html',  question=question, tags=tags, question_headers=question_headers)


@app.route('/question/<question_id>/tag/<tag_id>delete', methods=['GET'])
def delete_tag_from_question(question_id, tag_id):

    data_manager.delete_tag_from_question(tag_id)

    return redirect('/question/' + str(question_id))


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    comment = data_manager.get_comment_by_id(comment_id)
    question_id = comment['question_id']
    if question_id is None:
        question_id = data_manager.get_answer_by_id(comment['answer_id'])['question_id']

    if request.method == 'POST':
        my_new_data = {
            "id": request.form.get("answer_id"),
            "question_id": request.form.get("question_id"),
            "message": request.form.get("message"),
            "edited_count": int(request.form.get("edited_count"))+1
        }
        print(my_new_data)
        data_manager.edit_comment(my_new_data)

        return redirect('/question/' + str(question_id))

    return render_template('edit_comment.html', comment=comment, question_id=str(question_id))


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
