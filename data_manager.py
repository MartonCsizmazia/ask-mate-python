import connection


QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                   SELECT * FROM question
                   ORDER BY submission_time DESC;
                   """)
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_last_5_questions(cursor):
    cursor.execute("""
                   SELECT * FROM question
                   ORDER BY submission_time DESC LIMIT 5;
                   """)
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_question_by_id(cursor, id):
    cursor.execute("""
                   SELECT * FROM question WHERE id = %(id)s;
                   """,
                   {'id': id})
    question = cursor.fetchone()
    return question


@connection.connection_handler
def get_answer_by_question_id(cursor, question_id):
    cursor.execute("""
                   SELECT * FROM answer
                   WHERE question_id = %(question_id)s;
                   """,
                   {'question_id': question_id})
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def get_answer_by_id(cursor, id):
    cursor.execute("""
                   SELECT * FROM answer WHERE id = %(id)s;
                   """,
                   {'id': id})
    question = cursor.fetchone()
    return question


@connection.connection_handler
def get_comments_by_question_id(cursor, question_id):
    cursor.execute("""
                   SELECT * FROM comment
                   WHERE question_id = %(question_id)s
                   ORDER BY submission_time;
                   """,
                   {'question_id': question_id})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def get_comments_by_answer_id(cursor, answer_id):
    cursor.execute("""
                   SELECT * FROM comment WHERE answer_id = %(answer_id)s ORDER BY submission_time;
                   """,
                   {'answer_id': answer_id})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def edit_question(cursor, data):
    cursor.execute("""
                   UPDATE question SET title = %(title)s, message = %(message)s
                   WHERE id = %(id)s;
                   """,
                   {"id": data["id"],
                    "title": data["title"],
                    "message": data["message"]})


@connection.connection_handler
def add_answer(cursor, data):
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image )
                    VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s );
                   """,
                   {"submission_time": data["submission_time"],
                    "vote_number": data["vote_number"],
                    "question_id": data["question_id"],
                    "message": data["message"],
                    "image": data["image"]})


@connection.connection_handler
def question_vote_up(cursor, question_id):
    cursor.execute("""
                   UPDATE question SET vote_number = vote_number + 1
                   WHERE id = %(id)s;
                   """,
                   {"id": question_id})


@connection.connection_handler
def question_vote_down(cursor, question_id):
    cursor.execute("""
                   UPDATE question SET vote_number = vote_number - 1
                   WHERE id = %(id)s;
                   """,
                   {"id": question_id})


@connection.connection_handler
def answer_vote_up(cursor, answer_id):
    cursor.execute("""
                   UPDATE answer SET vote_number = vote_number + 1
                   WHERE id = %(id)s;
                   """,
                   {"id": answer_id})


@connection.connection_handler
def answer_vote_down(cursor, answer_id):
    cursor.execute("""
                   UPDATE answer SET vote_number = vote_number - 1
                   WHERE id = %(id)s;
                   """,
                   {"id": answer_id})


@connection.connection_handler
def delete_answer_by_id(cursor, answer_id):
    cursor.execute("""
                   DELETE FROM answer
                   WHERE id = %(id)s;
                   """,
                   {"id": answer_id})


@connection.connection_handler
def delete_answer_by_question_id(cursor, question_id):
    cursor.execute("""
                   DELETE FROM answer
                   WHERE question_id = %(id)s;
                   """,
                   {"id": question_id})


@connection.connection_handler
def delete_question(cursor, id):
    cursor.execute("""
                   DELETE FROM question
                   WHERE id = %(id)s;
                   """,
                   {"id": id})


@connection.connection_handler
def delete_question_tag(cursor, question_id):
    cursor.execute("""
                   DELETE FROM question_tag
                   WHERE question_id = %(id)s;
                   """,
                   {"id": question_id})


@connection.connection_handler
def add_question(cursor, data):
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image )
                    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s );
                   """,
                   {"submission_time": data["submission_time"],
                    "view_number": data["view_number"],
                    "vote_number": data["vote_number"],
                    "title": data["title"],
                    "message": data["message"],
                    "image": data["image"]})


@connection.connection_handler
def search_question(cursor, search_phrase):
    cursor.execute("""
                   SELECT DISTINCT question.* 
                   FROM question, answer
                   WHERE question.title ILIKE %(text)s 
                   OR question.message ILIKE %(text)s 
                   OR (answer.message ILIKE %(text)s AND answer.question_id=question.id);
                   """,
                   {'text': search_phrase})
    result = cursor.fetchall()
    return result


@connection.connection_handler
def edit_answer(cursor, data):
    cursor.execute("""
                   UPDATE answer SET message = %(message)s
                   WHERE id = %(id)s;
                   """,
                   {"id": data["id"],
                    "message": data["message"]})


@connection.connection_handler
def add_comment(cursor, data):
    cursor.execute("""
                    INSERT INTO comment (submission_time, answer_id, question_id, message)
                    VALUES (%(submission_time)s, %(answer_id)s, %(question_id)s, %(message)s);
                   """,
                   {"submission_time": data["submission_time"],
                    "answer_id": data["answer_id"],
                    "question_id": data["question_id"],
                    "message": data["message"]})


@connection.connection_handler
def add_comment_to_question(cursor, data):
    cursor.execute("""
                    INSERT INTO comment (question_id, message, submission_time)
                    VALUES (%(question_id)s, %(message)s, %(submission_time)s);
                   """,
                   {"question_id": data["question_id"],
                    "message": data["message"],
                    "submission_time": data["submission_time"]})


@connection.connection_handler
def delete_comment_by_id(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment 
                    WHERE id = %(comment_id)s;
                   """,
                   {'comment_id': comment_id})


@connection.connection_handler
def get_comment_by_id(cursor, comment_id):
    cursor.execute("""
                   SELECT * FROM comment WHERE id = %(comment_id)s;
                   """,
                   {'comment_id': comment_id})
    comment = cursor.fetchone()
    return comment


@connection.connection_handler
def get_tags_by_question_id(cursor, id):
    cursor.execute("""
                   SELECT tag.name FROM tag JOIN question_tag 
                   ON question_tag.tag_id=tag.id
                   WHERE question_tag.question_id=%(id)s;
                   """,
                   {'id': id})
    answer = cursor.fetchall()
    return answer


@connection.connection_handler
def get_comments_by_answer_idlist(cursor, answer_ids):
    cursor.execute("""
                   SELECT * FROM comment WHERE answer_id IN %(answer_ids)s ORDER BY submission_time;
                   """,
                   {'answer_ids': answer_ids})
    comments = cursor.fetchall()
    return comments

@connection.connection_handler
def get_comment_by_id(cursor, id):
    cursor.execute("""
                   SELECT * FROM comment WHERE id = %(id)s;
                   """,
                   {'id': id})
    comment = cursor.fetchone()
    return comment

@connection.connection_handler
def edit_comment(cursor, data):
    cursor.execute("""
                   UPDATE comment SET message = %(message)s
                   WHERE id = %(id)s;
                   """,
                   {"id": data["id"],
                    "message": data["message"]})
