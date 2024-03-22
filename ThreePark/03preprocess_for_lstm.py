import pandas as pd
import numpy as np

def scale_data_new(industry_data, x_factors, y_factors = ['Close'], time_steps=5):
    scaled_data_by_industry = {}

    for industry, columns in industry_data.items():
        industry_factors = pd.DataFrame()

        for factor in x_factors:
            factor_columns = [col for col in columns if col.endswith(f"_{factor}")]
            
            if not factor_columns:
                print(f"No columns found for factor: {factor} in industry: {industry}")
                continue

            factor_data = industry_data[industry][factor_columns]

            # Calculate global min and max for the current factor across all companies
            global_min = factor_data.min().min()
            global_max = factor_data.max().max()

            # Normalize the data using min-max scaling
            scaled_factor_data = (factor_data - global_min) / (global_max - global_min)

            # Concatenate the scaled data to the industry_factors DataFrame
            industry_factors = pd.concat([industry_factors, scaled_factor_data], axis=1)

        num_samples = len(industry_factors) - time_steps + 1
        num_features = industry_factors.shape[1]
        X_reshaped = np.empty((num_samples, time_steps, num_features))

        y_indices = [industry_factors.columns.get_loc(col) for col in industry_factors.columns if any(col.endswith(f"_{factors}") for factors in y_factors)]

        y_reshaped = np.empty((num_samples, len(y_factors)))


        for i in range(num_samples):
            X_reshaped[i] = industry_factors.iloc[i:i+time_steps].values
            y_reshaped[i, :] = industry_factors.iloc[[i + time_steps], y_indices].values


        # Store the reshaped data for the industry
        scaled_data_by_industry[industry] = (X_reshaped, y_reshaped)

    return scaled_data_by_industry

scaled_data = scale_data_new(industry_data, ['Close', 'pe_ratio'], ['Close'])
scaled_data['Materials']