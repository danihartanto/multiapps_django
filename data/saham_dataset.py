import kagglehub

# Download latest version
path = kagglehub.dataset_download("muamkh/ihsgstockdata")

print("Path to dataset files:", path)