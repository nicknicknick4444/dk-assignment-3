# IMPORT MODULES
import requests, json, csv, datetime, sys, json
import pandas as pd

url_str = "https://d2hmvvndovjpc2.cloudfront.net/efe"
accepted_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"

### HELPER FUNCTIONS ###
def add_to_dict(item, key, val):
    item[key] = val
    # Returns 'None' by default, so return the updated dict myself!
    return item

# Replaces any forbidden characters for the benefit of the filename
def cleanup_name(val_choice):
    new_str = ""
    for i in val_choice:
        if i not in accepted_chars:
            new_str += "_"
        else: new_str += i
    return new_str# Replaces any forbidden characters for the benefit of the filename

### SUPPORTING FUNCTIONS ###

# Fetches the Excel file, performs some data-type rationalisations and \
# returns the raw data in JSON format
def get_data():
    opened_file = pd.read_excel("Input/Course Books - Audios-2.xlsx", sheet_name="Sheet1")
    json_data = json.loads(opened_file.to_json(orient = "records"))
    # Stripping out those 4 empty cols at the end with a dictionary comprehension
    json_data = [{n:i[n] for n in i if "Unnamed:" not in n} for i in json_data]
    # Adding the url col, so that it's available for filtering!     
    json_data = [add_to_dict(i, "url", url_str + i["filepath"] + i["filename"]) for i in json_data]
    # Convert any None and int OR float types (Mac and Windows interpreted them differently) /
    # to stings for the purposes of analysis
    json_data = [{n:int(round(i[n], 0)) if isinstance(i[n], (float, int)) else i[n] for n in i} for i in json_data]
    json_data = [{n:str(i[n]) if isinstance(i[n], int) else i[n] for n in i} for i in json_data]
    json_data = [{n:"None" if i[n] is None else i[n] for n in i} for i in json_data]
    # Uncomment the below to check that the data types have been successfully converted to searchable strings
    # json_data = [{n:print("TYPE: ", type(i[n])) for n in i} for i in json_data]
    return json_data

# Grabs all the keys from the JSON data
def list_all_cols():
    cols = [i + "\n" for i in json_data[0]]
    return cols

# Display list items vertically as a string
def list_options(a_list, opt_line_break):
    str_output = ""
    for i in a_list:
# Optional line break becaue thecol names already \
# had them them, but values didn't
        str_output += str(i) + opt_line_break
    return str_output

def get_options(chosen_col):
    val_options = set()
    for i in json_data:
        val_options.add(i[f"{chosen_col}"])
    val_options_list = sorted(list(val_options))
    return val_options_list

### MAIN FUNCTIONS ###

# LAUNCH FUNCTION; INVITES TE USER TO CHOOSE A COLUMN
def launch_and_choose_col():
# Get string list of columns
    list_cols = list_options(cols, "")
    print("COLUMNS", file = sys.stderr)
    col_choice = input(f"{list_cols}\nPlease choose the column you wish to filter by.\n(Case-sensitive; copy & paste recommended): ")
    if col_choice in list_cols:
# If successful, move on to values section
        val_options = get_options(col_choice)
        choose_value(col_choice, val_options)
    else:
# Otherwise, if the column is not recognised, say so and restart fucntion with recursion
        print("\nColumn not in list! Please try again.\n", file = sys.stderr)
        return launch_and_choose_col()

# Invites the user to choose a value
def choose_value(col_choice, val_options):
#     Get the vertical values-list string
    options = list_options(val_options, "\n")
#     Formatted input messager for user
    print("FILTER VALUES:", file = sys.stderr)
    val_choice = input(f"{options}\nPlease enter your chosen filter value\n(Case-sensitive; copy & paste recommended): ")
#     Check if the user's input is one of the available values
    if val_choice in options:
#         If so, format the filename and move on to output function
        filename = cleanup_name(val_choice) + "__AND__" + col_choice
        make_output(col_choice, val_choice, filename)
#         Invite the user to have another go! Accepts 'y' or 'yes', in any case; \
#         anything else is taken as a 'no'
        again = input("\nAll done! Would you like to start again? (y/n) ")
        if again.lower() == "y" or again.lower() == "yes":
#             If yes, restart program from the very beginning
            return launch_and_choose_col()
        else:
#             Otherwise, thank you and goodnight
            print("\nExiting program...", file = sys.stderr)
            exit()
#     Otherwise, tell them so and repeat the prompt
    else:
        print("\nValue not in list! Please try again.", file = sys.stderr)
        return choose_value(col_choice, val_options)

# Takes all the input information and returns a filtered JSON array
def make_output(col_choice, val_choice, filename):
#     IMPORTANT: THIS IS THE LINE THAT DOES THE ACTUAL FILTERING, VIA A HANDY LIST COMPREHENSION!
    filtered_data = [i for i in json_data if i[f"{col_choice}"] == f"{val_choice}"]
    
#     Convert our "None" and "int" value strings back to their correct data-types for the JSON file
    filtered_data = [{n:int(i[n]) if i[n].isnumeric() else i[n] for n in i} for i in filtered_data]
    filtered_data = [{n:None if i[n] == "None" else i[n] for n in i} for i in filtered_data]
    
#     Deal with plural issue in row counting/ filename    
    extra_s = "S" if len(filtered_data) > 1 or len(filtered_data) == 0 else ""
    zero_message = "\nIs this what you expected? You maybe have used a subset of a larger existing value." if len(filtered_data) == 0 else ""
    filename += "_FILTER__" + str(len(filtered_data)) + f"_ROW{extra_s}.json"
    print(f"\n{len(filtered_data)} ROW{extra_s} FOUND!{zero_message}\n", file=sys.stderr)
    print(f"Writing '{filename}' to the Output folder.")
    
    # Write the JSON file
    with open (f"Output/{filename}", "w") as file:
        json.dump(filtered_data, file)


### RUN THE PROGRAM HERE ###
# Runs inside try/ except structure to catch errors
try:
#     Initialises the JSON data and 
    if __name__ == "__main__":
        json_data = get_data()
        cols = list_all_cols()
        launch_and_choose_col()
except Exception as e:
    print(f"\n-------AN ERROR HAS OCCURRED:-----\nERROR TYPE: {type(e).__name__}\nMESSAGE: {e}\n", \
          file = sys.stderr)
    exit()

### END OF PROGRAM ###