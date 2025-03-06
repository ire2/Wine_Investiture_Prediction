#!/bin/bash

# Project directory name
PROJECT_DIR="Wine_Investiture_Prediction"

# Create project root directory
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Data directories
mkdir -p data/{auction_prices,reviews,weather,images}

# Data processing scripts
mkdir -p data_processing
for script in preprocess_tabular.py preprocess_text.py preprocess_images.py; do
  touch data_processing/$script
done

# Preprocess timeseries
cp data_processing/preprocess_tabular.py data_processing/preprocess_timeseries.py

# Model training scripts
mkdir -p training
touch training/train.py training/hyperparameter_tuning.py

# Evaluation scripts
mkdir -p evaluation
for script in evaluate.py benchmark_models.py; do
  touch evaluation/$script
done

# Model interpretability scripts
mkdir -p interpretability
for script in interpret_tabnet.py interpret_text.py interpret_image.py; do
  touch interpretability/$script
done

# Utils
mkdir -p utils
touch utils/data_loader.py

# App integration directories and files
mkdir -p app_integration/frontend
mkdir -p app_integration/backend

for file in App.js ScannerComponent.js ResultsDisplay.js; do
  touch app_integration/frontend/$file
done

for script in api.py inference.py; do
  touch app_integration/backend/$script
done

# Training and evaluation
mkdir -p models training evaluation

for script in tabnet_model.py lstm_timeseries.py bert_text.py cnn_image.py fusion_model.py; do
  touch models/$script
done

for script in train.py hyperparameter_tuning.py; do
  touch training/$script
done

for script in evaluate.py benchmark_models.py; do
  touch evaluation/$script
done

# Data directories
mkdir -p data/{auction_prices,reviews,weather,images}

# Results
mkdir -p evaluation/results
mkdir -p evaluation

# Additional files
touch requirements.txt

touch README.md

# Results and visualizations
mkdir -p results/visualizations

# Notifying setup completion
echo "Project structure setup completed."
