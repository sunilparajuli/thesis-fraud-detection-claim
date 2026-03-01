# Thesis Proposal Expansion Plan

This plan outlines the steps to expand the provided thesis proposal into a comprehensive academic document.

## Proposed Sections and Changes

### 1. Introduction
- **1.1 Background**: Expand on the importance of digital health interventions and why automated claim processing is critical for platforms like openIMIS.
- **1.2 Problem Statement**: Quantify the impact where possible (e.g., loss percentages) and refine the 4 listed points. Focus on the transition from manual review to AI-assisted probabilistic risk assessment.
- **1.3 Rationale/Significance**: Explain how this research reduces financial leakage in health insurance and improves the efficiency of medical officers using openIMIS.
- **1.4 Research Objectives**:
    - **Primary**: Develop a system to calculate fraud probability and classify claims into three tiers (Fully Rejected, Partially Rejected, Fully Accepted).
    - **Secondary**: Compare performance of 7 ML classifiers (Logistic Regression, Decision Trees, Random Forest, XGBoost, SVM, KNN, ANN).

### 2. Literature Review
- **2.1 Traditional Fraud Detection**: Overview of rule-based systems.
- **2.2 Machine Learning in Healthcare**: General applications and recent successes.
- **2.3 Challenges in Claim Fraud Detection**: Data imbalance (low fraud rate), real-time processing, and adversarial behavior.
- **2.4 Item-Level vs. Claim-Level Analysis**: Discuss the gap in current literature regarding partial rejection and how this thesis addresses it using `tblClaimItems` and `tblClaimServices`.

### 3. Research Methodology
- **3.1 Conceptual Framework**: Diagrammatic representation of the system flow: Data Extraction → Feature Engineering → Probability Calculation → 3-Tier Classification.
- **3.2 Data Engineering**:
    - **Source**: openIMIS python backend (`claim` module).
    - **Key Tables**: `tblClaim` (header), `tblClaimItems` (medications), `tblClaimServices` (services).
    - **Features**: Patient history, diagnosis codes (`icd` to `icd_4`), facility level, and custom fraud rules (duplicate billing, etc.).
- **3.3 Algorithmic Approach**: Deeper dive into WHY these 7 models were chosen.
- **3.4 Probabilistic Risk Assessment**: Logic for calculating the 0-100% score based on model outputs (e.g., Softmax or Sigmoid probabilities).
- **3.5 Three-Tier Classification Logic**:
    - **Fully Accepted**: All items/services flagged as legitimate.
    - **Partially Rejected**: Mixed status where some items/services are flagged as fraudulent.
    - **Fully Rejected**: All items/services flagged as fraudulent.

### 4. Scope and Limitations
- **4.1 Scope**: Focus on billing and pattern-based fraud detected in historical `openIMIS` data.
- **4.2 Limitations**: Dependency on data quality, potential label noise in historical rejections.

### 5. Ethical Considerations
- **5.1 Data Privacy**: Anonymization of `Insuree` and `HealthFacility` identifiers.
- **5.2 Explainability (XAI)**: Importance of providing reasons for rejection (e.g., via SHAP or LIME) to help medical officers.

### 6. Expected Results and Timeline
- Refine the deliverables and impact sections.

## Verification Plan

### Content Review
- Check for academic tone and professional language.
- Ensure logical flow between sections.
- Verify that the methodology directly addresses the problem statement.
- Ensure all openIMIS specific tables are correctly referenced.

### Formatting
- Standard markdown structure for readability.
- Consistent heading levels.
