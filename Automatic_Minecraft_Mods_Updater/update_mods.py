import requests, os, json, shutil, time, asyncio, aiohttp, datetime, tqdm, threading

start_time = time.time()
datetime_start = datetime.datetime.now()

# dir = os.path.realpath(os.path.dirname(__file__))
path_to_dotminecraft_folder = "directory_path_here_(using \\ and not a single backslash)"

dir = path_to_dotminecraft_folder + "\\modstorage"
print(dir)

contents = []

mods = []
version_list = []
latest_used_version = ""

with open(dir + "\\list_of_mods.json", "rt") as file:
    file_json = json.loads(file.read())
    mods = (file_json)['modlist']
    version_list = (file_json)['all_versions']
    latest_used_version = (file_json)['recently_used_version']

log_output = f"Log of auto mod updater on {datetime_start.strftime("%Y-%m-%d at %H:%M:%S")}:\n"

def downJar(url, path, filename):
    # Note this is windows only
    os.chdir(path)

    # print(f"Downloading {filename}.....")

    remote_url = url
    local_file_name = filename

    data = requests.get(remote_url)
    
    # Save file data to local copy
    with open(f"{path}\\{local_file_name}", 'wb') as file:
        file.write(data.content)
        # print("Download complete")

def downloadfromModrinth(version_file_url, directory, filename):

    fileurl = version_file_url

    curn_dir = os.getcwd()
    print(curn_dir)

    downJar(fileurl, directory, filename=filename)
    # shutil.move(filename, directory)

def downloadMod(version_file_url, directory, file_name):
    downloadfromModrinth(version_file_url, directory, file_name)
    print(f"mod {file_name} downloaded")

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def retrieve_mod_versions(params):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(fetch(session, f"https://api.modrinth.com/v2/project/{mod}/version?loaders={params['loaders']}&game_versions={params['game_versions']}")) for mod in mods]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            contents.append(response)

def main(params, directory, ver, log_output):
    # urls = []
    files = os.listdir(directory)
    
    print("Checking for updates to the mods...")
    
    loop = asyncio.new_event_loop()
    loop.run_until_complete(retrieve_mod_versions(params))

    print("Updating out-of-date mods...")
    
    mods_to_update = []
    
    for c in contents:
        if not c:
            continue
        
        # update_to_version_id = ""
        update_to_version_file_name = ""
        update_to_version_file_url = ""
        current_version_file_name = ""
        list_of_file_names = []
    
        for entry in c:
            # if True: # Uncomment this to install the oldest compatible version of each mod
            if (not update_to_version_file_name) and (entry['version_type'] == 'release'):
                update_to_version_file_name = entry['files'][0]['filename']
                # update_to_version_id = entry['id']
                update_to_version_file_url = entry['files'][0]['url']
            list_of_file_names.append(entry['files'][0]['filename'])
        
        if not update_to_version_file_name:
            for entry in c:
                if (not update_to_version_file_name) and ((entry['version_type'] == 'release') or (entry['version_type'] == 'beta')):
                    update_to_version_file_name = entry['files'][0]['filename']
                    # update_to_version_id = entry['id']
                    update_to_version_file_url = entry['files'][0]['url']
        
        for f in files:
            if f in list_of_file_names:
                current_version_file_name = f
            else:
                pass
            
        if update_to_version_file_name == current_version_file_name:
            pass
        else:
            mods_to_update.append((update_to_version_file_url, directory, update_to_version_file_name, current_version_file_name))

    if mods_to_update:
        log_output = log_output + f"\nMods updated for minecraft version {ver}:\n"
    else:
        log_output = log_output + f"\nAll mods of minecraft version {ver} are already up-to-date\n"

    for m in mods_to_update:
        downloadMod(m[0], m[1], m[2])
        if m[3]:
            os.remove(f"{directory}\\{m[3]}")
            log_output = log_output + f"Mod \'{m[3]}\' updated to \'{m[2]}\'\n"
        else:
            log_output = log_output + f"New mod \'{m[2]}\' added\n"
    return log_output

def copy_files(source, destination):
  try:
    shutil.copytree(source, destination)
    print(f"Files copied successfully from {source} to {destination}")
  except OSError as e:
    print(f"Error copying files: {e}")

parameters = {
    'loaders': '[\"fabric\"]',
    'game_versions': '[\"1.20.6\"]'
}

for v in version_list:
    print(f"Updating {v}")
    contents = []
    parameters['game_versions'] = f"[\"{v}\"]"
    log_output = main(parameters, f"{dir}\\{v}", v, log_output)

# Define source and destination folder
destination_folder = path_to_dotminecraft_folder + "\\mods"
source_folder = path_to_dotminecraft_folder + "\\modstorage\\" + latest_used_version

# Delete the files inside the 'mods' folder
try:
  shutil.rmtree(destination_folder)
  print(f"Folder '{destination_folder}' deleted successfully.")
except OSError as e:
  print(f"Error deleting folder: {e}")

# Copy the files of the given minecraft version to the 'mods' folder
copy_files(source_folder, destination_folder)

current_time = time.time()
print(f"--- {round(current_time - start_time, 2)}s ---")

log_output += f"\nTook {str(round(current_time - start_time, 2))}s to complete"

with open(f"{dir}\\auto-update-logs\\log_file_{datetime_start.strftime("%Y-%m-%d_at_%H-%M-%S")}.txt", "w") as file:
    file.write(log_output)

