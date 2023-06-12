import csv
import re


def blockify(data):
    block_list = []
    # Remove empty lines and separator lines
    lines = [line.strip() for line in log_data if line.strip() != ""]
    for i in range(0, len(lines)):
        if lines[i].startswith("-"):
            block = []
            b = i + 1
            if b == len(lines):
                break

            while not lines[b].startswith("-"):
                block.append(lines[b])
                b += 1
            block_list.append(block)
            i = b
    return block_list

STATES = ["I", "F", "D", "S"]
def get_state(state):
    match state:
        case "I":
            return "init"
        case "F":
            return "Floating"
        case "D":
            return "Danger"
        case "S":
            return "Standby"
        case _:
            return ""

def isTime(str):
    return re.match(r"^(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)(?:\.(\d+))?$", str)

# Create a list to store the parsed data
def parse_data(blocks):
    parsed_data = []
    for block in blocks:
        state = ""
        time = ""
        altitude = ""
        hdop = ""
        latitude = ""
        longitude = ""
        speed = ""
        rssi = ""
        snr = ""
        for i in range(len(block)):
            cell = block[i]
            if cell in STATES:
                state = get_state(cell)
            if isTime(cell):
                time = cell
            elif cell.startswith("alt:"):
                altitude = cell.split(":")[1]
            elif cell.startswith("hdop:"):
                hdop = cell.split(":")[1]
            elif cell.startswith("lat:"):
                latitude = cell.split(":")[1]
            elif cell.startswith("lon:"):
                longitude = cell.split(":")[1]
            elif cell.startswith("speed:"):
                speed = cell.split(":")[1]
            elif cell.startswith("rssi:"):
                rssi = cell.split(":")[1]
            elif cell.startswith("snr:"):
                snr = cell.split(":")[1]

        parsed_data.append([state, time, altitude, hdop, latitude, longitude, speed, rssi, snr])
    return parsed_data


# Write the parsed data to a CSV file

def make_csv(parsed_data):
    with open("data.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["State", "Time", "Altitude", "HDOP", "Latitude", "Longitude", "Speed", "RSSI", "SNR"])
        writer.writerows(parsed_data)


if __name__ == '__main__':
    log_data = open("GS.log").readlines()

    lines = [line for line in log_data if not (line.__contains__("Lora") or line.__contains__("Serial"))]

    # Split the data by line breaks
    # lines = data.split("\n")

    blocked = blockify(lines)
    # for block in blocked:
    #     print(block)
    #     print()

    parsed = parse_data(blocked)
    # for block in parsed:
    #     for cell in block:
    #         if cell == "":
    #             print(block)
    #             print()
    #             continue
    make_csv(parsed)
    #
    print("Data successfully converted to CSV.")
