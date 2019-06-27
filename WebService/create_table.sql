--DROP TABLE session;

CREATE TABLE session
(
  id SERIAL PRIMARY KEY,
  player_id VARCHAR (50) NOT NULL,
  country VARCHAR (10) NULL,
  event VARCHAR (10) NOT NULL,
  session_id VARCHAR (255) NOT NULL,
  ts TIMESTAMP  NOT NULL
);
--
--INSERT INTO session (player_id, country, event, session_id, ts)
--values
--('d6313e1fb7d247a6a034e2aadc30ab3f', 'PK', 'start', '674606b1-2270-4285-928f-eef4a6b90a60', '2016-11-22T20:40:50'::timestamp),
--('20ac16ebb30a477087c3c7501b1fce73', null, 'end', '16ca9d01-d240-4527-9f8f-00ef6cddb1d4', '2016-11-18T06:24:50'::timestamp);
