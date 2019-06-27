from flask import request, jsonify
from sqlalchemy import text
from datetime import datetime, timedelta
from session import db, Session, app


@app.route('/')
def hello():
    return "Hello"


# API for receiving event batches (1-10 events / batch)
# Post Json format example,
# {
# 	"Data": [
# 		{"player_id": "584b087454e042688e0ce4f877feb74d", "country": "IS",
# 		"event": "start", "session_id": "9983eb04-5dad-4f2e-ad48-37fa0c0ec296", "ts": "2016-11-26T06:11:36"},
# 		{"player_id": "d6313e1fb7d247a6a034e2aadc30ab3f", "country": "PK",
# 		"event": "start", "session_id": "674606b1-2270-4285-928f-eef4a6b90a60", "ts": "2016-11-22T20:40:50"},
# 		{"player_id": "9b4f8903f38b413d8e3541197e445ff5", "country": "UA",
# 		"event": "start", "session_id": "62fb7773-0bca-41d5-ab91-9963803adf1a", "ts": "2013-11-28T17:45:34"},
# 		{"player_id": "20ac16ebb30a477087c3c7501b1fce73",
# 		"event": "end", "session_id": "16ca9d01-d240-4527-9f8f-00ef6cddb1d4", "ts": "2016-11-18T06:24:50"},
# 		{"player_id": "318e22b061b54042b880c365c28982d0",
# 		"event": "end", "session_id": "5f933591-8cd5-4147-8736-d6237bef5891", "ts": "2016-11-16T18:01:37"},
# 		{"player_id": "29bb390d9b1b4b4b9ec0d6243da34ec4",
# 		"event": "end", "session_id": "ef939180-692a-4845-aef7-afb03524c2da", "ts": "2016-11-13T10:38:09"}
# 		],
# 	"NumberRecord": 6
# }
@app.route('/process-data', methods=['GET', 'POST'])
def post_data():
    # Because the data is limited in 2016, assume the current timestamp is 12/1/2016
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
                        # handle json that doesn't have country
                        if "country" not in _data:
                            _data["country"] = None
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
# ** My understanding to the question is that it requires the last X hours from the current moment,
# ** In this case, country doesn't matter, but I put a sort here.
# http://127.0.0.1:5000/bycountry?hours=20
@app.route('/bycountry', methods=['GET'])
def get_bycountry():
    hours = request.args.get('hours')
    if not hours.isdigit():
        return "Wrong Parameter"

    # Because the data is limited in 2016, assume the current timestamp is 12/1/2016
    # now = datetime.now()
    now = datetime(2016, 12, 1)
    from_ts = now - timedelta(hours=int(hours))
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
    if results:
        for _result in results:
            content = {'player_id': _result[1],
                       'country': _result[2],
                       'event': _result[3],
                       'session_id': _result[4],
                       'ts': _result[5]
                       }
            ret_json.append(content)
        return jsonify(ret_json)
    else:
        return "No data"


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
    if results:
        for _result in results:
            content = {'player_id': _result[1],
                       'country': _result[2],
                       'event': _result[3],
                       'session_id': _result[4],
                       'ts': _result[5]
                       }
            ret_json.append(content)
        return jsonify(ret_json)
    else:
        return "No Data"


if __name__ == '__main__':
    app.run()




