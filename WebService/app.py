from flask import request, jsonify
from sqlalchemy import text
from datetime import datetime, timedelta
from session import db, Session, app


@app.route('/')
def hello():
    return "Hello"


# By default, a route only answers to GET requests.
# Post Json format example,
# {
# 	"Data": [
# 		{"player_id": "d6313e1fb7d247a6a034e2aadc30ab3f", "country": "PK",
# 		"event": "start", "session_id": "674606b1-2270-4285-928f-eef4a6b90a60", "ts": "2016-11-22T20:40:50"},
# 		{"player_id": "d6313e1fb7d247a6a034e2aadc30ab3f", "country": "PK",
# 		"event": "start", "session_id": "674606b1-2270-4285-928f-eef4a6b90a60", "ts": "2013-11-22T20:40:50"},
# 		{"player_id": "d6313e1fb7d247a6a034e2aadc30ab3f", "country": "PK",
# 		"event": "start", "session_id": "674606b1-2270-4285-928f-eef4a6b90a60", "ts": "2013-11-22T20:40:50"}
# 		],
# 	"NumberRecord": 3
# }
@app.route('/process-data', methods=['GET', 'POST'])
def post_data():
    # Because the data is limited in 2016, assume the current timestamp is 11/1/2016
    # now = datetime.now()
    now = datetime(2016, 12, 1)
    if request.method == 'POST':
        json = request.get_json()
        data_list = json["Data"]
        ret_str = ""
        if data_list:
            for _data in data_list:
                # If data ts is within a year then we keep record
                ts = datetime.strptime(_data["ts"], '%Y-%m-%dT%H:%M:%S')
                if now <= (ts + timedelta(days=365)):
                    try:
                        session = Session(
                            player_id=_data["player_id"],
                            country=_data["country"],
                            event=_data["event"],
                            session_id=_data["session_id"],
                            ts=_data["ts"])
                        db.session.add(session)
                        db.session.commit()
                        ret_str = ret_str + "Session added. {} session id={}\r\n".format(_data["event"],
                                                                                         _data["session_id"])
                    except Exception as e:
                        return str(e)
                else:
                    ret_str = ret_str + "Data is older than a year. Discarded.\r\n"
            return ret_str
        else:
            return 'No Data Provided'
    else:
        return 'get-data'


# API for fetching session starts for the last X (X is defined by the user) hours for each country
# http://127.0.0.1:5000/bycountry?hours=20
@app.route('/bycountry', methods=['GET'])
def get_bycountry():
    # Because the data is limited in 2016, assume the current timestamp is 11/1/2016
    # now = datetime.now()
    now = datetime(2016, 12, 1)
    hours = request.args.get('hours')
    from_ts = now - timedelta(hours=hours)
    sql = """
    SELECT *
    FROM session
    WHERE event = 'start'
    AND TS >= :from_ts 
    ORDER BY country, ts Desc
    """

    # db is SQLAlchemy object
    results = db.engine.execute(text(sql), {"from_ts": from_ts})
    ret_json = []
    for _result in results:
        content = {'player_id': _result[0],
                   'country': _result[1],
                   'event': _result[2],
                   'session_id': _result[3],
                   'ts': _result[4]
                   }
        ret_json.append(content)
    return jsonify(ret_json)


# API for fetching last 20 complete sessions for a given player
# http://127.0.0.1:5000/last20?player=20ac16ebb30a477087c3c7501b1fce73
@app.route('/last20', methods=['GET'])
def get_last20():
    player_id = request.args.get('player')
    sql = """
    SELECT *
    FROM session
    WHERE event = 'end'
    AND player_id = :player_id 
    ORDER BY ts Desc
    LIMIT 20
    """

    # db is SQLAlchemy object
    results = db.engine.execute(text(sql), {"player_id": player_id})
    ret_json = []
    for _result in results:
        content = {'player_id': _result[0],
                   'country': _result[1],
                   'event': _result[2],
                   'session_id': _result[3],
                   'ts': _result[4]
                   }
        ret_json.append(content)
    return jsonify(ret_json)


if __name__ == '__main__':
    app.run()




