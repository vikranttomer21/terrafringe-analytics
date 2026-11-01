import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_pipeline.schemas import BiodiversityRecord

load_dotenv()

class MySQLDataLoader:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            if self.connection.is_connected():
                print("✅ Successfully connected to MySQL database.")
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            sys.exit(1)

    def load_biodiversity_records(self, records: list[BiodiversityRecord]):
        if not records:
            return

        cursor = self.connection.cursor()
        
        insert_query = """
        INSERT INTO fact_flora_fauna_biodiversity (
            eco_zone_id, epoch_year, canopy_cover_retained_pct, 
            living_planet_index_score, iucn_threatened_species_count, 
            apex_predator_census_count, mesopredator_census_count, 
            megaherbivore_census_count, ungulate_biomass_density_sqkm,
            avian_diversity_index, reptile_amphibian_species_count,
            endemic_flora_richness_index, invasive_weed_spread_sqkm
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            canopy_cover_retained_pct = VALUES(canopy_cover_retained_pct),
            living_planet_index_score = VALUES(living_planet_index_score);
        """
        
        data_tuples = [
            (
                r.eco_zone_id, r.epoch_year, r.canopy_cover_retained_pct, 
                r.living_planet_index_score, r.iucn_threatened_species_count, 
                r.apex_predator_census_count, r.mesopredator_census_count,
                r.megaherbivore_census_count, r.ungulate_biomass_density_sqkm,
                r.avian_diversity_index, r.reptile_amphibian_species_count,
                r.endemic_flora_richness_index, r.invasive_weed_spread_sqkm
            ) for r in records
        ]

        try:
            cursor.executemany(insert_query, data_tuples)
            self.connection.commit()
            print(f"✅ Loaded {cursor.rowcount} full-ecosystem biodiversity records successfully.")
        except Error as e:
            print(f"❌ Failed to insert records: {e}")
        finally:
            cursor.close()

    def close(self):
        if self.connection.is_connected():
            self.connection.close()

if __name__ == "__main__":
    mock_scraped_data = [
        BiodiversityRecord(
            eco_zone_id="EZ_WG_01", epoch_year=2026, canopy_cover_retained_pct=65.5,
            living_planet_index_score=45.0, iucn_threatened_species_count=18,
            apex_predator_census_count=12, mesopredator_census_count=45,
            megaherbivore_census_count=120, ungulate_biomass_density_sqkm=35.5,
            avian_diversity_index=72.0, reptile_amphibian_species_count=85,
            endemic_flora_richness_index=55.0, invasive_weed_spread_sqkm=45.0
        )
    ]
    
    loader = MySQLDataLoader()
    loader.load_biodiversity_records(mock_scraped_data)
    loader.close()