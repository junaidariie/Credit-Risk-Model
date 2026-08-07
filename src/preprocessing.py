import numpy as np
import pandas as pd


def _normalize_categorical_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    category_mapping = {
        'residence_type': {
            'owned': 'Owned',
            'mortgage': 'Mortgage',
            'rented': 'Rented',
        },
        'loan_purpose': {
            'auto': 'Auto',
            'home': 'Home',
            'personal': 'Personal',
            'personaal': 'Personal',
            'education': 'Education',
        },
        'loan_type': {
            'secured': 'Secured',
            'unsecured': 'Unsecured',
        },
    }

    for column, mapping in category_mapping.items():
        if column in df.columns:
            def normalize_value(value):
                if pd.isna(value):
                    return value
                text = str(value).strip()
                if not text:
                    return value
                lowered = text.lower()
                if lowered in mapping:
                    return mapping[lowered]
                return text.title()

            df[column] = df[column].apply(normalize_value)

    return df


def clean_and_engineer(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = _normalize_categorical_values(df)

    if 'loan_purpose' in df.columns:
        df['loan_purpose'] = df['loan_purpose'].replace('Personaal', 'Personal')

    if 'residence_type' in df.columns:
        if df['residence_type'].isna().sum() > 0:
            mode_val = df['residence_type'].mode()[0]
            df['residence_type'] = df['residence_type'].fillna(mode_val)


    if 'processing_fee' in df.columns and 'loan_amount' in df.columns:
        df = df[(df['processing_fee'] / df['loan_amount']) < 0.03]

    if 'gst' in df.columns and 'loan_amount' in df.columns:
        df = df[(df['gst'] / df['loan_amount']) < 0.20]

    if 'net_disbursement' in df.columns and 'loan_amount' in df.columns:
        df = df[df['net_disbursement'] <= df['loan_amount']]

    if 'loan_amount' in df.columns and 'income' in df.columns:
        df['loan_to_income'] = round(df['loan_amount'] / df['income'], 2)
    else:
        df['loan_to_income'] = 0

    if 'total_loan_months' in df.columns and 'delinquent_months' in df.columns:
        df['delinquency_ratio'] = np.where(
            df['total_loan_months'] > 0,
            round((df['delinquent_months'] * 100) / df['total_loan_months'], 1),
            0
        )
    elif 'delinquency_ratio' not in df.columns:
        df['delinquency_ratio'] = 0

    if 'total_dpd' in df.columns and 'delinquent_months' in df.columns:
        df['avg_dpd_per_delinquency'] = np.where(
            df['delinquent_months'] > 0,
            round(df['total_dpd'] / df['delinquent_months'], 1),
            0
        )
    elif 'avg_dpd_per_delinquency' not in df.columns:
        df['avg_dpd_per_delinquency'] = 0

    drop_cols = [
        'cust_id', 'loan_id',
        'disbursal_date', 'installment_start_dt',
        'loan_amount', 'income',
        'total_loan_months', 'delinquent_months', 'total_dpd',
        'sanction_amount', 'processing_fee', 'gst', 'net_disbursement',
        'principal_outstanding'
    ]

    existing_drop_cols = [c for c in drop_cols if c in df.columns]
    df = df.drop(columns=existing_drop_cols)

    return df
