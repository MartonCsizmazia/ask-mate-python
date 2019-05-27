import connection
import util

QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                   SELECT * FROM question
                   ORDER BY submission_time;
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
