
backup_filename = "15:40" # TODO: replace with proper setting


import lz4.frame
import tarfile
import yaml
from pathlib import Path
import shutil
import os

# load paths settings

backups_settings_file = "settings_paths.yml"
backups_path = ""
to_backup_path = ""

with open(backups_settings_file, 'r') as f:
   data = yaml.load(f, Loader=yaml.FullLoader)

   backups_path = data['backups_path']
   to_backup_path = data['to_backup_path']


def loadBackup(backup_filename):
   backup_filepath = os.path.join(backups_path, backup_filename)

   # delete the to backup folder
   shutil.rmtree(to_backup_path)

   # load the backup
   with open(backup_filepath, 'rb') as file: # get the file
      with lz4.frame.open(file, mode='rb') as lz4_file: # get the lz4 frame file
         with tarfile.open(fileobj=lz4_file, mode='r|') as tar: # open the lz4 frame file with streaming mode
            tar.extractall(path=Path(to_backup_path).parent.absolute()) # extract in the parent of the to backup folder


# choose the first backup that matches the filename
matching = [fp for fp in os.listdir(backups_path) if os.path.isfile(os.path.join(backups_path, fp)) and backup_filename in fp]

if matching and len(matching) > 0:
   backup_filename = matching[0]

   loadBackup(backup_filename)