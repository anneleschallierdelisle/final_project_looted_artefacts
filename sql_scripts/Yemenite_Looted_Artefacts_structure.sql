USE yemen_looted_artefacts;
SET SESSION sql_mode = '';
CREATE TABLE IF NOT EXISTS `looted_artefacts` (
	`artifact_id` VARCHAR(255) NOT NULL,
	`type` VARCHAR(255),
	`detail` VARCHAR(255),
	`material` VARCHAR(255),
	`iconography` VARCHAR(255),
	`period_general` VARCHAR(255),
	`period_precise` VARCHAR(255),
	`pdf_name` VARCHAR(255),
	`page_num` INT,
	`pdf_upgrd_description` TEXT,
	PRIMARY KEY(`artifact_id`)
);

CREATE TABLE IF NOT EXISTS `art_dealers` (
	`main_website` VARCHAR(255) NOT NULL,
	`normalized_domain` VARCHAR(255),
	`city` VARCHAR(255),
	`country` VARCHAR(255),
	`source_classification` VARCHAR(255),
	PRIMARY KEY(`main_website`)
);

CREATE TABLE IF NOT EXISTS `web_pages` (
	`article_id` INT NOT NULL,
	`artifact_id` VARCHAR(255),
	`text_for_matching_web` TEXT,
	`id_page` INT,
	`price` FLOAT,
	`currency` VARCHAR(255),
	`wb_txt_shrt` TEXT,
	`wb_txt_lg` TEXT,
	`lien_ok` VARCHAR(255),
	`main_website` VARCHAR(255),
	PRIMARY KEY(`article_id`)
);

CREATE TABLE IF NOT EXISTS `web_photos` (
	`image_name` VARCHAR(255) NOT NULL,
	`article_id` INT NOT NULL,
	`artifact_id` VARCHAR(255),
	`image_path` TEXT,
	PRIMARY KEY(`image_name`)
);

CREATE TABLE IF NOT EXISTS `pdf_images` (
	`image_name` VARCHAR(255) NOT NULL,
	`artifact_id` VARCHAR(255),
	`image_path` TEXT,
	PRIMARY KEY(`image_name`)
);

CREATE TABLE IF NOT EXISTS `match_scoring` (
	`index` INT NOT NULL AUTO_INCREMENT,
	`score_txt` FLOAT,
	`score_img` FLOAT,
	`final_score` FLOAT,
	`score_type` VARCHAR(255),
	`artifact_id` VARCHAR(255),
	PRIMARY KEY(`index`)
);

ALTER TABLE `match_scoring`
ADD FOREIGN KEY(`artifact_id`) REFERENCES `looted_artefacts`(`artifact_id`);

ALTER TABLE `pdf_images`
ADD FOREIGN KEY(`artifact_id`) REFERENCES `looted_artefacts`(`artifact_id`);

ALTER TABLE `web_pages`
ADD FOREIGN KEY(`artifact_id`) REFERENCES `looted_artefacts`(`artifact_id`);

ALTER TABLE `web_photos`
ADD FOREIGN KEY(`article_id`) REFERENCES `web_pages`(`article_id`);

ALTER TABLE `web_pages`
ADD FOREIGN KEY(`main_website`) REFERENCES `art_dealers`(`main_website`);