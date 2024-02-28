import os
import subprocess

# Set the maximum allowed size in MB
MAX_COMMIT_SIZE = 200

def get_files_and_sizes(directory):
    files_and_sizes = []
    for root, _, files in os.walk(directory):
        for f in files:
            filepath = os.path.join(root, f)
            # Prefix the file path with '\\?\' to handle long paths on Windows
            long_filepath = '\\\\?\\' + os.path.abspath(filepath)
            size = os.path.getsize(long_filepath)
            files_and_sizes.append((long_filepath, size))
    return files_and_sizes

def create_batches(files_and_sizes):
    batches = []
    current_batch = []
    current_size = 0

    for file, size in files_and_sizes:
        # Convert size to MB
        size_mb = size / (1024 * 1024)
        if current_size + size_mb > MAX_COMMIT_SIZE:
            batches.append(current_batch)
            current_batch = []
            current_size = 0
        current_batch.append(file)
        current_size += size_mb

    # Add the last batch if it has files
    if current_batch:
        batches.append(current_batch)
    
    return batches

def commit_batches(batches):
    for i, batch in enumerate(batches, start=1):
        for file in batch:
            subprocess.run(['git', 'add', file])
        commit_message = f"Commit {i} with batched files"
        subprocess.run(['git', 'commit', '-m', commit_message])
        print(f"Batch {i} committed.")

# Usage
directory = "W:/Magnum Opus/album/h4"
files_and_sizes = get_files_and_sizes(directory)
batches = create_batches(files_and_sizes)
commit_batches(batches)