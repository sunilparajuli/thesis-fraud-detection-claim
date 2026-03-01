-- openIMIS Fraud Detection Data Extraction Script (MSSQL Version)
-- Optimized for Thesis: "AI-Based False Claim Detection System"
-- Purpose: Extracts both Accepted and Rejected claims to create Ground Truth labels.

WITH ClaimBase AS (
    -- Extract Items
    SELECT 
        c.ClaimID,
        c.HFID,
        c.ICDID AS DiagnosisID,
        i.DOB,
        i.Gender AS PatientGender,
        it.ItemName AS Name,
        ci.QtyProvided AS Quantity,
        ci.PriceAsked AS UnitPrice,
        (ci.QtyProvided * ci.PriceAsked) AS TotalAmount,
        'Item' as Source,
        ci.RejectionReason,
        ci.ClaimItemStatus as Status,
        -- Ground Truth Label Logic (Thesis Proposal 3.2.2)
        -- 1 = Fraud/Rejected, 0 = Accepted
        CASE 
            WHEN ci.RejectionReason != 0 OR ci.ClaimItemStatus = 1 THEN 1 
            ELSE 0 
        END AS IsFraud
    FROM tblClaim c
    JOIN tblInsuree i ON c.InsureeID = i.InsureeID
    JOIN tblClaimItems ci ON c.ClaimID = ci.ClaimID
    JOIN tblItems it ON ci.ItemID = it.ItemID
    WHERE c.ValidityTo IS NULL

    UNION ALL

    -- Extract Services
    SELECT 
        c.ClaimID,
        c.HFID,
        c.ICDID AS DiagnosisID,
        i.DOB,
        i.Gender AS PatientGender,
        s.ServName AS Name, -- Using ServName as per user request
        cs.QtyProvided AS Quantity,
        cs.PriceAsked AS UnitPrice,
        (cs.QtyProvided * cs.PriceAsked) AS TotalAmount,
        'Service' as Source,
        cs.RejectionReason,
        cs.ClaimServiceStatus as Status,
        -- Ground Truth Label Logic (Thesis Proposal 3.2.2)
        -- 1 = Fraud/Rejected, 0 = Accepted
        CASE 
            WHEN cs.RejectionReason != 0 OR cs.ClaimServiceStatus = 1 THEN 1 
            ELSE 0 
        END AS IsFraud
    FROM tblClaim c
    JOIN tblInsuree i ON c.InsureeID = i.InsureeID
    JOIN tblClaimServices cs ON c.ClaimID = cs.ClaimID
    JOIN tblServices s ON cs.ServiceID = s.ServiceID
    WHERE c.ValidityTo IS NULL
)
SELECT 
    *,
    -- Calculate Age (MSSQL syntax)
    DATEDIFF(year, DOB, GETDATE()) - 
    CASE 
        WHEN MONTH(DOB) > MONTH(GETDATE()) OR (MONTH(DOB) = MONTH(GETDATE()) AND DAY(DOB) > DAY(GETDATE())) 
        THEN 1 
        ELSE 0 
    END AS PatientAge
FROM ClaimBase;
