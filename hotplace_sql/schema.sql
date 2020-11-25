DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS restaurant;
DROP TABLE IF EXISTS bookmark;

CREATE TABLE users (
  id VARCHAR(50) PRIMARY KEY,
  password VARCHAR(50) NOT NULL,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL
);

CREATE TABLE restaurant (
  restaurant_name VARCHAR(50),
  content VARCHAR(200),
  rating INTEGER NOT NULL,
  locates VARCHAR(50) NOT NULL,
  category VARCHAR(50) NOT NULL,
  PRIMARY KEY(restaurant_name, content)
);



CREATE TABLE bookmark (
  u_id VARCHAR(50),
  r_name VARCHAR(50),
  location VARCHAR(50) NOT NULL,
  category VARCHAR(50) NOT NULL,
  FOREIGN KEY (u_id) REFERENCES users(id),
  FOREIGN KEY (r_name) REFERENCES restaurant(restaurant_name),
  FOREIGN KEY (location) REFERENCES restaurant(locates),
  FOREIGN KEY (category) REFERENCES restaurant(category)  
  PRIMARY KEY (u_id, r_name)
);
