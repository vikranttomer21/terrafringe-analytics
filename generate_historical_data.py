"""
TerraFringe historical scenario data generator.

IMPORTANT:
- This script generates illustrative synthetic scenario data, NOT official observations.
- It creates distinct corridor/year patterns for dashboard development.
- Replace these values with sourced observations before making scientific claims.
- Existing schema/table names are retained.
"""

import random
from data_pipeline.schemas import (
    BiodiversityRecord,
    HydrologyRecord,
    VulnerabilityRecord,
    ConflictRecord,
)
from data_pipeline.mysql_loader import MySQLDataLoader


EPOCHS = [1996, 2001, 2006, 2011, 2016, 2021, 2026]
ZONES = ["EZ_WG_01", "EZ_CI_01", "EZ_TR_01"]

# Separate corridor profiles prevent all corridors from sharing the same trend.
PROFILES = {
    "EZ_WG_01": {
        "canopy": 94, "canopy_loss": 17, "lpi": 96, "lpi_loss": 38,
        "threatened": 13, "apex": 26, "meso": 53, "mega": 185,
        "ungulate": 43, "avian": 88, "herp": 103, "flora": 82, "weed": 18,
        "temp": 0.25, "temp_rise": 2.05, "stream": 118, "stream_loss": 63,
        "dryout": 12, "dryout_rise": 53, "ground": 8.5, "ground_rise": 16,
        "carbon": 3.5, "carbon_loss": 1.15,
        "villages": 27, "population": 47000, "ntfp": 7, "debt": 18, "migration": 2.5,
        "crop": 145, "livestock": 18, "fatal": 1, "injury": 4, "retaliation": 1,
    },
    "EZ_CI_01": {
        "canopy": 93, "canopy_loss": 26, "lpi": 91, "lpi_loss": 44,
        "threatened": 16, "apex": 43, "meso": 47, "mega": 164,
        "ungulate": 48, "avian": 84, "herp": 96, "flora": 78, "weed": 12,
        "temp": 0.15, "temp_rise": 1.85, "stream": 126, "stream_loss": 54,
        "dryout": 9, "dryout_rise": 46, "ground": 7.5, "ground_rise": 13,
        "carbon": 3.8, "carbon_loss": 0.95,
        "villages": 22, "population": 39000, "ntfp": 5, "debt": 14, "migration": 1.8,
        "crop": 62, "livestock": 9, "fatal": 0, "injury": 2, "retaliation": 0,
    },
    "EZ_TR_01": {
        "canopy": 92, "canopy_loss": 21, "lpi": 94, "lpi_loss": 41,
        "threatened": 14, "apex": 24, "meso": 61, "mega": 142,
        "ungulate": 39, "avian": 86, "herp": 88, "flora": 80, "weed": 22,
        "temp": 0.30, "temp_rise": 2.35, "stream": 107, "stream_loss": 71,
        "dryout": 14, "dryout_rise": 64, "ground": 9.2, "ground_rise": 20,
        "carbon": 3.25, "carbon_loss": 1.4,
        "villages": 31, "population": 52000, "ntfp": 8, "debt": 21, "migration": 3.2,
        "crop": 92, "livestock": 12, "fatal": 0, "injury": 3, "retaliation": 0,
    },
}


def clamp(value, low=0, high=None):
    value = max(low, value)
    if high is not None:
        value = min(high, value)
    return value


def jitter(rng, value, spread=0.08):
    """Deterministic, bounded variation around a scenario value."""
    return value * rng.uniform(1 - spread, 1 + spread)


