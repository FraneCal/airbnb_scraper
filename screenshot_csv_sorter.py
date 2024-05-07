# import os
# import shutil

# # Function to create directories if they don't exist
# def create_directory(directory):
#     if not os.path.exists(directory):
#         os.makedirs(directory)

# # Path to the folders containing screenshots and CSV files
# screenshots_folder = 'screenshots_barcelona'
# csv_folder = 'barcelona_splitted_csv'

# # Path to the folder to save sorted data
# sorted_data_folder = 'barcelona_sorted_data'

# # Create the sorted data folder if it doesn't exist
# create_directory(sorted_data_folder)

# # Get the list of files in the screenshots folder
# screenshots_files = os.listdir(screenshots_folder)

# # Iterate through each screenshot file
# for screenshot_file in screenshots_files:
#     if screenshot_file.endswith('.png'):
#         # Get the base name (without extension) of the screenshot file
#         base_name = os.path.splitext(screenshot_file)[0]

#         # Find the corresponding CSV file with the same base name
#         csv_file = f"{base_name.replace('_', ' ')}.csv"
#         if csv_file in os.listdir(csv_folder):
#             # Create a folder with the base name if it doesn't exist
#             folder_path = os.path.join(sorted_data_folder, base_name)
#             create_directory(folder_path)

#             # Copy the screenshot file and CSV file to the folder
#             shutil.copy(os.path.join(screenshots_folder, screenshot_file), os.path.join(folder_path, screenshot_file))
#             shutil.copy(os.path.join(csv_folder, csv_file), os.path.join(folder_path, csv_file))


import os
import shutil
from fuzzywuzzy import fuzz

# Function to create directories if they don't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to find the most similar file in a list
def find_similar_file(target_file, file_list):
    max_similarity = 0
    most_similar_file = None
    for file in file_list:
        similarity = fuzz.partial_ratio(target_file, file)
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_file = file
    return most_similar_file

# Path to the folders containing screenshots and CSV files
screenshots_folder = 'screenshots_barcelona'
csv_folder = 'barcelona_splitted_csv'

# Path to the folder to save sorted data
sorted_data_folder = 'barcelona_sorted_data'

# Create the sorted data folder if it doesn't exist
create_directory(sorted_data_folder)

# Get the list of files in the screenshots folder
screenshots_files = os.listdir(screenshots_folder)
csv_files = os.listdir(csv_folder)

# Iterate through each screenshot file
for screenshot_file in screenshots_files:
    if screenshot_file.endswith('.png'):
        # Get the base name (without extension) of the screenshot file
        base_name = os.path.splitext(screenshot_file)[0]

        # Find the most similar CSV file with the same base name
        csv_file = find_similar_file(base_name, csv_files)
        if csv_file:
            # Create a folder with the base name if it doesn't exist
            folder_path = os.path.join(sorted_data_folder, base_name)
            create_directory(folder_path)

            # Copy the screenshot file and CSV file to the folder
            shutil.copy(os.path.join(screenshots_folder, screenshot_file), os.path.join(folder_path, screenshot_file))
            shutil.copy(os.path.join(csv_folder, csv_file), os.path.join(folder_path, csv_file))
