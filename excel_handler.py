import os
import time
import uuid
import pandas as pd
import xlwings as xw
from db_handler import fetch_all_data, save_data_to_supabase, add_uuid_to_tracker, check_uuid_exists
from PySide6.QtWidgets import QMessageBox

def start_excel_with_data(role, username):
    try:
        # Fetch data from Supabase
        data = fetch_all_data()

        # Filter data based on role and username
        if role == "Department":
            filtered_data = data[data['dept'] == username]
        elif role == "Appraiser":
            filtered_data = data[data['appraiser'] == username]

        # Generate a unique UUID for the temporary Excel file
        unique_uuid = str(uuid.uuid4())
        while check_uuid_exists(unique_uuid):
            unique_uuid = str(uuid.uuid4())

        temp_file_path = f"{unique_uuid}.xlsx"
        add_uuid_to_tracker(unique_uuid)

        # Convert all data to string and write to the Excel file
        filtered_data = filtered_data.astype(str)
        filtered_data.to_excel(temp_file_path, index=False)

        # Start Excel with xlwings and open the temporary file
        app = xw.App(visible=True, add_book=False)
        wb = app.books.open(temp_file_path)

        # Monitor the workbook and wait for it to close
        while True:
            try:
                open_books = [os.path.basename(book.fullname) for book in app.books]
                if os.path.basename(temp_file_path) not in open_books:
                    break
            except Exception as e:
                print(f"Error monitoring the file: {e}")
            time.sleep(1)

        # Save the updated data back to Supabase
        updated_data = pd.read_excel(temp_file_path)
        updated_data = updated_data.astype(str).where(pd.notnull(updated_data), None)

        save_data_to_supabase(updated_data)

        # Close the Excel application
        app.quit()

        # Delete the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        QMessageBox.information(None, "Success", "Data updated and saved successfully.")
    except Exception as e:
        QMessageBox.critical(None, "Error", f"An error occurred: {e}")
