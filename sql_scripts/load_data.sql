LOAD DATA LOCAL INFILE 'C:/Users/Utilisateur/Desktop/IRONHACK_DA/COURSES/FINAL_PROJECT/final_project_looted_artefacts/data/clean/match_scoring.csv'
INTO TABLE match_scoring
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(artifact_id, score_txt, score_img, final_score, score_type);
