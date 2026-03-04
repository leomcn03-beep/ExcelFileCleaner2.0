import pandas as pd
import re

def clean_data(file_path):
    """
    Cleans the NBCRI contact CSV file.
    """
    try:
        # Load CSV
        try:
             df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
             df = pd.read_csv(file_path, encoding='latin-1')

        # 1. Trim whitespace
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        
        initial_count = len(df)
        
        # 2. Validate Emails
        # Simple regex for email validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Ensure 'Email Address' column exists (case-insensitive check)
        email_col = None
        for col in df.columns:
            if col.strip().lower() == 'email address':
                email_col = col
                break
        
        if not email_col:
            return None, "Error: 'Email Address' column not found."

        # Filter invalid emails
        valid_emails = df[email_col].astype(str).apply(lambda x: bool(re.match(email_regex, x)))
        invalid_email_count = (~valid_emails).sum()
        df_valid = df[valid_emails]
        
        # 3. Remove Duplicates
        # Drop duplicates based on email, keeping the first occurrence
        df_cleaned = df_valid.drop_duplicates(subset=[email_col])
        duplicate_count = len(df_valid) - len(df_cleaned)
        
        removed_total = invalid_email_count + duplicate_count
        final_count = len(df_cleaned)

        report = {
            "initial_rows": initial_count,
            "invalid_emails_removed": invalid_email_count,
            "duplicates_removed": duplicate_count,
            "final_rows": final_count
        }

        return df_cleaned, report

    except Exception as e:
        return None, str(e)

if __name__ == "__main__":
    pass
