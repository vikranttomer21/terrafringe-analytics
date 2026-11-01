from pydantic import BaseModel, Field, field_validator

class EcoZone(BaseModel):
    eco_zone_id: str = Field(..., max_length=10)
    zone_name: str
    biome_type: str
    baseline_canopy_sqkm_1996: float = Field(..., gt=0)
    protected_core_sqkm: float = Field(..., gt=0)
    primary_deforestation_driver: str

class BaseFactRecord(BaseModel):
    eco_zone_id: str
    epoch_year: int

    @field_validator('epoch_year')
    def valid_epoch(cls, v):
        valid_years = [1996, 2001, 2006, 2011, 2016, 2021, 2026]
        if v not in valid_years:
            raise ValueError(f"Epoch year {v} must be one of {valid_years}")
        return v

class BiodiversityRecord(BaseFactRecord):
    canopy_cover_retained_pct: float = Field(..., ge=0.0, le=100.0)
    living_planet_index_score: float = Field(..., ge=0.0)
    iucn_threatened_species_count: int = Field(..., ge=0)
    apex_predator_census_count: int = Field(..., ge=0)
    mesopredator_census_count: int = Field(..., ge=0)
    megaherbivore_census_count: int = Field(..., ge=0)
    ungulate_biomass_density_sqkm: float = Field(..., ge=0.0)
    avian_diversity_index: float = Field(..., ge=0.0, le=100.0)
    reptile_amphibian_species_count: int = Field(..., ge=0)
    endemic_flora_richness_index: float = Field(..., ge=0.0, le=100.0)
    invasive_weed_spread_sqkm: float = Field(..., ge=0.0)

class HydrologyRecord(BaseFactRecord):
    land_surface_temp_anomaly_celsius: float
    mean_perennial_streamflow_m3s: float = Field(..., ge=0.0)
    forest_waterhole_dryout_rate_pct: float = Field(..., ge=0.0, le=100.0)
    groundwater_table_depth_mbgl: float = Field(..., ge=0.0)
    soil_organic_carbon_pct: float = Field(..., ge=0.0, le=100.0)

    @field_validator('land_surface_temp_anomaly_celsius')
    def check_realistic_anomaly(cls, v):
        if v > 8.0 or v < -3.0:
            raise ValueError(f"Anomalous LST spike detected: {v}°C. Review scraper source.")
        return v

class VulnerabilityRecord(BaseFactRecord):
    fringe_villages_count: int = Field(..., ge=0)
    fringe_population_exposed: int = Field(..., ge=0)
    tribal_ntfp_income_loss_pct: float = Field(..., ge=0.0, le=100.0)
    agrarian_debt_prevalence_pct: float = Field(..., ge=0.0, le=100.0)
    forced_economic_outmigration_rate: float = Field(..., ge=0.0)

class ConflictRecord(BaseFactRecord):
    crop_depredation_hectares: float = Field(..., ge=0.0)
    economic_crop_loss_val_usd: float = Field(..., ge=0.0)
    livestock_predated_heads: int = Field(..., ge=0)
    human_casualties_fatalities: int = Field(..., ge=0)
    human_casualties_injuries: int = Field(..., ge=0)
    compensation_claims_submitted_usd: float = Field(..., ge=0.0)
    compensation_claims_disbursed_usd: float = Field(..., ge=0.0)
    retaliatory_killing_incidents: int = Field(..., ge=0)

    @field_validator('compensation_claims_disbursed_usd')
    def check_disbursement_logic(cls, v, info):
        submitted = info.data.get('compensation_claims_submitted_usd', 0)
        if v > submitted:
            raise ValueError("Disbursed compensation cannot exceed submitted claims.")
        return v