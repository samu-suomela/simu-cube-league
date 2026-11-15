CREATE TABLE players (
    id          INT PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE
);

CREATE TABLE matches (
    event_date  DATE NOT NULL,
    round       INT NOT NULL CHECK (round > 0),
    player1     INT NOT NULL REFERENCES players (id),
    player2     INT NOT NULL REFERENCES players (id),
    wins_p1     INT NOT NULL CHECK (wins_p1 >= 0),
    wins_p2     INT NOT NULL CHECK (wins_p2 >= 0),
    g1_on_play  INT NOT NULL REFERENCES players (id),
    PRIMARY KEY (event_date, round, player1),
    CHECK (player1 <> player2),
    CHECK (g1_on_play IN (player1, player2))
);