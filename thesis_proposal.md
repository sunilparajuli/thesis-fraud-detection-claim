---
title: "AI-Based False Claim Detection System for Health Insurance"
subtitle: "A Probabilistic Risk Assessment Approach for openIMIS"
author: "Thesis Candidate"
date: "March 2026"
---

# THESIS PROPOSAL

## Table of Contents
1. [Introduction](#1-introduction)
2. [Literature Review](#2-literature-review)
3. [Research Methodology](#3-research-methodology)
4. [Scope, Limitations, and Ethics](#4-scope-limitations-and-ethics)
5. [Expected Results](#5-expected-results)
6. [Research Timeline](#6-research-timeline)
7. [Conclusion](#7-conclusion)

---

### 1. INTRODUCTION

#### 1.1 Background
The digital transformation of healthcare systems has led to the adoption of platforms like openIMIS, which streamline health insurance operations globally. These platforms process thousands of claims daily, ranging from simple medication dispensations to complex surgical procedures. However, the sheer volume of data makes manual review by medical officers both impractical and inefficient. In most insurance environments, only a small fraction (typically <10%) of claims can be manually audited, leaving a significant window for fraudulent activities, billing errors, and abuse. 

Automated fraud detection is no longer a luxury but a necessity for the financial sustainability of health insurance schemes. By utilizing Artificial Intelligence (AI) and Machine Learning (ML), insurance providers can transition from reactive, manual audits to proactive, data-driven oversight. This research proposes a system that not only identifies potential fraud but also provides a probabilistic risk score, allowing for efficient prioritization of manual reviews.

#### 1.2 Problem Statement
Healthcare insurance fraud accounts for billions of dollars in losses annually, directly impacting the quality of care and the affordability of insurance premiums. The openIMIS platform, despite its robust administrative features, faces several critical challenges in claim oversight:
1.  **Low Manual Coverage**: The inability of medical officers to review 100% of claims leads to undetected "leakage" where fraudulent claims are paid out.
2.  **Lack of Probability-Based Assessment**: Current systems often use binary rules (pass/fail), failing to account for the nuance of "suspicious but uncertain" claims.
3.  **Binary Claim Treatment**: Most fraud detection research focuses on the claim level, whereas in reality, a claim might be "partially" fraudulent (e.g., three services are legitimate, but one is overbilled).
4.  **Resource Prioritization**: Without a standardized risk score, medical officers lack a systematic way to prioritize which claims warrant intensive manual investigation.

#### 1.3 Rationale and Significance
The significance of this research lies in its potential to safeguard the financial integrity of health insurance funds. By implementing a three-tier classification system (Fully Accepted, Partially Rejected, and Fully Rejected), the system mimics the decision-making process of human experts but at a scale impossible for manual review. The inclusion of item-level analysis (`tblClaimItems` and `tblClaimServices`) ensures that legitimate services are not penalized due to a single fraudulent item, thus maintaining trust between providers and insurers.

#### 1.4 Research Objectives
**Primary Objective:**
To develop an AI-based system that calculates the probability of false claims (in percentage) and classifies them into a three-tier risk hierarchy:
-   **Fully Rejected**: Claims where all items/services are identified as fraudulent.
-   **Partially Rejected**: Claims where a subset of items/services are fraudulent.
-   **Fully Accepted**: Claims where all items/services are verified as legitimate.

**Secondary Objectives:**
1.  To engineer novel fraud pattern features based on historical openIMIS claim data.
2.  To evaluate and compare the performance of multiple ML classifiers (Logistic Regression, Random Forest, XGBoost, etc.) to identify the most accurate model for health insurance fraud.
3.  To establish optimal probability thresholds that balance the trade-off between sensitivity (catching fraud) and specificity (avoiding false alarms).

---

### 2. LITERATURE REVIEW

#### 2.1 Analysis of 10 Specific Academic Papers (2022-2025)
The following papers provide the academic foundation for this study, covering diverse aspects of healthcare fraud detection:

1.  **Narne, H. (2024)**: *"Machine Learning for Health Insurance Fraud Detection: Techniques, Insights, and Implementation Strategies."* This study provides a comprehensive overview of ML techniques and emphasizes practical implementation strategies within healthcare systems.
2.  **Gupta, G., et al. (2024)**: *"Integrating Blockchain with Machine Learning for Fraud Detection in Health Insurance Claims Management."* Explores a hybrid approach using blockchain for immutable record-keeping and ML for pattern recognition.
3.  **Samara, B. (2024)**: *"Using Binary Logistic Regression to Detect Health Insurance Fraud."* A focused study on the efficacy of logistic regression for classifying claims as fraudulent or legitimate.
4.  **Duman, E. (2022)**: *"Implementation of XGBoost Method for Healthcare Fraud Detection."* Demonstrates the superior performance of the XGBoost algorithm in identifying complex fraudulent patterns in large datasets.
5.  **Surjuse, A., & Deshmukh, S. (2024)**: *"Securing Healthcare Finances: AI Approach to Insurance Fraud Detection."* Discusses various AI and ML techniques aimed specifically at safeguarding financial resources in healthcare.
6.  **Chaurasiya, R., & Jain, K. (2025)**: *"Healthcare Fraud Detection Using Machine Learning Ensemble Methods."* Utilizes ensemble models (XGBoost, LightGBM) and SMOTE to address class imbalance in Medicare datasets.
7.  **Chengamma Chitteti, et al. (2025)**: *"Healthcare Insurance Fraud Detection Using Machine Learning."* Proposes an intelligent fraud detection system integrating blockchain and supervised learning, noting high performance with Random Forest.
8.  **SSRN Research (2025)**: *"Designing an Intelligent Fraud Detection System for Healthcare Insurance Claims Using a Machine Learning Approach."* Employs ADASYN for data balancing and Mutual Information for feature selection, highlighting the Extra Trees Classifier.
9.  **ArXiv Research (2025)**: *"An Attack Method for Medical Insurance Claim Fraud Detection based on Generative Adversarial Network."* Demonstrates vulnerabilities to GAN-based adversarial attacks, emphasizing the need for robust detection models.
10. **NIH Research (2025)**: *"A robust and interpretable ensemble machine learning model for predicting healthcare insurance fraud."* Develops a model using CatBoost, XGBoost, and LightGBM, focusing on interpretability and feature engineering.

#### 2.2 Research Gap and Highlight of This Work
Current literature primarily treats claims as binary units. This work addresses the **Relational Gap** by:
-   **Granular Analysis**: Targeting individual items/services in `tblClaimItems` and `tblClaimServices`.
-   **Three-Tier Logic**: Formally defining "Partially Rejected" status, a nuance missing in standard ML fraud research.

---

### 3. RESEARCH METHODOLOGY

#### 3.1 Research Design
This study follows a quantitative experimental design. A unique feature of this methodology is the **Two-Stage Algorithmic Selection Process**, ensuring both theoretical and empirical rigor.

#### 3.2 Data Collection and Preprocessing Strategy
The success of the risk assessment model depends heavily on the quality and preparation of the historical data extracted from openIMIS. The following strategy will be implemented:

**3.2.1 Data Extraction and Source Strategy**
Historical claim data spanning a minimum of 24 months will be extracted from the production/staging instances of openIMIS. The extraction strategy focuses on capturing the relational hierarchy of claims:
- **Header Level**: Claims (`tblClaim`) providing context on patient demographics and primary diagnosis.
- **Transactional Level**: Items and Services (`tblClaimItems`, `tblClaimServices`) which contain the actual quantities and prices billed.
- **Reference Level**: Health Facility (`tblHF`) and Diagnosis (`tblICDCodes`) tables to provide categorical context.

**3.2.2 Data Labeling and Ground Truth**
The "Ground Truth" for this supervised learning model will be derived from the historical decisions made by medical officers. 
- **Target Variable (Label)**: A binary indicator where `1` represents a "Fraudulent/Rejected" item (mapped from openIMIS `RejectionReason != 0` or `Status = 1`) and `0` represents an "Accepted" item.
- **Label Cleaning**: Claims marked as "Rejected" for administrative errors (e.g., incorrect ID) will be filtered out to ensure the model focuses purely on fraudulent patterns and medical billing abuse.

**3.2.3 Data Preprocessing Strategy**
- **Handling Missing Values**: Numerical missing data (e.g., price asked) will be imputed using the median of that specific service category, while categorical missing data will be filled with a "Unknown" flag.
- **Feature Scaling**: Continuous variables (Total Amount, Quantities) will be normalized using **StandardScaler** to ensure different units (currency vs. count) contribute equally to the model's distance calculations.
- **Class Imbalance Strategy**: Since fraudulent claims typically constitute <5% of health insurance data, **SMOTE (Synthetic Minority Over-sampling Technique)** will be applied to the training set to prevent the model from becoming biased toward the "Legitimate" majority class.

**3.2.4 Data Splitting Strategy**
To ensure robust evaluation and prevent overfitting, the dataset will be divided into three distinct subsets:
- **Training Set (70%)**: Used for the primary training of the 7 candidate classifiers.
- **Validation Set (15%)**: Used for hyperparameter tuning and early stopping during ANN training.
- **Test Set (15%)**: A "hold-out" set of unseen data used to calculate final performance metrics (F1-Score, AUC-ROC) to guarantee the model's generalizability to future claims.

#### 3.3 Feature Engineering
Features will be engineered around pattern-based rules (duplicate scans, diagnosis timing) and statistical anomalies (z-scores of amounts).

#### 3.4 Multi-Stage Algorithm Selection Process
To identify the most effective solution for openIMIS, the following selection process will be strictly followed:

**Stage 1: Selection of Top Three Candidates (From Literature)**
Based on the extensive literature review in Section 2, the three most promising and robust algorithms will be shortlisted:
1.  **XGBoost**: Known for its state-of-the-art performance and class imbalance handling.
2.  **Random Forest**: Valued for its stability and interpretability.
3.  **LightGBM/CatBoost**: Selected for their efficiency and handling of categorical data like diagnosis codes.

**Stage 2: Empirical Selection of the "Best" Algorithm**
The three selected candidates will be rigorously trained and tested on the historical openIMIS dataset. The model that achieves the highest **F1-Score** and **AUC-ROC**—while maintaining reasonable interpretability for medical officers—will be selected as the final "Best" algorithm to perform the fraud detection and risk assessment work within the system.



#### 3.5 The Three-Tier Classification Logic
The system will implement a bottom-up classification logic:

1.  **Item/Service Level Prediction (Step 1)**: The ML model predicts the probability ($P_{item}$) of fraud for each individual entry in `tblClaimItems` and `tblClaimServices`.
2.  **Claim Level Aggregation (Step 2)**:
    -   **Fully Accepted**: If for all items ($i$), $P_{item,i} < Threshold_{Low}$.
    -   **Partially Rejected**: If some items ($i$) have $P_{item,i} \geq Threshold_{High}$, while others have $P_{item,i} < Threshold_{Low}$.
    -   **Fully Rejected**: If for all items ($i$), $P_{item,i} \geq Threshold_{High}$.
3.  **Risk Probability Output**: The overall claim risk will be represented as a percentage, calculated as the maximum risk score found among its constituent items, ensuring that even a single highly fraudulent item flags the claim for review.

#### 3.6 Evaluation Metrics
In the context of imbalanced fraud data, **Accuracy** is a misleading metric. This research will prioritize:
-   **Precision-Recall Curve & F1-Score**: To ensure minimal false accusations while catching maximal fraud.
-   **AUC-ROC**: To evaluate the model's ability to distinguish between classes across all thresholds.
-   **Confusion Matrix**: Specifically focusing on minimizing **False Negatives** (missed fraud) which represent direct financial loss.

---

### 4. SCOPE, LIMITATIONS, AND ETHICS

#### 4.1 Scope
The research focuses on **Billing Fraud** (e.g., duplicate billing, phantom services, upcoding) within the openIMIS ecosystem. It does not cover medical malpractice or clinical outcome assessment which requires clinical trial data.

#### 4.2 Limitations
-   **Data Quality**: The model's performance is bound by the accuracy of historical rejection labels in openIMIS.
-   **Concept Drift**: Fraud patterns change over time; the model trained on 2024 data may require retraining for 2026 patterns.

#### 4.3 Ethical Considerations
-   **Data Privacy**: All personally identifiable information (PII) like names and exact addresses will be anonymized before being fed into the ML pipeline, adhering to global health data standards (GDPR/HIPAA principles).
-   **Algorithmic Bias**: The study will test for bias to ensure that the system does not unfairly target specific demographics or rural health facilities.

---

### 5. EXPECTED RESULTS

#### 5.1 Deliverables
The primary output of this thesis will be a validated **AI-Based Fraud Detection System** for openIMIS, consisting of:
-   **A Comparative Performance Report**: Detailing the accuracy, precision, and recall of all seven classifiers.
-   **A Trained Model Artifact**: A production-ready XGBoost (or otherwise selected) model.
-   **Granular Feature Set**: A library of Python-based feature extraction scripts compatible with the openIMIS database schema.
-   **Decision Support API**: A conceptual API that medical officers can query to obtain a risk probability for any given claim.

#### 5.2 Expected Outcomes
-   **Increased Detection Rates**: Identifying 75-90% of fraudulent patterns that are currently missed by manual audits.
-   **Reduction in Workload**: Filtering out "Fully Accepted" claims to reduce the manual audit workload by at least 50%.
-   **Improved Financial Planning**: More accurate forecasting of insurance fund liabilities by accounting for potential fraudulent outflows.

#### 5.3 Academic and Practical Contributions
-   **Academic**: Establishing a benchmark for item-level fraud detection in health insurance platforms.
-   **Practical**: Providing the openIMIS community with a tool to enhance the financial sustainability of universal health coverage schemes.

---

### 6. RESEARCH TIMELINE

| Phase | Activity | Duration |
| :--- | :--- | :--- |
| **Phase 1** | Data Acquisition & Cleaning (openIMIS Extraction) | 2 Weeks |
| **Phase 2** | Feature Engineering & Rule Implementation | 2 Weeks |
| **Phase 3** | Model Training & Hyperparameter Tuning | 3 Weeks |
| **Phase 4** | Model Evaluation & Selection | 1 Week |
| **Phase 5** | Threshold Optimization & 3-Tier Validation | 1 Week |
| **Phase 6** | Final Thesis Write-up & Defense Preparation | 3 Weeks |
| **Total** | | **12 Weeks** |

---

### 7. CONCLUSION
This thesis proposal outlines a data-driven approach to solving one of the most persistent challenges in health insurance—claim fraud. By moving beyond binary classification and implementing a probabilistic, item-level assessment, the proposed system provides openIMIS with a sophisticated, scalable, and fair mechanism for risk management.
