import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_synthetic_data(n_claims=1000):
    print(f"Generating {n_claims} synthetic claims...")
    
    # 1. Generate tblClaim (Header)
    claims = []
    hf_ids = ['HF001', 'HF002', 'HF003', 'HF004', 'HF005']
    diagnoses = ['D001', 'D002', 'D003', 'D004', 'D005'] # Represented as ICD-style
    
    start_date = datetime(2024, 1, 1)
    
    for i in range(n_claims):
        claim_id = f"CLM_{1000+i}"
        patient_age = np.random.randint(1, 85)
        patient_gender = random.choice(['M', 'F'])
        hf_id = random.choice(hf_ids)
        diagnosis_id = random.choice(diagnoses)
        claim_date = start_date + timedelta(days=np.random.randint(0, 365))
        
        claims.append({
            'ClaimID': claim_id,
            'PatientAge': patient_age,
            'PatientGender': patient_gender,
            'HFID': hf_id,
            'DiagnosisID': diagnosis_id,
            'ClaimDate': claim_date.strftime('%Y-%m-%d')
        })
        
    df_claims = pd.DataFrame(claims)
    
    # 2. Generate tblClaimItems and tblClaimServices
    items_data = []
    services_data = []
    
    item_catalog = {
        'Paracetamol': 5.0,
        'Amoxicillin': 25.0,
        'Artesunate': 50.0,
        'Ibuprofen': 10.0,
        'Normal Saline': 15.0
    }
    
    service_catalog = {
        'Consultation': 100.0,
        'Lab Test - Malaria': 150.0,
        'X-Ray': 500.0,
        'Inpatient Stay (Day)': 1000.0,
        'Physical Therapy': 200.0
    }
    
    for claim_id in df_claims['ClaimID']:
        # Randomly choose number of items and services
        n_items = np.random.randint(0, 5)
        n_services = np.random.randint(1, 3) # At least one consultation usually
        
        # Items logic
        for j in range(n_items):
            item_name = random.choice(list(item_catalog.keys()))
            unit_price = item_catalog[item_name]
            quantity = np.random.randint(1, 10)
            
            # Inject Fraud: High quantity for expensive item
            is_fraud = 0
            if item_name == 'Artesunate' and quantity > 7:
                is_fraud = 1 # Over-prescribing
            elif random.random() < 0.05: # Random noise fraud
                is_fraud = 1
                
            total = quantity * unit_price
            items_data.append({
                'ItemID': f"ITM_{len(items_data)}",
                'ClaimID': claim_id,
                'ItemName': item_name,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'TotalAmount': total,
                'IsFraud': is_fraud
            })
            
        # Services logic
        for k in range(n_services):
            service_name = random.choice(list(service_catalog.keys()))
            unit_price = service_catalog[service_name]
            quantity = 1
            
            # Inject Fraud: Upcoding or unnecessary expensive services
            is_fraud = 0
            if service_name == 'X-Ray' and random.random() < 0.2:
                is_fraud = 1 # Potentially unnecessary
            elif random.random() < 0.03:
                is_fraud = 1
                
            total = quantity * unit_price
            services_data.append({
                'ServiceID': f"SRV_{len(services_data)}",
                'ClaimID': claim_id,
                'ServiceName': service_name,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'TotalAmount': total,
                'IsFraud': is_fraud
            })
            
    df_items = pd.DataFrame(items_data)
    df_services = pd.DataFrame(services_data)
    
    # Save to data directory
    os.makedirs('data', exist_ok=True)
    df_claims.to_csv('data/claims.csv', index=False)
    df_items.to_csv('data/items.csv', index=False)
    df_services.to_csv('data/services.csv', index=False)
    
    print("Files saved to data/ directory.")
    return df_claims, df_items, df_services

if __name__ == "__main__":
    generate_synthetic_data()
