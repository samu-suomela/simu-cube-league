CREATE VIEW player_matches AS
SELECT
  event_date,
  round,
  player1 AS player,
  player2 AS opponent,
  CASE
    WHEN wins_p1 > wins_p2 THEN 'win'
    WHEN wins_p1 < wins_p2 THEN 'loss'
    ELSE 'draw'
  END AS outcome,
  wins_p1 AS wins,
  wins_p2 AS losses,
  CASE
    WHEN g1_on_play = player1 THEN player1
    ELSE player2
  END AS g1_on_play
FROM
  matches
UNION ALL
SELECT
  event_date,
  round,
  player2 AS player,
  player1 AS opponent,
  CASE
    WHEN wins_p1 > wins_p2 THEN 'loss'
    WHEN wins_p1 < wins_p2 THEN 'win'
    ELSE 'draw'
  END AS outcome,
  wins_p2 AS wins,
  wins_p1 AS losses,
  CASE
    WHEN g1_on_play = player2 THEN player2
    ELSE player1
  END AS g1_on_play
FROM
  matches
;

CREATE VIEW player_records AS
SELECT
  player,
  COUNT(DISTINCT event_date)                                        AS drafts,
  COUNT(*)                                                          AS n_matches,
  COUNT(*) FILTER (WHERE outcome = 'win')                           AS match_wins,
  COUNT(*) FILTER (WHERE outcome = 'loss')                          AS match_losses,
  COUNT(*) FILTER (WHERE outcome = 'draw')                          AS match_draws,
  COUNT(*) FILTER (WHERE outcome = 'win') * 1.0 / COUNT(*)          AS match_win_rate,
  SUM(wins)                                                         AS game_wins,
  SUM(losses)                                                       AS game_losses,
  SUM(wins) * 1.0 / NULLIF(SUM(wins) + SUM(losses), 0)              AS game_win_rate,
  COUNT(*) FILTER (WHERE g1_on_play = player)                       AS matches_g1_play,
  COUNT(*) FILTER (WHERE g1_on_play = player AND outcome = 'win')   AS wins_g1_play,
  COUNT(*) FILTER (WHERE g1_on_play <> player)                      AS matches_g1_draw,
  COUNT(*) FILTER (WHERE g1_on_play <> player AND outcome = 'win')  AS wins_g1_draw,
  wins_g1_play / NULLIF(matches_g1_play, 0)                         AS winrate_g1_play,
  wins_g1_draw / NULLIF(matches_g1_draw, 0)                         AS winrate_g1_draw
FROM 
  player_matches
GROUP BY 
  player
;

CREATE VIEW player_records_per_event AS
SELECT
  event_date,
  player,
  COUNT(*)                                                    AS n_matches,
  COUNT(*) FILTER (WHERE outcome = 'win')                     AS match_wins,
  COUNT(*) FILTER (WHERE outcome = 'loss')                    AS match_losses,
  COUNT(*) FILTER (WHERE outcome = 'draw')                    AS match_draws,
  COUNT(*) FILTER (WHERE outcome = 'win') * 1.0 / COUNT(*)    AS match_win_rate,
  SUM(wins)                                                   AS game_wins,
  SUM(losses)                                                 AS game_losses,
  SUM(wins) * 1.0 / NULLIF(SUM(wins) + SUM(losses), 0)        AS game_win_rate
FROM 
  player_matches
GROUP BY 
  player,
  event_date
;

CREATE VIEW head_to_head AS
SELECT
  player,
  opponent,
  COUNT(*)                                                  AS n_matches,
  COUNT(*) FILTER (WHERE outcome = 'win')                   AS match_wins,
  COUNT(*) FILTER (WHERE outcome = 'loss')                  AS match_losses,
  COUNT(*) FILTER (WHERE outcome = 'draw')                  AS match_draws,
  SUM(wins)                                                 AS game_wins,
  SUM(losses)                                               AS game_losses,
  COUNT(*) FILTER (WHERE outcome = 'win') * 1.0 / COUNT(*)  AS match_win_rate,
  SUM(wins) * 1.0 / NULLIF(SUM(wins) + SUM(losses), 0)      AS game_win_rate
FROM 
  player_matches
GROUP BY 
  player, 
  opponent
;

-- a player in two matches in the same round
CREATE VIEW check_double_booked AS
SELECT 
  event_date, 
  round, 
  player, 
  COUNT(*) AS n_matches
FROM 
  player_matches
GROUP BY 
  event_date, 
  round, 
  player
HAVING 
  COUNT(*) > 1
;

-- rounds that don't run 1..N (usually a mistyped round number)
CREATE VIEW check_round_gaps AS
SELECT 
  event_date, 
  MAX(round) AS max_round, 
  COUNT(DISTINCT round) AS distinct_rounds
FROM 
  player_matches
GROUP BY 
  event_date
HAVING 
  MAX(round) <> COUNT(DISTINCT round)
;

-- an event with fewer than 2 matches (usually a mistyped folder date)
CREATE VIEW check_thin_events AS
SELECT 
  event_date, 
  CAST(COUNT(*) / 2 AS INTEGER) AS n_matches
FROM 
  player_matches
GROUP BY 
  event_date
HAVING 
  COUNT(*) < 4
;

CREATE VIEW check_g1_on_play AS
SELECT 
  player,
  opponent,
  g1_on_play
FROM 
  player_matches
WHERE NOT
  (player = g1_on_play OR opponent = g1_on_play)
;

CREATE VIEW check_players_are_different AS
SELECT 
  player,
  opponent
FROM 
  player_matches
WHERE
  player = opponent
;