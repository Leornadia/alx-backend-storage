-- 101-average_weighted_score.sql
-- Create the ComputeAverageWeightedScoreForUsers stored procedure

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE total_users INT;
    DECLARE user_id INT;
    DECLARE total_weight FLOAT;
    DECLARE weighted_sum FLOAT;

    -- Declare a cursor to iterate through all users
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET user_id = NULL;

    OPEN user_cursor;
    FETCH user_cursor INTO user_id;

    WHILE user_id IS NOT NULL DO
        -- Calculate the weighted score for the current user
        SELECT SUM(p.weight) INTO total_weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        SELECT SUM(c.score * p.weight) / total_weight INTO weighted_sum
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        -- Update the average_score for the current user
        UPDATE users
        SET average_score = weighted_sum
        WHERE id = user_id;

        -- Fetch the next user
        FETCH user_cursor INTO user_id;
    END WHILE;

    CLOSE user_cursor;

    -- Calculate the total number of users
    SELECT COUNT(*) INTO total_users FROM users;

    -- Update the average_score for all users
    UPDATE users
    SET average_score = (SELECT SUM(average_score) FROM users) / total_users;
END //
DELIMITER ;
