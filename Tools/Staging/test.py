import os
from dotenv import load_dotenv

# Load environment variables from .env in the 'prereqs' folder
dotenv_path = os.path.join("prereqs", ".env")
load_dotenv(dotenv_path)

# Retrieve environment variables
SubscriptionID = os.getenv('SUBSCRIPTION_ID')
ResourceGroup = os.getenv('RESOURCE_GROUP')
Workspace = os.getenv('WORKSPACE')

print("SubscriptionID:", SubscriptionID)
print("ResourceGroup:", ResourceGroup)
print("Workspace:", Workspace)
