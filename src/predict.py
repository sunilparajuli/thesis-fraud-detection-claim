import pandas as pd
import numpy as np
import pickle
import os

def run_inference():
    print("--- AI False Claim Detection Inference ---")
    
    # 1. Load artifacts
    if not os.path.exists('models/model_xgb.pkl'):
        print("Error: Model not found. Please run 'python src/train.py' first.")
        return

    with open('models/model_xgb.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('models/encoders.pkl', 'rb') as f:
        encoders = pickle.load(f)

    # 2. Load data for prediction
    print("Loading data for inference...")
    df_claims = pd.read_csv('data/claims.csv')
    df_items = pd.read_csv('data/items.csv')
    df_services = pd.read_csv('data/services.csv')

    # 3. Preprocess (Same as train.py)
    df_items['Source'] = 'Item'
    df_services['Source'] = 'Service'
    df_items = df_items.rename(columns={'ItemName': 'Name', 'ItemID': 'TransactionID'})
    df_services = df_services.rename(columns={'ServiceName': 'Name', 'ServiceID': 'TransactionID'})
    
    df_transactions = pd.concat([df_items, df_services], ignore_index=True)
    df_full = df_transactions.merge(df_claims, on='ClaimID', how='left')

    # Encode categorical features using saved encoders
    df_full['Name_Enc'] = encoders['Name'].transform(df_full['Name'])
    df_full['Gender_Enc'] = encoders['Gender'].transform(df_full['PatientGender'])
    df_full['HF_Enc'] = encoders['HF'].transform(df_full['HFID'])
    df_full['Diag_Enc'] = encoders['Diag'].transform(df_full['DiagnosisID'])

    features = ['Quantity', 'UnitPrice', 'TotalAmount', 'PatientAge', 'Name_Enc', 'Gender_Enc', 'HF_Enc', 'Diag_Enc']
    X = df_full[features]
    
    # Scale
    X_scaled = scaler.transform(X)

    # 4. Predict
    print("Running model inference...")
    df_full['Prob_Fraud'] = model.predict_proba(X_scaled)[:, 1]
    df_full['Predicted_Fraud'] = model.predict(X_scaled)

    # 5. Apply 3-Tier Classification
    tier_threshold_high = 0.7
    tier_threshold_low = 0.3

    claim_summary = df_full.groupby('ClaimID').agg({
        'Prob_Fraud': ['max', 'mean', 'count'],
        'TotalAmount': 'sum'
    })
    claim_summary.columns = ['Max_Risk', 'Avg_Risk', 'Item_Count', 'Total_Claim_Amount']

    def get_tier(max_risk):
        if max_risk < tier_threshold_low:
            return 'Fully Accepted'
        elif max_risk >= tier_threshold_high:
            return 'Fully Rejected'
        else:
            return 'Partially Rejected'

    claim_summary['Tier'] = claim_summary['Max_Risk'].apply(get_tier)

    # 6. Display Results (Top 10 most suspicious)
    print("\n--- Top 10 High-Risk Claims ---")
    print(claim_summary.sort_values(by='Max_Risk', ascending=False).head(10))

    # Save results
    claim_summary.to_csv('data/latest_inference_results.csv')
    print("\nFull results saved to: data/latest_inference_results.csv")

if __name__ == "__main__":
    run_inference()
