USE defaultdb;

-- DROP TABLE animes;

CREATE TABLE IF NOT EXISTS animes (
      id INTEGER PRIMARY KEY NOT NULL,
      title STRING,
      synopsis STRING,
      genre STRING[],
      aired STRING,
      episodes INTEGER,
      members INTEGER,
      popularity REAL,
      ranked INTEGER,
      score REAL,
      img_url STRING,
      link STRING
);