def generate_empirical_data():
    # Stable seed means repeat runs are reproducible but not identical by formula alone.
    rng = random.Random(20261031)

    biodiversity_data = []
    hydrology_data = []
    vuln_data = []
    conflict_data = []

    for zone_index, zone in enumerate(ZONES):
        p = PROFILES[zone]
        previous_year_shock = 0.0

        for i, year in enumerate(EPOCHS):
            t = i / (len(EPOCHS) - 1)
            # Small corridor-specific shocks create non-linear trajectories.
            shock = [0.0, -0.035, 0.055, -0.02, 0.045, -0.03, 0.025][i]
            zone_shift = (zone_index - 1) * 0.012
            local = shock + zone_shift + rng.uniform(-0.025, 0.025)

            canopy = clamp(p["canopy"] - p["canopy_loss"] * t + local * 25, 0, 100)
            lpi = clamp(p["lpi"] - p["lpi_loss"] * t + local * 35, 0, 100)
            apex = round(clamp(p["apex"] + (5 + zone_index) * t + (rng.randint(-3, 3)), 0))
            if year == 2006:
                apex = max(0, apex - (7 if zone == "EZ_CI_01" else 3))
            if year >= 2016:
                apex += 2 if zone == "EZ_CI_01" else 1

            biodiversity_data.append(BiodiversityRecord(
                eco_zone_id=zone,
                epoch_year=year,
                canopy_cover_retained_pct=round(canopy, 2),
                living_planet_index_score=round(lpi, 2),
                iucn_threatened_species_count=int(clamp(
                    p["threatened"] + 7 * t + rng.randint(-1, 2), 0
                )),
                apex_predator_census_count=int(apex),
                mesopredator_census_count=int(clamp(
                    p["meso"] + 11 * t + rng.randint(-5, 5), 0
                )),
                megaherbivore_census_count=int(clamp(
                    p["mega"] - (25 + zone_index * 4) * t + rng.randint(-8, 8), 0
                )),
                ungulate_biomass_density_sqkm=round(clamp(
                    p["ungulate"] - (8 + zone_index) * t + rng.uniform(-3, 3), 0
                ), 2),
                avian_diversity_index=round(clamp(
                    p["avian"] - (15 + zone_index * 2) * t + rng.uniform(-4, 4), 0, 100
                ), 2),
                reptile_amphibian_species_count=int(clamp(
                    p["herp"] - (16 + zone_index * 3) * t + rng.randint(-6, 6), 0
                )),
                endemic_flora_richness_index=round(clamp(
                    p["flora"] - (13 + zone_index) * t + rng.uniform(-3, 3), 0, 100
                ), 2),
                invasive_weed_spread_sqkm=round(clamp(
                    p["weed"] + (230 + zone_index * 55) * t + rng.uniform(-18, 18), 0
                ), 2),
            ))

            # Hydrology scenarios: different slopes and local deviations per corridor.
            hydrology_data.append(HydrologyRecord(
                eco_zone_id=zone,
                epoch_year=year,
                land_surface_temp_anomaly_celsius=round(clamp(
                    p["temp"] + p["temp_rise"] * t + rng.uniform(-0.18, 0.18), -5
                ), 2),
                mean_perennial_streamflow_m3s=round(clamp(
                    p["stream"] - p["stream_loss"] * t + rng.uniform(-8, 8), 0
                ), 2),
                forest_waterhole_dryout_rate_pct=round(clamp(
                    p["dryout"] + p["dryout_rise"] * t + rng.uniform(-5, 5), 0, 100
                ), 2),
                groundwater_table_depth_mbgl=round(clamp(
                    p["ground"] + p["ground_rise"] * t + rng.uniform(-2, 2), 0
                ), 2),
                soil_organic_carbon_pct=round(clamp(
                    p["carbon"] - p["carbon_loss"] * t + rng.uniform(-0.18, 0.18), 0
                ), 2),
            ))

            # Vulnerability indicators with zone-specific baselines and varied trajectories.
            vuln_data.append(VulnerabilityRecord(
                eco_zone_id=zone,
                epoch_year=year,
                fringe_villages_count=int(clamp(
                    p["villages"] + 12 * t + rng.randint(-2, 2), 0
                )),
                fringe_population_exposed=int(clamp(
                    p["population"] + (23000 + zone_index * 6500) * t
                    + rng.randint(-2500, 2500), 0
                )),
                tribal_ntfp_income_loss_pct=round(clamp(
                    p["ntfp"] + (48 + zone_index * 7) * t + rng.uniform(-5, 5), 0, 100
                ), 2),
                agrarian_debt_prevalence_pct=round(clamp(
                    p["debt"] + (39 + zone_index * 5) * t + rng.uniform(-4, 4), 0, 100
                ), 2),
                forced_economic_outmigration_rate=round(clamp(
                    p["migration"] + (7 + zone_index * 1.5) * t + rng.uniform(-1.2, 1.2), 0
                ), 2),
            ))

            # Conflict values vary by corridor and epoch. Financial values are
            # illustrative assumptions, not observed loss/compensation figures.
            crop_damage = clamp(
                p["crop"] * (1 + (1.2 + zone_index * 0.18) * t)
                + (t ** 1.7) * (250 + zone_index * 90)
                + rng.uniform(-25, 25),
                0
            )
            livestock = int(clamp(
                p["livestock"] + (8 + zone_index * 3) * t + rng.randint(-4, 5), 0
            ))
            fatalities = int(clamp(
                p["fatal"] + (1.2 + zone_index * 0.4) * t + rng.choice([0, 0, 0, 1]), 0
            ))
            injuries = int(clamp(
                p["injury"] + (6 + zone_index * 2) * t + rng.randint(-2, 3), 0
            ))
            retaliatory = int(clamp(
                p["retaliation"] + (1.8 + zone_index * 0.9) * t + rng.choice([0, 0, 1]), 0
            ))

            # Synthetic proxy only. Do not present these USD figures as actual claims.
            estimated_loss_per_ha = rng.uniform(450, 1250)
            claims_submitted = crop_damage * estimated_loss_per_ha
            paid_fraction = rng.uniform(0.48, 0.86)

            conflict_data.append(ConflictRecord(
                eco_zone_id=zone,
                epoch_year=year,
                crop_depredation_hectares=round(crop_damage, 2),
                economic_crop_loss_val_usd=round(
                    claims_submitted * rng.uniform(1.05, 1.32), 2
                ),
                livestock_predated_heads=livestock,
                human_casualties_fatalities=fatalities,
                human_casualties_injuries=injuries,
                compensation_claims_submitted_usd=round(claims_submitted, 2),
                compensation_claims_disbursed_usd=round(claims_submitted * paid_fraction, 2),
                retaliatory_killing_incidents=retaliatory,
            ))

    return biodiversity_data, hydrology_data, vuln_data, conflict_data


