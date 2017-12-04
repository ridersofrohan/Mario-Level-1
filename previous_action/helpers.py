import subprocess
import os
from os import path
import pickle

def killFCEUX():
  subprocess.call(["killall", "-9", "fceux"])

# Function to write the data to the appropriate filename
def write_to_file(filename, data, overwrite=False):
  if overwrite:
    #try statement to remove previous file before writing new file
    try:
      os.remove(filename)
    except OSError:
      pass
  with open(filename, 'wb') as f:
    pickle.dump(data, f)
  f.close()

# Function to read in weights and create a dictionary and a action table
def read_in_data(filename):
  data = {}
  with open(filename, 'rb') as f:
    data = pickle.load(f)
  f.close()
  return data
