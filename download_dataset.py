import kagglehub
import shutil
import os

# Download the dataset
path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")

print("Downloaded dataset to:")
print(path)

# Find the CSV file
csv_path = os.path.join(path, "creditcard.csv")

# Destination inside our project
destination = "data/raw/creditcard.csv"

# Create destination folder if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

# Copy dataset
shutil.copy2(csv_path, destination)

print("Dataset copied successfully!")
print("Saved at:", destination)