def main():
    print("Generating TerraFringe illustrative scenario dataset.")
    print("WARNING: these are synthetic values, NOT official historical observations.")
    b_data, h_data, v_data, c_data = generate_empirical_data()

    loader = MySQLDataLoader()
    cursor = None

    try:
        print("Loading biodiversity records...")
        loader.load_biodiversity_records(b_data)

        cursor = loader.connection.cursor()

        cursor.executemany("""
            INSERT INTO fact_watershed_aquifer_hydrology (
                eco_zone_id, epoch_year, land_surface_temp_anomaly_celsius,
                mean_perennial_streamflow_m3s, forest_waterhole_dryout_rate_pct,
                groundwater_table_depth_mbgl, soil_organic_carbon_pct
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                land_surface_temp_anomaly_celsius = VALUES(land_surface_temp_anomaly_celsius),
                mean_perennial_streamflow_m3s = VALUES(mean_perennial_streamflow_m3s),
                forest_waterhole_dryout_rate_pct = VALUES(forest_waterhole_dryout_rate_pct),
                groundwater_table_depth_mbgl = VALUES(groundwater_table_depth_mbgl),
                soil_organic_carbon_pct = VALUES(soil_organic_carbon_pct)
        """, [
            (r.eco_zone_id, r.epoch_year, r.land_surface_temp_anomaly_celsius,
             r.mean_perennial_streamflow_m3s, r.forest_waterhole_dryout_rate_pct,
             r.groundwater_table_depth_mbgl, r.soil_organic_carbon_pct)
            for r in h_data
        ])

        cursor.executemany("""
            INSERT INTO fact_fringe_population_vulnerability (
                eco_zone_id, epoch_year, fringe_villages_count,
                fringe_population_exposed, tribal_ntfp_income_loss_pct,
                agrarian_debt_prevalence_pct, forced_economic_outmigration_rate
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                fringe_villages_count = VALUES(fringe_villages_count),
                fringe_population_exposed = VALUES(fringe_population_exposed),
                tribal_ntfp_income_loss_pct = VALUES(tribal_ntfp_income_loss_pct),
                agrarian_debt_prevalence_pct = VALUES(agrarian_debt_prevalence_pct),
                forced_economic_outmigration_rate = VALUES(forced_economic_outmigration_rate)
        """, [
            (r.eco_zone_id, r.epoch_year, r.fringe_villages_count,
             r.fringe_population_exposed, r.tribal_ntfp_income_loss_pct,
             r.agrarian_debt_prevalence_pct, r.forced_economic_outmigration_rate)
            for r in v_data
        ])

        cursor.executemany("""
            INSERT INTO fact_human_wildlife_conflict (
                eco_zone_id, epoch_year, crop_depredation_hectares,
                economic_crop_loss_val_usd, livestock_predated_heads,
                human_casualties_fatalities, human_casualties_injuries,
                compensation_claims_submitted_usd, compensation_claims_disbursed_usd,
                retaliatory_killing_incidents
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                crop_depredation_hectares = VALUES(crop_depredation_hectares),
                economic_crop_loss_val_usd = VALUES(economic_crop_loss_val_usd),
                livestock_predated_heads = VALUES(livestock_predated_heads),
                human_casualties_fatalities = VALUES(human_casualties_fatalities),
                human_casualties_injuries = VALUES(human_casualties_injuries),
                compensation_claims_submitted_usd = VALUES(compensation_claims_submitted_usd),
                compensation_claims_disbursed_usd = VALUES(compensation_claims_disbursed_usd),
                retaliatory_killing_incidents = VALUES(retaliatory_killing_incidents)
        """, [
            (r.eco_zone_id, r.epoch_year, r.crop_depredation_hectares,
             r.economic_crop_loss_val_usd, r.livestock_predated_heads,
             r.human_casualties_fatalities, r.human_casualties_injuries,
             r.compensation_claims_submitted_usd, r.compensation_claims_disbursed_usd,
             r.retaliatory_killing_incidents)
            for r in c_data
        ])

        loader.connection.commit()
        print("Loaded/updated 21 rows in each of the four fact tables.")
        print("Refresh Power BI. These values remain synthetic scenarios.")

    except Exception:
        if getattr(loader, "connection", None):
            loader.connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        loader.close()


if __name__ == "__main__":
    main()
