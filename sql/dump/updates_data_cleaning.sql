USE new_yemen_looted_artefacts;
UPDATE looted_artefacts
SET period_clean = CASE
    WHEN period_precise IN ('1th century', '1st century') THEN '1st century'
    WHEN period_precise IN ('2 century', '2th century', '2nd century') THEN '2nd century'
    WHEN period_precise IN ('18 century', '18th century') THEN '18th century'
    WHEN period_precise IN ('19 century', '19th century') THEN '19th century'
    WHEN period_precise = 'Islamic medieval' THEN 'Islamic Medieval'
    WHEN period_precise = 'South Arabian antiquity' THEN 'South Arabian Antiquity'
    ELSE period_precise
END;

UPDATE looted_artefacts
SET major_period = CASE
    WHEN period_clean IN ('1st century', '2nd century', '3rd century')
        THEN 'South Arabian Antiquity'
    WHEN period_clean IN ('4th century', '5th century', '6th century')
        THEN 'Late Antiquity'
    WHEN period_clean IN ('7th century', '8th century', '9th century', '10th century',
                          '11th century', '12th century', '13th century', '14th century',
                          '15th century')
        THEN 'Islamic Medieval'
    WHEN period_clean IN ('16th century', '17th century', '18th century', '19th century',
                          '20th century', '21st century')
        THEN 'Post-medieval / Modern'
    WHEN period_clean IN ('South Arabian Antiquity', 'Late Antiquity', 'Islamic Medieval')
        THEN period_clean
    ELSE 'Unclassified'
END;


UPDATE looted_artefacts
SET period_precise = period_clean
WHERE artifact_id IS NOT NULL;

UPDATE looted_artefacts
SET period_general = major_period
WHERE artifact_id IS NOT NULL;

ALTER TABLE looted_artefacts
DROP COLUMN major_period;

ALTER TABLE looted_artefacts
DROP COLUMN period_clean;