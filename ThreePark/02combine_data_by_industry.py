import pandas as pd

def data_by_industry(by_industry, company_dataframes, factors):
    industry_data = {}
    for industry, companies in by_industry.items():
        combined_df = pd.DataFrame()
        for company in companies:
            if company not in company_dataframes.keys():
                continue
                
            df = company_dataframes[company]
            df.index = pd.to_datetime(df.index)

            # Rename columns to include the company name for uniqueness
            df_renamed = df.rename(columns={factor: f'{company}_{factor}' for factor in factors})

            if combined_df.empty:
                combined_df = df_renamed
            else:
                combined_df = pd.concat([combined_df, df_renamed], axis=1)

        industry_data[industry] = combined_df

    return industry_data

industry_data = data_by_industry(by_industry, company_dataframes, ['Close', 'pe_ratio'])