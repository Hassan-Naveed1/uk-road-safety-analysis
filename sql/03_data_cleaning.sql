
USE UKRoadSafetyDB;
GO

-- =========================================================
-- 1. CHECK MISSING AND EMPTY VALUES
-- =========================================================

SELECT
    'Collisions' AS Dataset,
    COUNT_BIG(*) AS TotalRecords,
    SUM(CASE WHEN collision_index IS NULL OR LTRIM(RTRIM(collision_index)) = ''
        THEN 1 ELSE 0 END) AS MissingCollisionIndex,
    SUM(CASE WHEN latitude IS NULL OR latitude = ''
        THEN 1 ELSE 0 END) AS MissingLatitude,
    SUM(CASE WHEN longitude IS NULL OR longitude = ''
        THEN 1 ELSE 0 END) AS MissingLongitude
FROM stg.Collisions

UNION ALL

SELECT
    'Vehicles',
    COUNT_BIG(*),
    SUM(CASE WHEN collision_index IS NULL OR LTRIM(RTRIM(collision_index)) = ''
        THEN 1 ELSE 0 END),
    NULL,
    NULL
FROM stg.Vehicles

UNION ALL

SELECT
    'Casualties',
    COUNT_BIG(*),
    SUM(CASE WHEN collision_index IS NULL OR LTRIM(RTRIM(collision_index)) = ''
        THEN 1 ELSE 0 END),
    NULL,
    NULL
FROM stg.Casualties;
GO


-- =========================================================
-- 2. CHECK MAXIMUM TEXT LENGTHS
-- =========================================================

DROP TABLE IF EXISTS #ColumnLengthChecks;

CREATE TABLE #ColumnLengthChecks
(
    TableName SYSNAME,
    ColumnName SYSNAME,
    MaximumLength INT
);

DECLARE @TableName SYSNAME;
DECLARE @ColumnName SYSNAME;
DECLARE @SQL NVARCHAR(MAX);

DECLARE column_cursor CURSOR LOCAL FAST_FORWARD FOR
SELECT
    t.name,
    c.name
FROM sys.tables t
INNER JOIN sys.schemas s
    ON t.schema_id = s.schema_id
INNER JOIN sys.columns c
    ON t.object_id = c.object_id
WHERE s.name = 'stg'
  AND t.name IN ('Collisions', 'Vehicles', 'Casualties');

OPEN column_cursor;

FETCH NEXT FROM column_cursor
INTO @TableName, @ColumnName;

WHILE @@FETCH_STATUS = 0
BEGIN
    SET @SQL = N'
        INSERT INTO #ColumnLengthChecks
        SELECT
            @TableName,
            @ColumnName,
            MAX(LEN(' + QUOTENAME(@ColumnName) + N'))
        FROM stg.' + QUOTENAME(@TableName) + N';';

    EXEC sp_executesql
        @SQL,
        N'@TableName SYSNAME, @ColumnName SYSNAME',
        @TableName,
        @ColumnName;

    FETCH NEXT FROM column_cursor
    INTO @TableName, @ColumnName;
END;

CLOSE column_cursor;
DEALLOCATE column_cursor;

SELECT *
FROM #ColumnLengthChecks
WHERE MaximumLength >= 255
ORDER BY MaximumLength DESC;

-- No results means no values reached the 255-character limit.
GO


-- =========================================================
-- 3. CHECK COLLISION DATE AND TIME CONVERSION
-- =========================================================

SELECT
    COUNT_BIG(*) AS TotalRecords,

    SUM(CASE
        WHEN TRY_CONVERT(DATE, [date], 103) IS NULL
        THEN 1 ELSE 0
    END) AS InvalidDates,

    SUM(CASE
        WHEN TRY_CONVERT(TIME, [time]) IS NULL
        THEN 1 ELSE 0
    END) AS InvalidTimes

FROM stg.Collisions;
GO


-- Show examples of invalid dates or times, if any.

SELECT TOP 10
    collision_index,
    [date],
    [time]
FROM stg.Collisions
WHERE TRY_CONVERT(DATE, [date], 103) IS NULL
   OR TRY_CONVERT(TIME, [time]) IS NULL;
GO


-- =========================================================
-- 4. CHECK NUMERIC CONVERSION
-- =========================================================

SELECT
    'Collisions' AS Dataset,
    SUM(CASE WHEN TRY_CONVERT(INT, collision_year) IS NULL
        THEN 1 ELSE 0 END) AS InvalidYears,
    SUM(CASE WHEN TRY_CONVERT(INT, number_of_vehicles) IS NULL
        THEN 1 ELSE 0 END) AS InvalidVehicleCounts,
    SUM(CASE WHEN TRY_CONVERT(INT, number_of_casualties) IS NULL
        THEN 1 ELSE 0 END) AS InvalidCasualtyCounts
FROM stg.Collisions

UNION ALL

SELECT
    'Vehicles',
    SUM(CASE WHEN TRY_CONVERT(INT, collision_year) IS NULL
        THEN 1 ELSE 0 END),
    SUM(CASE WHEN TRY_CONVERT(INT, vehicle_reference) IS NULL
        THEN 1 ELSE 0 END),
    NULL
FROM stg.Vehicles

UNION ALL

SELECT
    'Casualties',
    SUM(CASE WHEN TRY_CONVERT(INT, collision_year) IS NULL
        THEN 1 ELSE 0 END),
    SUM(CASE WHEN TRY_CONVERT(INT, vehicle_reference) IS NULL
        THEN 1 ELSE 0 END),
    SUM(CASE WHEN TRY_CONVERT(INT, casualty_reference) IS NULL
        THEN 1 ELSE 0 END)
FROM stg.Casualties;
GO


-- =========================================================
-- 5. INSPECT SPECIAL COLLISION SEVERITY CODES
-- =========================================================

SELECT
    collision_severity,
    COUNT_BIG(*) AS RecordCount
FROM stg.Collisions
GROUP BY collision_severity
ORDER BY collision_severity;
GO


-- =========================================================
-- 6. INSPECT SPECIAL WEATHER CONDITION CODES
-- =========================================================

SELECT
    weather_conditions,
    COUNT_BIG(*) AS RecordCount
FROM stg.Collisions
GROUP BY weather_conditions
ORDER BY weather_conditions;
GO
