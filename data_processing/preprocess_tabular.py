import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib


def preprocess_tabular_data(input_csv, output_path):
    # Load data
    data = pd.read_csv(input_csv_path)

    # Define categorical and numeric columns
    categorical_features = ['region', 'vineyard', 'producer', 'grape_variety']
    numeric_features = ['critic_score',
                        'production_volume', 'average_vine_age']

    # Pipeline for numeric features
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])

    # Pipeline for categorical features
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # Combine transformers into a ColumnTransformer
    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

    # Apply transformations
    processed_data = preprocessor.fit_transform(data)

    # Save processed data
    processed_df = pd.DataFrame(processed_data.toarray())
    processed_df.to_csv('processed_tabular_data.csv', index=False)

    # Save preprocessing pipeline
    joblib.dump(preprocessor, 'tabular_preprocessor.pkl')

    print("Tabular data preprocessing complete and saved.")
