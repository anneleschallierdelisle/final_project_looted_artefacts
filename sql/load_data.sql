SET GLOBAL local_infile = 1;
LOAD DATA LOCAL INFILE 'C:/Users/Utilisateur/Desktop/web_pages.csv'
INTO TABLE web_pages
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(artifact_id, text_for_matching_web, price, currency,  wb_txt_shrt, wb_txt_lg, link, main_website, article_id);
