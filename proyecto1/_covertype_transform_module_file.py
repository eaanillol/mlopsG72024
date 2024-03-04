
import tensorflow as tf
import tensorflow_transform as tft

def preprocessing_fn(inputs):
    """Preprocess input DataFrame columns into transformed columns."""
    
    # No transformation for 'Cover_Type' since it's the target variable
    
    # Normalize 'Hillshade_9am' to be in [0, 1]
    hillshade_9am_scaled = tft.scale_by_min_max(inputs['Hillshade_9am'], 
                                                output_min = 0, 
                                                output_max = 1)
    
    # Normalize 'Hillshade_Noon' to be in [0, 1]
    hillshade_noon_scaled = tft.scale_by_min_max(inputs['Hillshade_Noon'], 
                                                output_min = 0, 
                                                output_max = 1)
    
    # Normalize 'Slope' to be in [0, 1]
    slope_scaled = tft.scale_by_min_max(inputs['Slope'], 
                                                output_min = 0, 
                                                output_max = 1)
    
    # The other features don't have specified min/max values for scaling.
    # z-score scaling
    elevation_z_score = tft.scale_to_z_score(inputs['Elevation'])
    distance_to_fire_points_z_score = tft.scale_to_z_score(inputs['Horizontal_Distance_To_Fire_Points'])
    distance_to_hydrology_z_score = tft.scale_to_z_score(inputs['Horizontal_Distance_To_Hydrology'])
    distance_to_roadways_z_score = tft.scale_to_z_score(inputs['Horizontal_Distance_To_Roadways'])
    vertical_distance_to_hydrology_z_score = tft.scale_to_z_score(inputs['Vertical_Distance_To_Hydrology'])
    
    # Return the transformed features
    return {
        'Cover_Type': inputs['Cover_Type'],
        'Hillshade_9am_scaled': hillshade_9am_scaled,
        'Hillshade_Noon_scaled': hillshade_noon_scaled,
        'Slope_scaled': slope_scaled,
        'Elevation_z_score': elevation_z_score,
        'Distance_To_Fire_Points_z_score': distance_to_fire_points_z_score,
        'Distance_To_Hydrology_z_score': distance_to_hydrology_z_score,
        'Distance_To_Roadways_z_score': distance_to_roadways_z_score,
        'Vertical_Distance_To_Hydrology_z_score': vertical_distance_to_hydrology_z_score
    }
