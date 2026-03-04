import argparse
import os
from cleaner import clean_data

def main():
    parser = argparse.ArgumentParser(description="NBCRI CSV Cleaner CLI")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("--output", help="Path to save the cleaned CSV file", default="cleaned_contacts.csv")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' not found.")
        return

    print(f"Cleaning '{args.input_file}'...")
    df_cleaned, report = clean_data(args.input_file)
    
    if df_cleaned is None:
        print(f"Cleaning failed: {report}")
    else:
        print("\n--- Cleaning Report ---")
        print(f"Initial Rows: {report['initial_rows']}")
        print(f"Invalid Emails Removed: {report['invalid_emails_removed']}")
        print(f"Duplicate Rows Removed: {report['duplicates_removed']}")
        print(f"Final Rows: {report['final_rows']}")
        print("-----------------------")
        
        df_cleaned.to_csv(args.output, index=False)
        print(f"\nCleaned file saved to: {args.output}")

if __name__ == "__main__":
    main()
