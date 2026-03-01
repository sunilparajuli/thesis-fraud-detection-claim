# Health Insurance False Claim Detection Thesis

This repository contains the thesis proposal and research materials for the project "AI-Based False Claim Detection System for Health Insurance: Probabilistic Risk Assessment".

## Contents
- [thesis_proposal.md](file:///d:/thesis/thesis_proposal.md): The full thesis proposal document including literature review (10 studies), methodology, and research timeline.
- [implementation_plan.md](file:///d:/thesis/implementation_plan.md): The technical roadmap for the experimental phase.

## Research Objective
To develop an AI-based system that calculates the probability of false claims and classifies them into a three-tier risk hierarchy (Fully Rejected, Partially Rejected, Fully Accepted).

## Methodology
- **Data Source**: openIMIS (Python backend)
- **Primary Algorithm candidates**: XGBoost, Random Forest, LightGBM/CatBoost.
- **Evaluation**: F1-Score, AUC-ROC, and Precision-Recall analysis focused on minimizing False Negatives.

## Results (Synthetic POC)
- **Model**: XGBoost Classifier
- **Accuracy**: 94%
- **F1-Score**: 0.51 (Synthetic Fraud Minority Class)
- **ROC-AUC**: 0.73
- **3-Tier Distribution**:
    - Fully Accepted: 780 claims
    - Partially Rejected: 220 claims

## Repository Structure
- `src/`: Source code for data generation and model training.
- `data/`: Relational synthetic data (CSV) and risk assessment results.
- `models/`: Serialized model and preprocessing artifacts.
- `thesis_proposal.md`: Comprehensive thesis proposal.
