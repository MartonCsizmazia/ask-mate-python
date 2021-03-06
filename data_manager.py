import connection
import util
from psycopg2 import sql
from flask import session


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
def get_table_by_id(cursor, id, input_table):
    cursor.execute(
            sql.SQL("""
                   SELECT * FROM {table} WHERE id = %(id)s;
                   """).format(table=sql.Identifier(input_table)),
                   {'id': id}
                   )
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
                   UPDATE question SET title = %(title)s, message = %(message)s, image = %(image)s
                   WHERE id = %(id)s;
                   """,
                   {"id": data["question_id"],
                    "title": data["title"],
                    "message": data["message"],
                    "image": data["image"]})


@connection.connection_handler
def add_answer(cursor, data):
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id )
                    VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s, %(user_id)s);
                   """,
                   {"submission_time": util.date_now(),
                    "vote_number": 0,
                    "question_id": data["question_id"],
                    "message": data["answer-message"],
                    "image": data["image"],
                    "user_id": get_user_id_by_username(session['username'])})


@connection.connection_handler
def add_new_user(cursor, data):
    cursor.execute("""
                        INSERT INTO users (username, creation_date, password)
                        VALUES (%(username)s, %(creation_date)s,  %(password)s);
                       """,
                   {"username": data["username"],
                    "creation_date": util.date_now(),
                    "password": util.hash_password(data["password"])})


@connection.connection_handler
def vote(cursor, table_name, vote_value, id):
    cursor.execute(
            sql.SQL("""
                   UPDATE {table} SET vote_number = vote_number + %(vote_value)s
                   WHERE id = %(id)s;
                   """).format(table=sql.Identifier(table_name)),
                   {"id": id,
                    "vote_value": vote_value})


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
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id )
                    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s, %(user_id)s );
                   """,
                   {"submission_time": util.date_now(),
                    "view_number": 0,
                    "vote_number": 0,
                    "title": data["title"],
                    "message": data["message"],
                    "image": data["image"],
                    "user_id": get_user_id_by_username(session["username"])})


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
                   UPDATE answer SET message = %(message)s, image = %(image)s
                   WHERE id = %(id)s;
                   """,
                   {"id": data["answer_id"],
                    "message": data["message"],
                    "image": data["image"]})


@connection.connection_handler
def add_comment_to_answer(cursor, data):
    cursor.execute("""
                    INSERT INTO comment (submission_time, answer_id, message, edited_count, user_id)
                    VALUES (%(submission_time)s, %(answer_id)s, %(message)s, %(edited_count)s, %(user_id)s);
                   """,
                   {"submission_time": util.date_now(),
                    "answer_id": data["answer_id"],
                    "message": data["comment-message"],
                    "edited_count": 0,
                    "user_id": get_user_id_by_username(session['username'])})


@connection.connection_handler
def add_comment_to_question(cursor, data):
    cursor.execute("""
                    INSERT INTO comment (question_id, message, submission_time, edited_count, user_id)
                    VALUES (%(question_id)s, %(message)s, %(submission_time)s, %(edited_count)s, %(user_id)s);
                   """,
                   {"question_id": data["question_id"],
                    "message": data["comment-message"],
                    "submission_time": util.date_now(),
                    "edited_count": 0,
                    "user_id": get_user_id_by_username(session['username'])})


@connection.connection_handler
def delete_from_table_by_id(cursor, id, input_table):
    cursor.execute(
        sql.SQL("""
                DELETE FROM {table}
                WHERE id = %(id)s;""").format(table=sql.Identifier(input_table)),
                {'id': id})


@connection.connection_handler
def get_tags_by_question_id(cursor, id):
    cursor.execute("""
                   SELECT tag.* FROM tag JOIN question_tag 
                   ON question_tag.tag_id=tag.id
                   WHERE question_tag.question_id=%(id)s;
                   """,
                   {'id': id})
    tags = cursor.fetchall()
    return tags


@connection.connection_handler
def get_all_tags(cursor):
    cursor.execute("""
                   SELECT name FROM tag 
                   """)
    tags = cursor.fetchall()
    return tags


@connection.connection_handler
def add_new_tag_to_tags(cursor, new_tag):
    cursor.execute("""
                   INSERT INTO tag (name)
                   SELECT %(name)s 
                   WHERE NOT EXISTS( SELECT * FROM tag WHERE name = %(name)s);
                   """,
                   {'name': new_tag})


@connection.connection_handler
def get_tag_id(cursor, name):
    cursor.execute("""
                   SELECT id 
                   FROM tag
                   WHERE name = %(name)s;
                   """,
                   {'name': name})
    id = cursor.fetchone()
    return id


@connection.connection_handler
def add_new_tag_to_question(cursor, question_id, tag_id):
    cursor.execute("""
                   INSERT INTO question_tag (question_id, tag_id)
                   VALUES (%(question_id)s, %(tag_id)s)
                   ON CONFLICT DO NOTHING;
                   """,
                   {'question_id': question_id,
                    'tag_id': tag_id})


@connection.connection_handler
def delete_tag_from_question(cursor, tag_id):
    cursor.execute("""
                   DELETE FROM question_tag
                   WHERE tag_id = %(tag_id)s;
                   """,
                   {'tag_id': tag_id})


@connection.connection_handler
def get_comments_by_answer_idlist(cursor, answer_ids):
    cursor.execute("""
                   SELECT * FROM comment WHERE answer_id IN %(answer_ids)s ORDER BY submission_time;
                   """,
                   {'answer_ids': answer_ids})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def edit_comment(cursor, data):
    cursor.execute("""
                   UPDATE comment SET message = %(message)s, edited_count = edited_count+1 
                   WHERE id = %(id)s;
                   """,
                   {"id": data["answer_id"],
                    "message": data["message"]})


@connection.connection_handler
def list_users(cursor):
    cursor.execute("""
                   SELECT * FROM users 
                   """)
    users = cursor.fetchall()
    return users


@connection.connection_handler
def get_hashed_password_for_user(cursor, username):
    cursor.execute("""
                   SELECT password FROM users
                   WHERE username = %(username)s 
                   """,
                   {'username': username})
    result = cursor.fetchone()
    return result['password']


@connection.connection_handler
def get_user_id_by_username(cursor, username):
    cursor.execute("""
                   SELECT user_id FROM users
                   WHERE username = %(username)s 
                   """,
                   {'username': username})
    result = cursor.fetchone()
    return result['user_id']


@connection.connection_handler
def list_tags(cursor):
    cursor.execute("""
                   SELECT DISTINCT name, count(question_id) AS number FROM tag
                   JOIN question_tag ON (tag_id=id) 
                   group by name
                   ORDER BY number DESC
                   """)
    tags = cursor.fetchall()
    return tags


@connection.connection_handler
def get_comments_by_user_id(cursor, user_id):
    cursor.execute("""
                   SELECT c.question_id, answer_id, c.message, c.submission_time, c.edited_count, a.question_id as new_q_id
                   FROM comment c LEFT JOIN answer a on c.answer_id = a.id
                   WHERE c.user_id = %(user_id)s
                   """,
                   {'user_id': user_id})
    result = cursor.fetchall()
    return result


@connection.connection_handler
def get_data_by_user_id(cursor, user_id, input_table):
    cursor.execute(
           sql.SQL("""
                   SELECT * FROM {table}
                   WHERE user_id = %(user_id)s 
                   """).format(table=sql.Identifier(input_table)),
                   {'user_id': user_id})
    result = cursor.fetchall()
    return result




