USE defaultdb;

CREATE EXTENSION pg_trgm;

CREATE TABLE IF NOT EXISTS animes (
      id INTEGER PRIMARY KEY NOT NULL,
      title STRING,
      synopsis STRING,
      genre STRING[],
      aired STRING,
      episodes INTEGER,
      members INTEGER,
      popularity INTEGER,
      ranked INTEGER,
      score REAL,
      img_url STRING,
      link STRING
);