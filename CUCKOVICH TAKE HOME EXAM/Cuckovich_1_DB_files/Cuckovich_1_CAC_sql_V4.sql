-- Look at the data
SELECT COUNT(*) 
FROM esg_scores -- 7125

SELECT * 
FROM esg_scores
LIMIT 10

SELECT COUNT(*)
FROM id_map -- 9876

SELECT * 
FROM id_map
LIMIT 10

SELECT COUNT(*)
FROM sp500 -- 500

SELECT * 
FROM sp500
LIMIT 10

--DROP table sp500_esg_scores
-- Should I make id a primary key?  UNIQUE?
CREATE TABLE sp500_esg_scores (
id bigint NOT NULL,
instr_id text,
total_score numeric(15,6),
e_score numeric(15,6),
s_score numeric(15,6),
g_score numeric(15,6),
name text -- if it were me, I would use org_name or something more descriptive and not a keyword
);

-- Do instr_ids from two tables have differences? -- 9876 same as id_map
-- I think I am supposed to only include sp500 companies, otherwise, why include that table 
    -- since it has no additional values
-- I would ask the person who gave me the instructions to confirm
SELECT DISTINCT instr_id
FROM sp500 SP
FULL JOIN id_map IM
USING(instr_id);


-- left join will be quick -- sp500 only has 500 rows
INSERT INTO sp500_esg_scores
(id, instr_id, name, total_score, e_score, s_score, g_score)
SELECT IM.id,
IM.instr_id,
IM.name,
ESG.total_score,
ESG.e_score, 
ESG.s_score, 
ESG.g_score
FROM sp500 SP
LEFT JOIN id_map IM
ON SP.instr_id = IM.instr_id
LEFT JOIN esg_scores ESG
ON IM.id = ESG.id

-- OK I HAVE 500 ROWS IN THE TABLE NOW
SELECT * FROM sp500_esg_scores

-- Add a column rank for total_score percentile
ALTER TABLE sp500_esg_scores
ADD rank numeric DEFAULT 0 -- I might call it score_rank instead of rank because rank feels like a keyword

WITH v_sp500_esg_scores AS
(
    SELECT PERCENT_RANK() OVER (
	ORDER BY total_score ASC
	) AS rank, id
	FROM sp500_esg_scores
) 
UPDATE sp500_esg_scores SET rank = v_sp500_esg_scores.rank
FROM v_sp500_esg_scores
WHERE sp500_esg_scores.id = v_sp500_esg_scores.id;  

-- Null values should be set to 0
UPDATE sp500_esg_scores SET rank = 0
WHERE sp500_esg_scores.total_score IS NULL;  

-- Add a MEDIAN scores row
-- I used an id of 0 assuming that no id would be < 1 but maybe -1 would be safer?
INSERT INTO sp500_esg_scores
(id, instr_id, total_score, e_score, s_score, g_score, name, rank)
VALUES
(0, 'MEDIAN', 
 (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY total_score) FROM sp500_esg_scores), 
 (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY e_score) FROM sp500_esg_scores), 
 (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY s_score) FROM sp500_esg_scores), 
 (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY g_score) FROM sp500_esg_scores),
 'MEDIAN',
 (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY rank) FROM sp500_esg_scores)
)

-- Look at the MEDIAN scores row
SELECT * 
FROM sp500_esg_scores
WHERE id = 0;

-- Look at the data
SELECT * FROM sp500_esg_scores
ORDER BY rank ASC
