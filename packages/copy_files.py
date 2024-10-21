import os
import shutil

def copy_files_to_subdirectory(filenames, subdirectory_name):
  """Copies a list of files to a new subdirectory.

  Args:
    filenames: A list of filenames to copy.
    subdirectory_name: The name of the subdirectory to create and copy files to.
  """

  # Create the subdirectory if it doesn't exist
  if not os.path.exists(subdirectory_name):
    os.makedirs(subdirectory_name)

  # Copy each file to the subdirectory
  for filename in filenames:
    source_path = os.path.join(".", filename)  # Assuming files are in the current directory
    destination_path = os.path.join(subdirectory_name, filename)
    shutil.copy2(source_path, destination_path)  # copy2 preserves metadata

# Example usage:
filenames_to_copy = ["file1.txt", "image.jpg", "document.pdf"]
new_subdirectory = "my_files"

copy_files_to_subdirectory(filenames_to_copy, new_subdirectory)
