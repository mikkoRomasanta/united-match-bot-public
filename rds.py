# Access AWS RDS MYSQL
import os

import pymysql
from dotenv import load_dotenv

load_dotenv()
DB = os.getenv('DB')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

db = pymysql.connect(HOST, USERNAME, PASSWORD, DB)
cur = db.cursor()


def prediction_time_start(match_time):
    sql = '''INSERT INTO prediction_status(status,date) values(1,%s)'''

    cur.execute(sql, match_time)
    db.commit()
    response = '----- You can now make your predictions! -----'
    return response


def register_user(username):
    sql = '''INSERT INTO users(username,points) values(%s,100)'''

    try:
        cur.execute(sql, username)
        db.commit()
        return True
    except BaseException:
        return False


def prediction_time_end():
    # get latest prediction
    sql = '''SELECT * FROM prediction_status ORDER BY id DESC LIMIT 1'''
    cur.execute(sql)
    result = cur.fetchone()

    # check if prediction_status is active
    if result[1] == 1:
        sql = '''UPDATE prediction_status SET status = 0 WHERE id = %s'''
        cur.execute(sql, result[0])
        db.commit()
        response = '----- Prediction time ended! -----'
    else:
        response = 'Prediction time has already ended'

    return response


def prediction_enter(username, pred):
    # split prediction
    entry = pred.split('/')

    # check if user is registered
    sql = '''SELECT * FROM users WHERE username = %s'''
    cur.execute(sql, username)
    user = cur.fetchone()

    # check if prediction is open
    sql = '''SELECT * FROM prediction_status ORDER BY id DESC LIMIT 1'''
    cur.execute(sql)
    prediction_status = cur.fetchone()

    # check is user already has entry for prediction period
    sql = '''SELECT * FROM prediction_entries WHERE user_id=%s AND date=%s'''
    cur.execute(sql, (user[0], prediction_status[2]))
    user_entry = cur.fetchone()

    # process
    if user is not None:
        if prediction_status[1] == 1:
            if user_entry is None:
                sql = '''INSERT INTO prediction_entries(user_id,result_prediction, score_prediction, date)
                values(%s,%s,%s,%s)'''
                cur.execute(
                    sql,
                    (user[0],
                        entry[1],
                        entry[0],
                        prediction_status[2]))
                db.commit()
                response = f'Prediction entered. United: {entry[0]} | Score: Utd {entry[1]}'
            else:
                response = "You already have an entry. NO CHEATING!"
        else:
            response = 'Predictions are currently closed'
    else:
        response = 'You are not registered'

    return response


def end_match(stat):
    result = stat.split('/')

    # get latest prediction status for the date
    sql = '''SELECT * FROM prediction_status ORDER BY id DESC LIMIT 1'''
    cur.execute(sql)
    prediction_date = cur.fetchone()

    # insert result to database
    sql = ''' INSERT INTO prediction_results(result,date) values(%s,%s)'''
    cur.execute(sql, (stat, prediction_date[2]))
    db.commit()

    # check if tally is already done
    sql = '''SELECT * FROM prediction_results WHERE date = %s'''
    cur.execute(sql, prediction_date[2])
    result_status = cur.fetchone()

    # tally points
    sql = '''SELECT * FROM prediction_entries WHERE date = %s'''
    cur.execute(sql, prediction_date[2])
    entries = cur.fetchall()
    response = '----- POINTS AWARDED -----'

    if result_status is None:
        for row in entries:
            print(row)
            score = 0
            # if result(W|L|D) is correct +100
            if row[2] == result[0]:
                score += 100
                if row[3] == result[1]:  # if score is correct bonus +50
                    score += 50

                # award points
                sql = '''UPDATE users SET points = points + %s WHERE id = %s'''
                cur.execute(sql, (score, row[1]))
                db.commit()
                # get username
                sql = '''SELECT * FROM users where id = %s'''
                cur.execute(sql, row[1])
                username = cur.fetchone()

                response += f'\n     {username[2]} + {score}'
            else:
                response = 'No points awarded'
    else:
        response = 'Points were already tallied'

    return response


def show_scores():  # show leaderboard. Limited to 5 for now
    sql = '''SELECT * FROM users ORDER BY points DESC LIMIT 5'''
    cur.execute(sql)
    user = cur.fetchall()
    response = '----- LEADER BOARD -----'
    if user is not None:
        for i in range(len(user)):
            response += f'\nTOP {i+1}: {user[i][2]} \tScore: {user[i][1]}'
        return response


if __name__ == "__main__":
    show_scores()
