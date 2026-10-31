import csv


def read_csv(path):
    required_heads =   {"timestamp","source_ip","username","outcome"} 
    with open(path,"r",encoding="utf-8",newline="") as handle:
        reader = csv.DictReader(handle)
        csv_header = reader.fieldnames
        if csv_header is None:
            raise ValueError("The header of the csv are empty")
        else:
            csv_header_set = set(csv_header)
            missing = required_heads - csv_header_set
            if len(missing)>0:
                raise ValueError(f"Missing header(s) {missing}")
        return list(reader)

def check_username(input):
    username = input.get("username")
    if username is not None and username.strip() != "":
        return True
    else:
        return False



try:
    list_of_data = read_csv("examples/auth_valid.csv")
    for data in list_of_data:
        if check_username(data):
            print("Username is good")
        else:
            
            print("Username is bad")
    
except FileNotFoundError as fileError:
    print(f"File Not found Error :{fileError}")
except ValueError as ve:
    print(f"Value Error : {ve}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    print(f"Error type: {type(e).__name__}")
    
