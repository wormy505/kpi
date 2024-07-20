import pandas as pd
from supabase import create_client, Client
import json

# Load Supabase credentials and table names from JSON file
with open('supabase_data.json') as f:
    supabase_data = json.load(f)

SUPABASE_URL = supabase_data['SUPABASE_URL']
SUPABASE_KEY = supabase_data['SUPABASE_KEY']
KPIs_TABLE = supabase_data['KPIs']
KPI_USERS_TABLE = supabase_data['KPI_Users']
UUID_TRACKER_TABLE = supabase_data['UUID_Tracker']

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_user_credentials(role):
    response = supabase.table(KPI_USERS_TABLE).select("username").eq("role", role).execute()
    data = response.data

    if data:
        return list(set([user['username'] for user in data]))
    else:
        return []

def get_user_password(role, username):
    response = supabase.table(KPI_USERS_TABLE).select("password").eq("role", role).eq("username", username).execute()
    data = response.data

    if data:
        return data[0]['password']
    else:
        return None

def fetch_all_data():
    response = supabase.table(KPIs_TABLE).select("*").execute()
    data = response.data

    if data:
        df = pd.DataFrame(data)
        return df
    else:
        return pd.DataFrame()

def save_data_to_supabase(df):
    # Convert every cell to string and then replace NaN values with None
    df = df.astype(str).where(pd.notnull(df), None)

    for index, row in df.iterrows():
        record_id = row['id']  # Assuming 'id' is the primary key column
        updated_data = row.to_dict()
        response = supabase.table(KPIs_TABLE).update(updated_data).eq('id', record_id).execute()
        if 'message' in response:
            print(f"Error updating record id {record_id}: {response['message']}")

def add_uuid_to_tracker(uuid):
    supabase.table(UUID_TRACKER_TABLE).insert({"uuid": uuid}).execute()

def check_uuid_exists(uuid):
    response = supabase.table(UUID_TRACKER_TABLE).select("uuid").eq("uuid", uuid).execute()
    exists = len(response.data) > 0
    return exists
