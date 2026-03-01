import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, f1_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os
import pickle

def prepare_and_train():
    # Load data
    print("Loading synthetic data...")
    df_claims = pd.read_csv('data/claims.csv')
    df_items = pd.read_csv('data/items.csv')
    df_services = pd.read_csv('data/services.csv')
    
    # 1. Feature Engineering (Item Level)
    print("Preparing features...")
    
    # Merge items and services into a single transactional dataframe
    df_items['Source'] = 'Item'
    df_services['Source'] = 'Service'
    
    # Rename columns for consistency
    df_items = df_items.rename(columns={'ItemName': 'Name', 'ItemID': 'TransactionID'})
    df_services = df_services.rename(columns={'ServiceName': 'Name', 'ServiceID': 'TransactionID'})
    
    df_transactions = pd.concat([df_items, df_services], ignore_index=True)
    
    # Merge with claim headers
    df_full = df_transactions.merge(df_claims, on='ClaimID', how='left')
    
    # Encode categorical features
    le_name = LabelEncoder()
    df_full['Name_Enc'] = le_name.fit_transform(df_full['Name'])
    
    le_gender = LabelEncoder()
    df_full['Gender_Enc'] = le_gender.fit_transform(df_full['PatientGender'])
    
    le_hf = LabelEncoder()
    df_full['HF_Enc'] = le_hf.fit_transform(df_full['HFID'])
    
    le_diag = LabelEncoder()
    df_full['Diag_Enc'] = le_diag.fit_transform(df_full['DiagnosisID'])
    
    # Prepare features and target
    features = ['Quantity', 'UnitPrice', 'TotalAmount', 'PatientAge', 'Name_Enc', 'Gender_Enc', 'HF_Enc', 'Diag_Enc']
    X = df_full[features]
    y = df_full['IsFraud']
    
    # Scale numerical features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)
    
    # 2. Train Random Forest Model
    print("Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # 3. Evaluation
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    
    print(f"F1-Score: {f1:.4f}")
    print(f"ROC-AUC: {auc:.4f}")
    
    # 4. Save Model and Scaler
    os.makedirs('models', exist_ok=True)
    with open('models/model_xgb.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
        
    # Save label encoders
    encoders = {'Name': le_name, 'Gender': le_gender, 'HF': le_hf, 'Diag': le_diag}
    with open('models/encoders.pkl', 'wb') as f:
        pickle.dump(encoders, f)
        
    print("\nModel and artifacts saved to models/ directory.")
    
    # 5. Three-Tier Logic Implementation (Conceptual Demo)
    print("\nImplementing 3-tier classification on test set claims...")
    df_full.loc[X.index, 'Prob_Fraud'] = model.predict_proba(X_scaled)[:, 1]
    
    # Aggregate to Claim Level
    tier_threshold_high = 0.7
    tier_threshold_low = 0.3
    
    claim_tiers = df_full.groupby('ClaimID').agg({
        'Prob_Fraud': ['max', 'mean', 'all']
    })
    
    # Custom 3-tier logic
    def classify_tier(row):
        max_prob = row[('Prob_Fraud', 'max')]
        min_prob = df_full[df_full['ClaimID'] == row.name]['Prob_Fraud'].min()
        
        if max_prob < tier_threshold_low:
            return 'Fully Accepted'
        elif min_prob >= tier_threshold_high:
            return 'Fully Rejected'
        else:
            return 'Partially Rejected'
            
    claim_tiers['Tier'] = claim_tiers.apply(classify_tier, axis=1)
    
    print("\n3-Tier Distribution:")
    print(claim_tiers['Tier'].value_counts())
    
    claim_tiers.to_csv('data/claim_risk_assessment.csv')
    print("Risk assessment saved to data/claim_risk_assessment.csv")

if __name__ == "__main__":
    prepare_and_train()
