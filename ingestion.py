import csv
import re
import datetime


def read_csv(path):
    required_heads =   {"timestamp","source_ip","username","outcome"}
    good_data =[]
    bad_data = []
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

        for line ,data in enumerate(reader,start=2):
            if not check_username(data):
                bad_data.append({"line_number" : line,   "reason": "Username is blank or missing"})
            elif not check_timestamp(data):
                bad_data.append({"line_number" : line,   "reason": "Timestamp is blank or missing or errored"})
            else:
                good_data.append(data)



        return good_data,bad_data


def check_username(input):
    username = input.get("username")
    if username is not None and username.strip() != "":
        return True
    else:
        return False

def check_timestamp(input):
    timestamp = input.get("timestamp")
    if timestamp is not None and timestamp.strip() != "":
        match = re.fullmatch("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z",timestamp)
        if match is not None:
            try:
                datetime.datetime.strptime(timestamp,"%Y-%m-%dT%H:%M:%SZ")
                return True
            except ValueError:
                return False
        else:
            return False
    else:
        return False


if __name__ == "__main__":
    try:

        paths = ["auth_test_valid_long.csv","auth_test_usernames_long.csv","auth_test_header_only.csv","auth_test_empty.csv","auth_test_missing_outcome_long.csv"]
        for path in paths:
            print(f"Doing {path}...................................................................................................................")
            try:
                right_data,wrong_data = read_csv(f"examples/{path}")
                print(f"Good data {right_data}")
                print("..................................................................................................................................")
                print(f"Wrong data {wrong_data}")
            except FileNotFoundError as fileError:
                print(f"File Not found Error :{fileError}")
            except ValueError as ve:
                print(f"Value Error : {ve}")


            print("------------------------------------------------------------------------------------------------------------------------------------")

    except FileNotFoundError as fileError:
        print(f"File Not found Error :{fileError}")
    except ValueError as ve:
        print(f"Value Error : {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print(f"Error type: {type(e).__name__}")