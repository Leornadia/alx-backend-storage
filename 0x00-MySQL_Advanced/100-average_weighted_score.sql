-- 100-average_weighted_score.sql
-- Create the ComputeAverageWeightedScoreForUser stored procedure

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weight FLOAT;
    DECLARE weighted_sum FLOAT;

    SELECT SUM(p.weight) INTO total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = ComputeAverageWeightedScoreForUser.user_id;

    SELECT SUM(c.score * p.weight) / total_weight INTO weighted_sum
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = ComputeAverageWeightedScoreForUser.user_id;

    UPDATE users
    SET average_score = weighted_sum
    WHERE id = ComputeAverageWeightedScoreForUser.user_id;
END //
DELIMITER ;
