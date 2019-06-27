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
  API for receiving event batches (1-10 events / batch).

* **URL**

  /process-data

* **Method:**
  

  `POST` 
  
*  **URL Params**

   <_If URL params exist, specify them in accordance with name mentioned in URL section. Separate into optional and required. Document data constraints._> 

   **Required:**
 
   `id=[integer]`

   **Optional:**
 
   `photo_id=[alphanumeric]`

* **Data Params**

  <_If making a post request, what should the body payload look like? URL Params rules apply here too._>

* **Success Response:**
  
  <_What should the status code be on success and is there any returned data? This is useful when people need to to know what their callbacks should expect!_>

  * **Code:** 200 <br />
    **Content:** `{ id : 12 }`
 
* **Error Response:**

  <_Most endpoints will have many ways they can fail. From unauthorized access, to wrongful parameters etc. All of those should be liste d here. It might seem repetitive, but it helps prevent assumptions from being made where they should be._>

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "Log in" }`

  OR

  * **Code:** 422 UNPROCESSABLE ENTRY <br />
    **Content:** `{ error : "Email Invalid" }`

* **Sample Call:**

  <_Just a sample call to your endpoint in a runnable format ($.ajax call or a curl request) - this makes life easier and more predictable._> 

* **Notes:**

  <_This is where all uncertainties, commentary, discussion etc. can go. I recommend timestamping and identifying oneself when leaving comments here._> 
