def convert(time):
    # The common steps for processing time in 24-hour and 12-hour formats
    if time[1] == ":":
        formatted_time = float(time[:1]) + float(time[2:4]) / 60
    else:
        formatted_time = float(time[:2]) + float(time[3:5]) / 60

    # The unique step when processing time in 12-hour format
    if time[-3] == "p":
        formatted_time += 12.0

    return formatted_time


def main():
    time = input("What time is it? ")
    time = convert(time)

    if 7 <= time <= 8:
        print("breakfast time")
    elif 12 <= time <= 13:
        print("lunch time")
    elif 18 <= time <= 19:
        print("dinner time")


if __name__ == "__main__":
    main()
