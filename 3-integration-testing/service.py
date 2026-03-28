import datastore

def process_and_store(key, raw_value):
    processed_value=""
    if key=="name":
        processed_value = raw_value.strip().upper()
    datastore.store_value(key, processed_value)
    return processed_value


def retrieve_processed(key):
    result=datastore.get_value(key)
    return result.lower() if result else None

def update_value(key, raw_value):
    datastore.store_value(key, raw_value)


def delete_value(key):
    return datastore.delete_value(key)


def list_all_keys():
    return datastore.list_keys()
