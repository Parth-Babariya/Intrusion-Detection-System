import pandas as pd
import joblib
import shap
import numpy as np

# ==========================================
# SETUP: Load your saved "brains"
# ==========================================
print("Loading model and scaler...")
rf_model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')

# Initialize SHAP explainer (doing this once upfront saves processing time)
explainer = shap.TreeExplainer(rf_model)

# ==========================================
# 1. EXTRACT: Get the new data
# ==========================================
print("Extracting new data...")
# Read the incoming batch of network logs
raw_data = pd.read_csv('new_network_traffic.csv')

# Keep an untouched copy for our final database table 
# (Stakeholders want to see actual IPs/Ports, not scaled math numbers)
final_output = raw_data.copy()

# ==========================================
# 2. TRANSFORM: Clean, Encode, Scale, Predict
# ==========================================
print("Transforming and predicting...")

# Step A: Drop ID, target, and problematic columns FIRST
columns_to_drop = ['id', 'attack_cat', 'label', 'sstl']
raw_data_clean = raw_data.drop(columns=[col for col in columns_to_drop if col in raw_data.columns])

print(f"Dropped columns: {[col for col in columns_to_drop if col in raw_data.columns]}")
print(f"Remaining columns: {list(raw_data_clean.columns)}")

# Step B: One-Hot Encode the specific text columns
raw_data_encoded = pd.get_dummies(raw_data_clean, columns=['proto', 'service', 'state'])

# Step C: The Magic Alignment
expected_columns = scaler.feature_names_in_
raw_data_aligned = raw_data_encoded.reindex(columns=expected_columns, fill_value=0)

# ---> THE FIX: Force everything to be a standard decimal number (float) <---
# This prevents the MinMaxScaler from getting confused by True/False vs 1/0
raw_data_aligned = raw_data_aligned.astype(float)

# Step D: Scale safely and convert back to DataFrame
scaled_array = scaler.transform(raw_data_aligned)
scaled_features = pd.DataFrame(scaled_array, columns=expected_columns)
# Make predictions (0 = Normal, 1 = Attack)
predictions = rf_model.predict(scaled_features)
final_output['Prediction'] = predictions

# --- THE SHAP OPTIMIZATION ---
# Create a boolean mask to perfectly align our rows
is_attack = final_output['Prediction'] == 1

if is_attack.sum() > 0:
    print(f"Detected {is_attack.sum()} attacks. Calculating SHAP explanations...")
    
    # Grab only the scaled data for the attacks
    attack_data_scaled = scaled_features[is_attack]
    
    # Calculate the SHAP values
    shap_values = explainer.shap_values(attack_data_scaled)
    
    # Bulletproof way to extract the Attack class values regardless of SHAP version
    if isinstance(shap_values, list):
        shap_values_to_use = shap_values[1]
    elif len(shap_values.shape) == 3:
        shap_values_to_use = shap_values[:, :, 1] # Extract the 2nd class (Attacks)
    else:
        shap_values_to_use = shap_values

    # Find the index of the highest SHAP value for each attack row
    top_feature_indices = np.argmax(np.abs(shap_values_to_use), axis=1)
    
    # Map those indices back to the actual column names
    top_features = [expected_columns[i] for i in top_feature_indices]
    
    # Add these top features to our final output dataframe safely
    final_output.loc[is_attack, 'Top_Risk_Feature'] = top_features
else:
    print("No attacks detected in this batch.")
    final_output['Top_Risk_Feature'] = None
# ==========================================
# 3. LOAD: Push to PostgreSQL Database
# ==========================================
from sqlalchemy import create_engine

print("\nConnecting to PostgreSQL Database...")

# Format: postgresql+psycopg2://username:password@host:port/database_name
# Replace 'YOUR_PASSWORD' with the password you set during installation!
# Note: Special characters in password must be URL-encoded (@ becomes %40)
db_connection_str = 'postgresql+psycopg2://postgres:Bhautik%401234@localhost:5432/IntrusionDB'
engine = create_engine(db_connection_str)

# We filter the dataframe to only include the columns we created in our SQL table
columns_for_db = ['id', 'proto', 'spkts', 'dpkts', 'Prediction', 'Top_Risk_Feature']
data_to_load = final_output[columns_for_db].copy()

# Rename the pandas columns to perfectly match the lowercase PostgreSQL table columns
data_to_load.rename(columns={
    'Prediction': 'prediction', 
    'Top_Risk_Feature': 'top_risk_feature'
}, inplace=True)

try:
    # Push the data! 'append' adds new rows without deleting old ones.
    data_to_load.to_sql('network_traffic', con=engine, if_exists='append', index=False)
    print("SUCCESS: Pipeline data loaded into PostgreSQL!")
except Exception as e:
    print(f"ERROR: Could not load data to database. Details: {e}")