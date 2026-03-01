import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, f1_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from imblearn.over_sampling import SMOTE
import os
import pickle

def train_on_real_data(file_path='data/real/extracted_claims.csv'):
    """
    Trains the fraud detection model using data extracted from the real SQL database.
    Format expects columns: HFID, DiagnosisID, PatientGender, Name, Quantity, UnitPrice, TotalAmount, PatientAge, IsFraud
    """
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Please run the SQL extraction and save as CSV first.")
        return

    print(f"Loading real-world data from {file_path}...")
    column_names = [
        'ClaimID', 'HFID', 'DiagnosisID', 'DOB', 'PatientGender', 'Name', 
        'Quantity', 'UnitPrice', 'TotalAmount', 'Source', 
        'RejectionReason', 'Status', 'IsFraud', 'PatientAge'
    ]
    df = pd.read_csv(file_path, names=column_names, header=None)
    
    # Preprocessing as per Thesis Proposal 3.2.3
    print("Preprocessing data...")
    
    # Encode categorical features
    encoders = {}
    categorical_cols = ['Name', 'PatientGender', 'HFID', 'DiagnosisID']
    
    for col in categorical_cols:
        le = LabelEncoder()
        df[f'{col}_Enc'] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
    
    # Define features and target
    features = ['Quantity', 'UnitPrice', 'TotalAmount', 'PatientAge', 
                'Name_Enc', 'PatientGender_Enc', 'HFID_Enc', 'DiagnosisID_Enc']
    X = df[features]
    y = df['IsFraud']
    
    # Scale numerical features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data (70/15/15 as per Thesis Proposal 3.2.4)
    # First split into 70% train and 30% temp
    X_train, X_temp, y_train, y_temp = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42, stratify=y
    )
    # Split temp into 15% validation and 15% test
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )
    
    # Handle Class Imbalance using SMOTE (Thesis Proposal 3.2.3)
    print("Applying SMOTE to handle class imbalance...")
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    
    # Train Random Forest Model
    print("Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10, # Increased depth for real complexity
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train_res, y_train_res)
    
    # Evaluation
    print("\n--- Model Evaluation (Test Set) ---")
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    print(classification_report(y_test, y_pred))
    print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.4f}")
    print(f"F1-Score: {f1_score(y_test, y_pred):.4f}")
    
    # Save artifacts
    os.makedirs('models/real', exist_ok=True)
    with open('models/real/model_rf.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('models/real/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    with open('models/real/encoders.pkl', 'wb') as f:
        pickle.dump(encoders, f)
        
    print("\nModel and artifacts saved to models/real/ directory.")

if __name__ == "__main__":
    train_on_real_data()
