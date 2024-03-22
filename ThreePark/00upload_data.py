import pandas as pd
import os

## getting file path from computer
def file_path(file_name):
    home_directory = os.path.expanduser('~')
    csv_file_path = os.path.join(home_directory, 'Downloads', file_name)
    return csv_file_path

## importing files
companies_file_path = file_path('companies.csv')
companies_df = pd.read_csv(companies_file_path)



## code to upload csv in Colab
"""from google.colab import files
def upload_and_load_csv(file_name):
    # Upload the file from your local machine to the Colab environment
    uploaded_files = files.upload()

    # Ensure the desired file was uploaded
    if file_name not in uploaded_files:
        raise ValueError(f"{file_name} not uploaded. Please make sure the file name is correct and try again.")

    cwd = os.getcwd()  # This should be '/content' in Google Colab
    csv_file_path = os.path.join(cwd, file_name)

    companies_df = pd.read_csv(csv_file_path)

    return companies_df

companies_df = upload_and_load_csv('companies.csv')"""