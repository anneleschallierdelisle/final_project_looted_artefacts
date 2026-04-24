-- denormalized version of the dataset
CREATE OR REPLACE TABLE `project-bdf0bfdc-ba62-4020-ae1.artifacts_dataset.looted_artifacts_final` AS
FROM EXTERNAL_QUERY(
  "projects/project-bdf0bfdc-ba62-4020-ae1/locations/us-central1/connections/mysql-bq-connection",
  "SELECT la.*, wp.wb_txt_lg, wp.link, wp.main_website, wp.article_id, ms.score_txt, ms.score_img, ms.final_score, ms.score_type, ad.normalized_domain,	ad.city, ad.country,ad.source_classification FROM looted_artefacts la LEFT JOIN web_pages wp ON la.artifact_id = wp.artifact_id LEFT JOIN match_scoring ms ON la.artifact_id = ms.artifact_id   LEFT JOIN art_dealers ad ON wp.main_website = ad.main_website");