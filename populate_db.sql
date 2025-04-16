-- Create Replies Table
CREATE TABLE replies (
    id SERIAL PRIMARY KEY,
    time_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    model VARCHAR(50) NOT NULL,
    reply VARCHAR(512) NOT NULL,
    version VARCHAR(50) NOT NULL,
    batch_id INTEGER NOT NULL,
    number_in_batch INTEGER NOT NULL,
    story_id INTEGER NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
);

-- Create Images Table
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    batch_id INTEGER NOT NULL,
    title VARCHAR(128),
    image_url VARCHAR(255) NOT NULL,
    thumbnail_url VARCHAR(255),
    img_model VARCHAR(30) NOT NULL,
    time_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    story_id INTEGER NOT NULL REFERENCES stories(id) ON DELETE CASCADE
);

-- Create Stories Table
CREATE TABLE stories (
    id SERIAL PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    live BOOLEAN,
    story_type VARCHAR(30) NOT NULL
);

-- Create Story contexts Table
CREATE TABLE story_contexts (
    id SERIAL PRIMARY KEY,
    story_id INTEGER NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    context JSONB NOT NULL
);