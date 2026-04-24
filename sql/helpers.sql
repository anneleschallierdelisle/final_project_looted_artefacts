-- Change a column name
ALTER TABLE web_pages
CHANGE lien_ok link VARCHAR(255);
-- Change a column type
ALTER TABLE mola_artefacts
MODIFY year_returned INT; 
-- Update values within column
UPDATE mola_artefacts
SET year_acquired = NULL
WHERE year_acquired = '' OR year_acquired = ' ';
-- Identify regex char
SELECT year_acquired
FROM mola_artefacts
WHERE year_acquired NOT REGEXP '^[0-9]+$';
-- replace values
UPDATE mola_artefacts
SET date_looted = REPLACE(date_looted, '.0','');
-- drop table, view
DROP VIEW artefacts_scoring;
-- check quickly
SELECT * FROM artefacts_scoring LIMIT 10;
-- TRIM removes sapce around a text
-- TRIM(w.link);
-- DELETE COLUMN
ALTER TABLE web_pages
DROP COLUMN id_page;