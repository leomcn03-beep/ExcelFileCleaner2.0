import FreeSimpleGUI as sg
import os
from cleaner import clean_data

def main():
    # Define custom theme
    sg.LOOK_AND_FEEL_TABLE['NBCRI_Pink'] = {
        'BACKGROUND': '#d71b7a',
        'TEXT': '#ffffff',
        'INPUT': '#ffffff',
        'TEXT_INPUT': '#000000',
        'SCROLL': '#ffffff',
        'BUTTON': ('#d71b7a', '#ffffff'),
        'PROGRESS': ('#ffffff', '#D0D0D0'),
        'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
    }
    sg.theme('NBCRI_Pink')

    layout = [
        [sg.Text("NBCRI CSV Cleaner", font=("Helvetica", 16))],
        [sg.Text("Select CSV File to Clean:", size=(20, 1)), sg.Input(key="-FILE-"), sg.FileBrowse(file_types=(("CSV Files", "*.csv"),))],
        [sg.Button("Clean File", size=(15, 1)), sg.Button("Exit", size=(10, 1))],
        [sg.HorizontalSeparator()],
        [sg.Text("Report:", size=(10, 1))],
        [sg.Multiline(size=(60, 10), key="-REPORT-", disabled=True, autoscroll=True)],
        [sg.Text("", key="-STATUS-", size=(60, 1))]
    ]

    window = sg.Window("NBCRI CSV Cleaner Data Tool", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break

        if event == "Clean File":
            file_path = values["-FILE-"]
            
            if not file_path:
                sg.popup_error("Please select a file first.")
                continue
            
            if not os.path.exists(file_path):
                sg.popup_error(f"File not found: {file_path}")
                continue

            window["-STATUS-"].update("Processing...")
            window.refresh()

            try:
                df_cleaned, report = clean_data(file_path)

                if df_cleaned is None:
                    window["-REPORT-"].update(f"Error occurred:\n{report}")
                    window["-STATUS-"].update("Failed.")
                else:
                    output_path = os.path.splitext(file_path)[0] + "_cleaned.csv"
                    df_cleaned.to_csv(output_path, index=False)
                    
                    report_text = (
                        f"--- Cleaning Completed ---\n"
                        f"File: {os.path.basename(file_path)}\n"
                        f"Saved to: {os.path.basename(output_path)}\n\n"
                        f"Initial Rows: {report['initial_rows']}\n"
                        f"Invalid Emails Removed: {report['invalid_emails_removed']}\n"
                        f"Duplicate Rows Removed: {report['duplicates_removed']}\n"
                        f"Final Rows: {report['final_rows']}"
                    )
                    
                    window["-REPORT-"].update(report_text)
                    window["-STATUS-"].update(f"Success! Saved to {output_path}")
                    sg.popup("Success", f"File cleaned and saved to:\n{output_path}")

            except Exception as e:
                window["-REPORT-"].update(f"Unexpected Error:\n{str(e)}")
                window["-STATUS-"].update("Error encountered.")

    window.close()

if __name__ == "__main__":
    main()
