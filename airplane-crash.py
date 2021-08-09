import random
import time
import csv
import requests
from googlesearch import search


def extract_between(text, match, last):
    found = text.find(match)
    if found != -1:
        end = text.find(last, len(match) + found + 1)
        return text[found + len(match): end]
    return None


def extract_latitude_longitude(text):
    found = text.find(r'"latitude"')
    if found != -1:
        end = text.find(r'"longitude"', found)
        if end != -1:
            last = text.find("},", end)
            str_extract = text[found: last]
            latitude = extract_between(str_extract, r'"latitude":"', r'",')
            longitude = extract_between(str_extract, r'"longitude":"', r'"')
            return (latitude, longitude)
    return None, None


def extract_lat_lon(location):
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)
    result = search("latitude and longitude " +
                    location, num_results=2)
    for url in result:
        try:
            r = requests.get(url)
            (lat, lon) = extract_latitude_longitude(r.text)
            if lat and lon:
                return (lat, lon)
            else:
                break
        except:
            print("failed")
            break
    return "", ""


def write_output(output):
    with open('airplane-crash-result.csv', 'w') as file:
        for line in output:
            file.write(line + "\n")


def normalize_str(row):
    csv_str = []
    for item in row:
        csv_str.append(item.replace(", ", " ").replace("\n", " "))

    return ",".join(csv_str)


def enrich_lat_lon_airplane_crash():
    with open('airplane-crash.csv', 'r') as file:
        output = []
        rows = csv.reader(file)
        output.append(str(next(rows, None)))
        count = 1
        for row in rows:
            location = row[7]
            (lat, lon) = extract_lat_lon(location)
            row[8] = lat
            row[9] = lon
            str_row = normalize_str(row)
            print(f"{count}: {str_row}")
            output.append(str_row)
            count = count + 1

        write_output(output)


enrich_lat_lon_airplane_crash()
