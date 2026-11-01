CREATE DATABASE IF NOT EXISTS terrafringe_intelligence;
USE terrafringe_intelligence;

CREATE TABLE IF NOT EXISTS dim_eco_zones (
    eco_zone_id VARCHAR(10) PRIMARY KEY,
    zone_name VARCHAR(100) NOT NULL,
    biome_type VARCHAR(50),
    baseline_canopy_sqkm_1996 DECIMAL(10,2),
    protected_core_sqkm DECIMAL(10,2),
    primary_deforestation_driver VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS fact_flora_fauna_biodiversity (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    eco_zone_id VARCHAR(10),
    epoch_year INT,
    canopy_cover_retained_pct DECIMAL(5,2),
    living_planet_index_score DECIMAL(5,2),
    iucn_threatened_species_count INT,
    apex_predator_census_count INT,
    mesopredator_census_count INT,
    megaherbivore_census_count INT,
    ungulate_biomass_density_sqkm DECIMAL(6,2),
    avian_diversity_index DECIMAL(5,2),
    reptile_amphibian_species_count INT,
    endemic_flora_richness_index DECIMAL(5,2),
    invasive_weed_spread_sqkm DECIMAL(8,2),
    UNIQUE KEY unique_zone_year (eco_zone_id, epoch_year),
    FOREIGN KEY (eco_zone_id) REFERENCES dim_eco_zones(eco_zone_id)
);

CREATE TABLE IF NOT EXISTS fact_watershed_aquifer_hydrology (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    eco_zone_id VARCHAR(10),
    epoch_year INT,
    land_surface_temp_anomaly_celsius DECIMAL(4,2),
    mean_perennial_streamflow_m3s DECIMAL(8,2),
    forest_waterhole_dryout_rate_pct DECIMAL(5,2),
    groundwater_table_depth_mbgl DECIMAL(5,2),
    soil_organic_carbon_pct DECIMAL(4,2),
    UNIQUE KEY unique_zone_year (eco_zone_id, epoch_year),
    FOREIGN KEY (eco_zone_id) REFERENCES dim_eco_zones(eco_zone_id)
);

CREATE TABLE IF NOT EXISTS fact_fringe_population_vulnerability (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    eco_zone_id VARCHAR(10),
    epoch_year INT,
    fringe_villages_count INT,
    fringe_population_exposed INT,
    tribal_ntfp_income_loss_pct DECIMAL(5,2),
    agrarian_debt_prevalence_pct DECIMAL(5,2),
    forced_economic_outmigration_rate DECIMAL(5,2),
    UNIQUE KEY unique_zone_year (eco_zone_id, epoch_year),
    FOREIGN KEY (eco_zone_id) REFERENCES dim_eco_zones(eco_zone_id)
);

CREATE TABLE IF NOT EXISTS fact_human_wildlife_conflict (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    eco_zone_id VARCHAR(10),
    epoch_year INT,
    crop_depredation_hectares DECIMAL(10,2),
    economic_crop_loss_val_usd DECIMAL(12,2),
    livestock_predated_heads INT,
    human_casualties_fatalities INT,
    human_casualties_injuries INT,
    compensation_claims_submitted_usd DECIMAL(12,2),
    compensation_claims_disbursed_usd DECIMAL(12,2),
    retaliatory_killing_incidents INT,
    UNIQUE KEY unique_zone_year (eco_zone_id, epoch_year),
    FOREIGN KEY (eco_zone_id) REFERENCES dim_eco_zones(eco_zone_id)
);

INSERT IGNORE INTO dim_eco_zones VALUES 
('EZ_WG_01', 'Wayanad-Bandipur Link', 'Tropical Wet Evergreen', 4500.0, 3100.0, 'Commercial Agriculture'),
('EZ_CI_01', 'Kanha-Pench Corridor', 'Moist Deciduous', 4200.0, 2400.0, 'Linear Infrastructure'),
('EZ_TR_01', 'Rajaji-Corbett Link', 'Moist Deciduous', 3600.0, 2100.0, 'Linear Infrastructure');


SELECT *
FROM fact_watershed_aquifer_hydrology;