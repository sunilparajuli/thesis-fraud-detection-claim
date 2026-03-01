import pandas as pd
import psycopg2
from datetime import datetime
import os

def extract_from_openimis(db_config):
    """
    Extracts claim data from openIMIS PostgreSQL database.
    db_config = {
        'dbname': 'openimis',
        'user': 'postgres',
        'password': 'your_password',
        'host': 'localhost',
        'port': '5432'
    }
    """
    print("Connecting to openIMIS database...")
    try:
        conn = psycopg2.connect(**db_config)
        
        query = """
        SELECT 
            c."ClaimID",
            c."HFID",
            c."ICDID" AS "DiagnosisID",
            i."DOB",
            i."Gender" AS "PatientGender",
            it."ItemName" AS "Name",
            ci."QtyProvided" AS "Quantity",
            ci."PriceAsked" AS "UnitPrice",
            (ci."QtyProvided" * ci."PriceAsked") AS "TotalAmount",
            CASE WHEN ci."RejectionReason" > 0 THEN 1 ELSE 0 END as "IsFraud_Synthetic" -- Placeholder if labels don't exist
        FROM "tblClaim" c
        JOIN "tblInsuree" i ON c."InsureeID" = i."InsureeID"
        JOIN "tblClaimItems" ci ON c."ClaimID" = ci."ClaimID"
        JOIN "tblItems" it ON ci."ItemID" = it."ItemID"
        WHERE c."ValidityTo" IS NULL

        UNION ALL

        SELECT 
            c."ClaimID",
            c."HFID",
            c."ICDID" AS "DiagnosisID",
            i."DOB",
            i."Gender" AS "PatientGender",
            s."ServiceName" AS "Name",
            cs."QtyProvided" AS "Quantity",
            cs."PriceAsked" AS "UnitPrice",
            (cs."QtyProvided" * cs."PriceAsked") AS "TotalAmount",
            CASE WHEN cs."RejectionReason" > 0 THEN 1 ELSE 0 END as "IsFraud_Synthetic"
        FROM "tblClaim" c
        JOIN "tblInsuree" i ON c."InsureeID" = i."InsureeID"
        JOIN "tblClaimServices" cs ON c."ClaimID" = cs."ClaimID"
        JOIN "tblServices" s ON cs."ServiceID" = s."ServiceID"
        WHERE c."ValidityTo" IS NULL;
        """
        
        print("Executing extraction query...")
        df = pd.read_sql_query(query, conn)
        
        # Post-processing
        print("Processing demographics...")
        df['DOB'] = pd.to_datetime(df['DOB'])
        # Simplified age calculation
        df['PatientAge'] = datetime.now().year - df['DOB'].dt.year
        
        # Save results
        os.makedirs('data/real', exist_ok=True)
        df.to_csv('data/real/extracted_claims.csv', index=False)
        print(f"Extraction complete. {len(df)} records saved to data/real/extracted_claims.csv")
        
        conn.close()
        return df

    except Exception as e:
        print(f"Error during extraction: {e}")
        return None

if __name__ == "__main__":
    # Example usage - user should replace with their actual credentials
    config = {
        'dbname': 'openimis',
        'user': 'postgres',
        'password': 'password',
        'host': 'localhost',
        'port': '5432'
    }
    # extract_from_openimis(config)
    print("Please configure the database credentials in src/extract_data.py and run it.")
