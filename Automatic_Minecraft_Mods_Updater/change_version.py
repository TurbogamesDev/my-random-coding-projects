# Import necessary libraries
import shutil, json

path_to_dotminecraft_folder = "insert_path_here"

dir = path_to_dotminecraft_folder + "\\modstorage"

# Define function to copy files
def copy_files(source, destination):
  try:
    shutil.copytree(source, destination)
    print(f"Files copied successfully from {source} to {destination}")
  except OSError as e:
    print(f"Error copying files: {e}")

# Get the minecraft version to be used
version = input("Enter the minecraft version to be used: ")

file = open(f"{dir}\\list_of_mods.json", "r")
file_json = json.loads(file.read())
file.close()
file_json['recently_used_version'] = version
file = open(f"{dir}\\list_of_mods.json", "w")
file.write(json.dumps(file_json, indent=4))
file.close()

# Define source and destination folder
destination_folder = path_to_dotminecraft_folder + "\\mods"
source_folder = path_to_dotminecraft_folder + "\\modstorage\\" + version

# Delete the files inside the 'mods' folder
try:
  shutil.rmtree(destination_folder)
  print(f"Folder '{destination_folder}' deleted successfully.")
except OSError as e:
  print(f"Error deleting folder: {e}")

# Copy the files of the given minecraft version to the 'mods' folder
copy_files(source_folder, destination_folder)

# Pause program execution so that the user can check for any errors
input("Program Executed.")