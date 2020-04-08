USE covid_19;
DROP PROCEDURE IF EXISTS daily_deaths_change;

DELIMITER $$
USE covid_19 $$
CREATE PROCEDURE daily_deaths_change ()
BEGIN
    SET @daily_death_change := -1,@country := 'default';
	SELECT 
		ID,
        country_region,
        calander,
		IF(@daily_death_change = -1 OR @country <> Country_Region , 0, death_per_day - @daily_death_change) AS death_change,
		@daily_death_change := death_per_day AS dummy1,
		@country :=Country_Region AS dummy2
	FROM 
		death_total
	ORDER BY  Country_Region, calander;
END $$
DELIMITER ;

call daily_deaths_change;