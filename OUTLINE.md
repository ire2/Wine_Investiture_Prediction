# Project Code Outline: Fine Wine Investment Prediction

**Author:** Ignacio Estrada Cavero \
**Completion Goal:** April 2025

## Overview

This document outlines the project structure, files, directories, and development steps required to implement the multi-modal deep learning wine investment prediction model, including future integration for a mobile application enabling users to scan wine bottles.

## Directory Structure

```bash
FineWineInvestmentPrediction/
├── data/
│   ├── auction_prices/
│   ├── reviews/
│   ├── weather/
│   └── images/
├── data_processing/
│   ├── preprocess_tabular.py
│   ├── preprocess_text.py
│   ├── preprocess_images.py
│   └── preprocess_timeseries.py
├── models/
│   ├── tabnet_model.py
│   ├── lstm_timeseries.py
│   ├── bert_text.py
│   ├── cnn_images.py
│   └── fusion_model.py
├── training/
│   ├── train.py
│   └── hyperparameter_tuning.py
├── evaluation/
│   ├── evaluate.py
│   └── benchmark_models.py
├── interpretability/
│   ├── interpret_tabnet.py
│   ├── interpret_text.py
│   └── interpret_image.py
├── app_integration/
│   ├── api/
│   │   ├── api.py
│   │   └── utils.py
│   └── frontend/
│       ├── mobile_app/
│       ├── app_frontend/
│       ├── App.js
│       ├── ScannerComponent.js
│       └── ResultsDisplay.js
│   └── backend/
│       ├── api.py
│       └── inference.py
├── utils/
│   ├── data_loader.py
│   ├── train_test_split.py
│   └── evaluation_metrics.py
├── notebooks/
│   ├── exploratory_analysis.ipynb
│   └── model_testing.ipynb
├── results/
│   ├── model_results/
│   └── visualizations/
├── requirements.txt
└── README.md
```

## Development Steps & Descriptions

### Step 1: Data Collection and Preparation

- **Tabular Data:** Collect and preprocess structured data including wine attributes (region, vineyard, scores).
- **Textual Data:** Gather and preprocess textual wine reviews.
- **Image Data:** Collect, resize, and normalize wine bottle images.
- **Time-Series Data:** Structure historical pricing and macroeconomic indicators.

### Step 2: Preprocessing

- **`preprocess_tabular.py`:** Clean, encode, and normalize tabular data.
- **`preprocess_text.py`:** Tokenize texts and generate embeddings using BERT.
- **`preprocess_images.py`:** Prepare image data for CNN models.
- **`preprocess_timeseries.py`:** Format time-series data for LSTM modeling.

### Step 3: Model Development

#### Tabular Model (TabNet)

- **`tabnet_model.py`:** Develop and train TabNet model for structured features.

#### Text Model (BERT)

- **`bert_text.py`:** Fine-tune BERT for embedding textual reviews.

#### Image Model (CNN)

- **`cnn_image.py`:** Fine-tune pre-trained CNN (ResNet) for image feature extraction.

#### Time-Series Model (LSTM)

- **`lstm_timeseries.py`:** Implement LSTM to capture sequential price and economic trends.

#### Fusion Model

- **`fusion_model.py`:** Integrate TabNet, LSTM, BERT, and CNN embeddings into a unified multimodal architecture.

### Step 3: Training Procedure

- **Hyperparameter tuning:** Use grid search or Bayesian optimization.
- **Modality training:** Train subnetworks individually, then combine and fine-tune end-to-end.

### Step 4: Model Evaluation

- **`evaluate.py`:** Compute RMSE, R², ROC AUC, Sharpe, and Sortino ratios.
- **Monte Carlo simulations:** Evaluate investment strategy robustness.
- **Ablation studies:** Quantify contribution from each data modality.

### Step 4: Interpretability & Analysis

- **`interpret_tabnet.py`:** Visualize TabNet feature importances.
- **`interpret_text.py`:** Apply SHAP/LIME to interpret textual data impact.
- **`interpret_image.py`:** Generate saliency maps to analyze CNN predictions.

### Step 5: Comparative Benchmarking

- Implement baseline models (Linear Regression, XGBoost, Random Forest, ARIMA) for comparison.
- Evaluate all models using the same metrics (RMSE, R², ROC AUC).

### Step 6: Visualization & Reporting

- Create clear visualizations:
  - Calibration plots
  - Error distribution histograms
  - ROI comparisons
- Save charts and tables in a `results/` directory.

### Step 7: Documentation & Reproducibility

- **`README.md`:** Provide a project overview, setup instructions, and usage guide.
- **`requirements.txt`:** Document project dependencies.
- **`run_experiments.sh`:** Automate data processing, training, evaluation, and visualization.

### Step 8: Future Enhancement - App Integration

- Develop mobile app functionality for bottle scanning and real-time predictions.
  - **Frontend:** React Native or similar for image capture and result display.
  - **Backend:** API for inference and response management.

### Additional Resources

- **`utils/` directory:** Include common utilities for data loading, splitting, and evaluation metrics.
- **`run_experiments.sh`:** Automate the execution of the entire pipeline.



## Future Integration: App Development

### Step 7: App Integration (Future Enhancement)

- **Frontend (React Native or similar):**
  - Develop a mobile application enabling users to scan wine bottles using device cameras.
  - Implement image capture and uploading functionality.

- **Backend API:**
  - Build a lightweight RESTful API endpoint serving model predictions.
  - Integrate the trained CNN model to perform real-time inference based on uploaded images.

- **Workflow:**
  - User scans bottle → Image is uploaded → Backend performs inference → Prediction and investment insights are returned → Frontend displays results clearly and intuitively.

### Step 8: Deployment & Scalability

- Consider deploying backend model to cloud services like AWS, GCP, or Azure.
- Evaluate scalability options like Kubernetes for managing increased user traffic and simultaneous inference requests.

This addition ensures the model is not only academically robust but also practically accessible to end-users, enhancing the project's commercial viability.

