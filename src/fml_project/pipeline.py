import pandas as pd
import joblib
import shap
import numpy as np
from sqlalchemy import create_engine


def load_models(model_path='random_forest_model.pkl', scaler_path='scaler.pkl'):
    """Load trained model and scaler from disk."""
    rf_model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    explainer = shap.TreeExplainer(rf_model)
    return rf_model, scaler, explainer


def transform_and_predict(raw_data: pd.DataFrame, scaler, rf_model):
    final_output = raw_data.copy()

    columns_to_drop = ['id', 'attack_cat', 'label', 'sstl']
    raw_data_clean = raw_data.drop(columns=[col for col in columns_to_drop if col in raw_data.columns])

    raw_data_encoded = pd.get_dummies(raw_data_clean, columns=['proto', 'service', 'state'])

    expected_columns = scaler.feature_names_in_
    raw_data_aligned = raw_data_encoded.reindex(columns=expected_columns, fill_value=0)
    raw_data_aligned = raw_data_aligned.astype(float)

    scaled_array = scaler.transform(raw_data_aligned)
    scaled_features = pd.DataFrame(scaled_array, columns=expected_columns)

    predictions = rf_model.predict(scaled_features)
    final_output['Prediction'] = predictions

    return final_output, scaled_features


def explain_attacks(final_output: pd.DataFrame, scaled_features: pd.DataFrame, explainer):
    is_attack = final_output['Prediction'] == 1
    if is_attack.sum() == 0:
        final_output['Top_Risk_Feature'] = None
        return final_output

    attack_data_scaled = scaled_features[is_attack]
    shap_values = explainer.shap_values(attack_data_scaled)

    if isinstance(shap_values, list):
        shap_values_to_use = shap_values[1]
    elif len(shap_values.shape) == 3:
        shap_values_to_use = shap_values[:, :, 1]
    else:
        shap_values_to_use = shap_values

    top_feature_indices = np.argmax(np.abs(shap_values_to_use), axis=1)
    expected_columns = scaled_features.columns
    top_features = [expected_columns[i] for i in top_feature_indices]

    final_output.loc[is_attack, 'Top_Risk_Feature'] = top_features
    return final_output


def load_to_db(final_output: pd.DataFrame, db_connection_str: str):
    engine = create_engine(db_connection_str)
    columns_for_db = ['id', 'proto', 'spkts', 'dpkts', 'Prediction', 'Top_Risk_Feature']
    data_to_load = final_output[columns_for_db].copy()
    data_to_load.rename(columns={'Prediction': 'prediction', 'Top_Risk_Feature': 'top_risk_feature'}, inplace=True)
    data_to_load.to_sql('network_traffic', con=engine, if_exists='append', index=False)


def run_pipeline(input_csv='new_network_traffic.csv', model_path='random_forest_model.pkl', scaler_path='scaler.pkl', db_connection_str=None):
    print("Loading model and scaler...")
    rf_model, scaler, explainer = load_models(model_path, scaler_path)

    print("Extracting new data...")
    raw_data = pd.read_csv(input_csv)

    print("Transforming and predicting...")
    final_output, scaled_features = transform_and_predict(raw_data, scaler, rf_model)

    print("Explaining attacks (if any)...")
    final_output = explain_attacks(final_output, scaled_features, explainer)

    if db_connection_str:
        print("Loading results to database...")
        try:
            load_to_db(final_output, db_connection_str)
            print("SUCCESS: Pipeline data loaded into PostgreSQL!")
        except Exception as e:
            print(f"ERROR: Could not load data to database. Details: {e}")

    return final_output


if __name__ == "__main__":
    # Example run (override args when calling as module)
    DB_CONN = 'postgresql+psycopg2://postgres:password@localhost:5432/IntrusionDB'
    run_pipeline()
