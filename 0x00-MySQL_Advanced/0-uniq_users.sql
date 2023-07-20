--We are all unique!


--If table exist ignore the error and continue
CREATE TABLE IF NOT EXIST users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255)
);
