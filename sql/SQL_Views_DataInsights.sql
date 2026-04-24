-- This sql file includes 2 views for API flask and 5 scripts to dive into the data --
-- artefacts scoring (for API Flask)
CREATE VIEW artefacts_scoring AS
SELECT 
ms.artifact_id, 
ms.score_txt, 
ms.score_img,
l.pdf_name,
l.page_num,
l.pdf_upgrd_description,
w.wb_txt_lg, 
w.link
FROM match_scoring ms
JOIN looted_artefacts l ON ms.artifact_id = l.artifact_id
JOIN web_pages w ON ms.artifact_id = w.artifact_id
WHERE w.link IS NOT NULL AND TRIM(w.link) != '';

-- looted artefacts in the world (for API Flask)
CREATE VIEW looted_identified_artefacts AS
SELECT 
w.artifact_id, 
w.link,
a.normalized_domain,
a.city,
a.country,
a.source_classification

FROM web_pages w
JOIN art_dealers a ON w.main_website = a.main_website;

-- Most represented looted artifact's types - TOP 5 
SELECT count(*), type FROM looted_artefacts
GROUP BY type
ORDER BY count(*) DESC LIMIT 5;

-- Most represented centuries (no limit, only ordering)
SELECT period_precise, count(*) FROM looted_artefacts
WHERE period_precise != 'Unknown'
GROUP BY period_precise
ORDER BY count(*) DESC;

-- Assign a specific rank for countries in  high-risk level UNESCO sites in danger based on both volume and percentage (cte)
WITH cte_ranked AS 
(SELECT *, DENSE_RANK() OVER (ORDER BY yes_danger DESC) AS Rank_nb,
DENSE_RANK() OVER (ORDER BY percent_danger DESC) AS Rank_pct
FROM unesco_sites_in_danger)
SELECT states_name_en, no_danger, yes_danger, percent_danger,
(Rank_nb * Rank_pct) AS final_rank
FROM cte_ranked;


-- Calculate the average number of years it for each sending country to return looted artifacts along with number of artifacts
WITH cte_duration AS 
(SELECT sending_country, year_returned, year_acquired,
year_returned - year_acquired as return_duration
FROM mola_artefacts)
SELECT sending_country, count(*), round(avg(return_duration),0) as avg_duration FROM cte_duration
WHERE return_duration IS NOT NULL
GROUP BY sending_country
ORDER BY avg_duration DESC;

-- Number of looted artefacts per art dealer
SELECT 
    a.normalized_domain,
    COUNT(w.artifact_id) AS n_artifacts
FROM art_dealers a
JOIN web_pages w 
    ON a.main_website = w.main_website
GROUP BY a.normalized_domain
ORDER BY n_artifacts DESC limit 5;

