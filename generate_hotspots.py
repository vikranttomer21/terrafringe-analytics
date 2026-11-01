import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import numpy as np

def generate_master_path(polygon, total_points):
    points_data = []
    minx, miny, maxx, maxy = polygon.bounds
    
    # Perfect balance: 2.2x pool organically fills a thick outer fringe instead of a thin line
    pool_size = int(total_points * 2.2) 
    
    # Safety fallback if 2.2x is somehow too small for a tiny total
    pool_size = max(pool_size, total_points + 50)
    
    while len(points_data) < pool_size:
        batch_x = np.random.uniform(minx, maxx, 2000)
        batch_y = np.random.uniform(miny, maxy, 2000)
        
        for x, y in zip(batch_x, batch_y):
            pt = Point(x, y)
            if polygon.contains(pt):
                dist_to_edge = polygon.boundary.distance(pt)
                points_data.append({'lat': y, 'lon': x, 'dist': dist_to_edge})
                
                if len(points_data) >= pool_size:
                    break
                    
    # Fuzziness multiplier (0.7 to 1.3) blurs the inner edge to make it jagged and organic
    points_data.sort(key=lambda d: d['dist'] * np.random.uniform(0.7, 1.3))
    
    final_points = points_data[:total_points]
    
    return [[p['lat'], p['lon']] for p in final_points]
def main():
    print("Loading data...")
    loss_df = pd.read_csv('yearly_loss_numbers.csv')
    corridors_gdf = gpd.read_file('raw_corridors.geojson')

    # DENSITY MODIFIER: 1 dot now represents 2 SqKm (cutting total dots in half)
    sqkm_per_dot = 2 

    # Scale down the maximum points calculated
    max_pts_per_zone = (loss_df.groupby('zone_name')['Canopy_Loss_SqKm'].max() / sqkm_per_dot).astype(int).to_dict()
    
    print("Calculating organic inward-bleeding points based on edge distance...")
    master_coords = {}
    for zone, max_pts in max_pts_per_zone.items():
        if max_pts > 0:
            zone_geom = corridors_gdf.loc[corridors_gdf['zone_name'] == zone, 'geometry'].values[0]
            if zone_geom.geom_type == 'MultiPolygon':
                zone_geom = max(zone_geom.geoms, key=lambda a: a.area)
            
            master_coords[zone] = generate_master_path(zone_geom, int(max_pts))

    final_coordinates = []
    print("Assigning coordinates to timeline...")
    for index, row in loss_df.iterrows():
        zone = row['zone_name']
        year = row['Loss_Year']
        
        # Scale down the points taken for the timeline
        pts_to_take = int(row['Canopy_Loss_SqKm'] / sqkm_per_dot)
        
        if pts_to_take > 0 and zone in master_coords:
            year_coords = master_coords[zone][:pts_to_take]
            
            for lat, lon in year_coords:
                final_coordinates.append({
                    'zone_name': zone,
                    'Loss_Year': year,
                    'Latitude': lat,
                    'Longitude': lon,
                    'Hectares_Lost': 100 * sqkm_per_dot  # Preserves correct underlying mathematical total
                })
                
    print(f"Generated {len(final_coordinates)} total spatial points.")
    
    final_df = pd.DataFrame(final_coordinates)
    final_df.to_csv('localized_deforestation_events.csv', index=False)
    print("Saved to localized_deforestation_events.csv. Refresh Power BI!")
if __name__ == "__main__":
    main()