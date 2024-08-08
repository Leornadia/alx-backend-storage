-- 7-average_score.sql
-- Create the ComputeAverageScoreForUser stored procedure

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE avg_score FLOAT;
    
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = ComputeAverageScoreForUser.user_id;
    
    UPDATE users
    SET average_score = avg_score
    WHERE id = ComputeAverageScoreForUser.user_id;
END //
DELIMITER ;
