-- artefacts scoring endpoint
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

-- looted artefacts in the world
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