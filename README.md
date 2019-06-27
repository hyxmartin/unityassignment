**unityassignment**
----
  API for receiving event batches (1-10 events / batch).

* **URL**

  /process-data

* **Method:**
  
  `POST` 

* **Data Params and sample request**

  {
	"Data": [
		{"player_id": "d6313e1fb7d247a6a034e2aadc30ab3f", "country": "PK", "event": "start", "session_id": "674606b1-2270-4285-928f-eef4a6b90a60", "ts": "2016-11-22T20:40:50"},
		{"player_id": "d6313e1fb7d247a6a034e2aadc30ab3f", "country": "PK", "event": "start", "session_id": "674606b1-2270-4285-928f-eef4a6b90a60", "ts": "2013-11-22T20:40:50"},
		{"player_id": "d6313e1fb7d247a6a034e2aadc30ab3f", "country": "PK", "event": "start", "session_id": "674606b1-2270-4285-928f-eef4a6b90a60", "ts": "2013-11-22T20:40:50"}
		],
	"NumberRecord": 3
}

* **Success Response:**
  
  Session added. ["event"] session id=["session_id"]

----
  API for fetching session starts for the last X (X is defined by the user) hours for each country

* **URL**

  /bycountry

* **Method:**
  
  `GET` 
  
*  **URL Params**

   hours

   **Required:**
 
   `hours=[integer]`


* **Success Response:**
  
  Json Array

* **Sample Call:**

  /bycountry?hours=24

----
  API for fetching last 20 complete sessions for a given player

* **URL**

  /last20

* **Method:**
  
  `GET` 
  
*  **URL Params**

   player

   **Required:**
 
   `hours=[String]`


* **Success Response:**
  
  Json Array

* **Sample Call:**

  /last20?player=20ac16ebb30a477087c3c7501b1fce73

