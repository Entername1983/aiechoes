-- Create Replies Table
CREATE TABLE replies (
    id SERIAL PRIMARY KEY,
    time_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    model VARCHAR(50) NOT NULL,
    reply VARCHAR(512) NOT NULL,
    version VARCHAR(50) NOT NULL,
    batch_id INTEGER NOT NULL,
    number_in_batch INTEGER NOT NULL
);

-- Create Images Table
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    batch_id INTEGER NOT NULL,
    title VARCHAR(128),
    image_url VARCHAR(255) NOT NULL,
    thumbnail_url VARCHAR(255),
    img_model VARCHAR(30) NOT NULL,
    time_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
