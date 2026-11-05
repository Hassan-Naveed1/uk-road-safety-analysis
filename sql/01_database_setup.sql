
USE UKRoadSafetyDB;
GO

-- =========================================================
-- 1. CREATE STAGING SCHEMA
-- =========================================================

IF NOT EXISTS (
    SELECT 1
    FROM sys.schemas
    WHERE name = 'stg'
)
BEGIN
    EXEC('CREATE SCHEMA stg');
END;
GO


-- =========================================================
-- 2. COLLISIONS STAGING TABLE
-- =========================================================

IF OBJECT_ID('stg.Collisions', 'U') IS NOT NULL
    DROP TABLE stg.Collisions;
GO

CREATE TABLE stg.Collisions
(
    collision_index NVARCHAR(50),
    collision_year NVARCHAR(255),
    collision_ref_no NVARCHAR(255),
    location_easting_osgr NVARCHAR(255),
    location_northing_osgr NVARCHAR(255),
    longitude NVARCHAR(255),
    latitude NVARCHAR(255),
    police_force NVARCHAR(255),
    collision_severity NVARCHAR(255),
    number_of_vehicles NVARCHAR(255),
    number_of_casualties NVARCHAR(255),
    date NVARCHAR(255),
    day_of_week NVARCHAR(255),
    time NVARCHAR(255),
    local_authority_district NVARCHAR(255),
    local_authority_ons_district NVARCHAR(255),
    local_authority_highway NVARCHAR(255),
    local_authority_highway_current NVARCHAR(255),
    first_road_class NVARCHAR(255),
    first_road_number NVARCHAR(255),
    road_type NVARCHAR(255),
    speed_limit NVARCHAR(255),
    junction_detail_historic NVARCHAR(255),
    junction_detail NVARCHAR(255),
    junction_control NVARCHAR(255),
    second_road_class NVARCHAR(255),
    second_road_number NVARCHAR(255),
    pedestrian_crossing_human_control_historic NVARCHAR(255),
    pedestrian_crossing_physical_facilities_historic NVARCHAR(255),
    pedestrian_crossing NVARCHAR(255),
    light_conditions NVARCHAR(255),
    weather_conditions NVARCHAR(255),
    road_surface_conditions NVARCHAR(255),
    special_conditions_at_site NVARCHAR(255),
    carriageway_hazards_historic NVARCHAR(255),
    carriageway_hazards NVARCHAR(255),
    urban_or_rural_area NVARCHAR(255),
    did_police_officer_attend_scene_of_accident NVARCHAR(255),
    trunk_road_flag NVARCHAR(255),
    lsoa_of_accident_location NVARCHAR(255),
    enhanced_severity_collision NVARCHAR(255),
    collision_injury_based NVARCHAR(255),
    collision_adjusted_severity_serious NVARCHAR(255),
    collision_adjusted_severity_slight NVARCHAR(255)
);
GO


-- =========================================================
-- 3. VEHICLES STAGING TABLE
-- =========================================================

IF OBJECT_ID('stg.Vehicles', 'U') IS NOT NULL
    DROP TABLE stg.Vehicles;
GO

CREATE TABLE stg.Vehicles
(
    collision_index NVARCHAR(50),
    collision_year NVARCHAR(255),
    collision_ref_no NVARCHAR(255),
    vehicle_reference NVARCHAR(255),
    vehicle_type NVARCHAR(255),
    towing_and_articulation NVARCHAR(255),
    vehicle_manoeuvre_historic NVARCHAR(255),
    vehicle_manoeuvre NVARCHAR(255),
    vehicle_direction_from NVARCHAR(255),
    vehicle_direction_to NVARCHAR(255),
    vehicle_location_restricted_lane_historic NVARCHAR(255),
    vehicle_location_restricted_lane NVARCHAR(255),
    junction_location NVARCHAR(255),
    skidding_and_overturning NVARCHAR(255),
    hit_object_in_carriageway NVARCHAR(255),
    vehicle_leaving_carriageway NVARCHAR(255),
    hit_object_off_carriageway NVARCHAR(255),
    first_point_of_impact NVARCHAR(255),
    vehicle_left_hand_drive NVARCHAR(255),
    journey_purpose_of_driver_historic NVARCHAR(255),
    journey_purpose_of_driver NVARCHAR(255),
    sex_of_driver NVARCHAR(255),
    age_of_driver NVARCHAR(255),
    age_band_of_driver NVARCHAR(255),
    engine_capacity_cc NVARCHAR(255),
    propulsion_code NVARCHAR(255),
    age_of_vehicle NVARCHAR(255),
    generic_make_model NVARCHAR(255),
    driver_imd_decile NVARCHAR(255),
    lsoa_of_driver NVARCHAR(255),
    escooter_flag NVARCHAR(255),
    driver_distance_banding NVARCHAR(255)
);
GO


-- =========================================================
-- 4. CASUALTIES STAGING TABLE
-- =========================================================

IF OBJECT_ID('stg.Casualties', 'U') IS NOT NULL
    DROP TABLE stg.Casualties;
GO

CREATE TABLE stg.Casualties
(
    collision_index NVARCHAR(50),
    collision_year NVARCHAR(255),
    collision_ref_no NVARCHAR(255),
    vehicle_reference NVARCHAR(255),
    casualty_reference NVARCHAR(255),
    casualty_class NVARCHAR(255),
    sex_of_casualty NVARCHAR(255),
    age_of_casualty NVARCHAR(255),
    age_band_of_casualty NVARCHAR(255),
    casualty_severity NVARCHAR(255),
    pedestrian_location NVARCHAR(255),
    pedestrian_movement NVARCHAR(255),
    car_passenger NVARCHAR(255),
    bus_or_coach_passenger NVARCHAR(255),
    pedestrian_road_maintenance_worker NVARCHAR(255),
    casualty_type NVARCHAR(255),
    casualty_imd_decile NVARCHAR(255),
    lsoa_of_casualty NVARCHAR(255),
    enhanced_casualty_severity NVARCHAR(255),
    casualty_injury_based NVARCHAR(255),
    casualty_adjusted_severity_serious NVARCHAR(255),
    casualty_adjusted_severity_slight NVARCHAR(255),
    casualty_distance_banding NVARCHAR(255),
    escooter_flag NVARCHAR(255)
);
GO


-- =========================================================
-- 5. VERIFY TABLE CREATION
-- =========================================================

SELECT
    SCHEMA_NAME(schema_id) AS schema_name,
    name AS table_name
FROM sys.tables
WHERE schema_id = SCHEMA_ID('stg')
ORDER BY name;
GO
