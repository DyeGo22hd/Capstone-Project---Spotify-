# Load required libraries
library(DBI)
library(RMariaDB)

# Connection details
endpoint <- "peepify-db.c7swoaco2oxs.us-east-2.rds.amazonaws.com"  # AWS RDS endpoint
port <- 3306                                                       # MySQL port
user <- "peepify"                                                  # Username
password <- "capstone499"                                          # Password
database <- "peepify_data"                                         # Database name

# Establish connection to the database
con <- dbConnect(
  RMariaDB::MariaDB(),
  dbname = database,
  host = endpoint,
  port = port,
  user = user,
  password = password,
  ssl.verify = FALSE
)

# Create tables
tryCatch({
  # Create user_info table
  dbExecute(con, "
  CREATE TABLE IF NOT EXISTS user_info (
      user_id VARCHAR(255) PRIMARY KEY,  -- Unique user identifier
      raw_data_id INT NOT NULL,          -- Foreign key for raw_data
      api_data_id INT NOT NULL           -- Foreign key for api_data
  );
  ")
  print("Table 'user_info' created successfully.")
  
  # Create raw_data table
  dbExecute(con, "
  CREATE TABLE IF NOT EXISTS raw_data (
      raw_data_id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for raw data
      user_id VARCHAR(255) NOT NULL,              -- Associated user
      streaming_history_json BLOB,               -- JSON file for streaming history
      extended_history_json BLOB,                -- JSON file for extended history
      FOREIGN KEY (user_id) REFERENCES user_info(user_id)
  );
  ")
  print("Table 'raw_data' created successfully.")
  
  # Create api_data table
  dbExecute(con, "
  CREATE TABLE IF NOT EXISTS api_data (
      api_data_id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for API data
      user_id VARCHAR(255) NOT NULL,              -- Associated user
      top_artists_json BLOB,                      -- JSON file for top artists
      top_genre_json BLOB,                        -- JSON file for top genres
      streamed_tracks_json BLOB,                  -- JSON file for streamed tracks
      FOREIGN KEY (user_id) REFERENCES user_info(user_id)
  );
  ")
  print("Table 'api_data' created successfully.")
  
  # Disconnect from the database
  dbDisconnect(con)
  print("Disconnected successfully.")
}, error = function(e) {
  print("Error creating tables:")
  print(e$message)
  dbDisconnect(con)
})
