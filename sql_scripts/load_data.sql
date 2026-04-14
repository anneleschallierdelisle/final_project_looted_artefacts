LOAD DATA LOCAL INFILE 'C:/Users/Utilisateur/Desktop/IRONHACK_DA/COURSES/FINAL_PROJECT/final_project_looted_artefacts/data/clean/argh/web_pages_rgx.csv'
INTO TABLE web_pages
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(artifact_id, text_for_matching_web, id_page, price, currency,  wb_txt_shrt, wb_txt_lg, lien_ok, main_website, article_id);
