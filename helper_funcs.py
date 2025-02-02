### HELPER FUNCTIONS ###

# Adds my composite url strings to the json_data. 
def add_urls(item, key, val):
    item[key] = val
    # Returns 'None' by default, so return the updated dict myself!
    return item

# Replaces any forbidden characters for the benefit of the filename
def cleanup_name(val_choice):
    # These chars are acceptable when naming files
    accepted_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
    new_str = ""
    for i in val_choice:
        if i not in accepted_chars:
            new_str += "_"
        else: new_str += i
    return new_str # Replaces any forbidden characters for the benefit of the filename