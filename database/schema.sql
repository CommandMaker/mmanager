CREATE TABLE IF NOT EXISTS artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    folder_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS covers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS albums (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    folder_name VARCHAR(255) NOT NULL,
    release_year VARCHAR(255) NOT NULL,
    artist_id INTEGER NOT NULL,
    cover_id INTEGER,

    FOREIGN KEY (artist_id) REFERENCES artists (id) ON DELETE CASCADE,
    FOREIGN KEY (cover_id) REFERENCES covers (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS genres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    album_id INTEGER NOT NULL,
    music_id INTEGER, -- Deezer music id, used for download songs using deezer-downloader
    source_id INTEGER NOT NULL, -- The source where the music is on, refer to the music_sources table for list of values
    track_number INTEGER,
    genre_id INTEGER,
    album_artist_id INTEGER,
    composer_id INTEGER,
    disc_number INTEGER,

    FOREIGN KEY (album_id) REFERENCES albums (id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES music_sources (id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres (id) ON DELETE SET NULL,
    FOREIGN KEY (album_artist_id) REFERENCES artists (id) ON DELETE CASCADE,
    FOREIGN KEY (composer_id) REFERENCES artists (id) ON DELETE CASCADE
);
