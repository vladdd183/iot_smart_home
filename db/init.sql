DROP TABLE IF EXISTS devices;

CREATE TABLE devices (
  id SERIAL PRIMARY KEY,
  topic varchar(255) NOT NULL,
  name varchar(255) NOT NULL,
  data varchar(255),
  dev_type varchar(255) NOT NULL);


DROP TABLE IF EXISTS logs;

CREATE TABLE logs (
  topic varchar(255) NOT NULL,
  name varchar(255) NOT NULL,
  data varchar(255),
  log_data varchar(255) NOT NULL,
  timestemp varchar(255) NOT NULL PRIMARY KEY);
