CREATE TABLE IF NOT EXISTS countries(
    id SERIAL PRIMARY KEY,
    country varchar(50) NOT NULL,
    slug varchar(50) NOT NULL,
    iso2 varchar(3) NOT NULL
)