import requests
import sys

# My previous mistake: missing the HTTP protocol
CAPCOIN_API_URL = r"https://rest.coincap.io/v3/assets/bitcoin?apiKey=2917913f41455eb20013777d94694883fd4274def096f3ea50fe97ef66a9671b"


def get_btc_demand() -> float:
    """Check the correctness of CLA and return user's bitcoin demand."""
    if len(sys.argv) < 2:
        sys.exit("Missing command-line argument")
    elif len(sys.argv) > 2:
        sys.exit("Excess command-line argument")

    try:
        btc_demand = float(sys.argv[1])
    except ValueError:
        sys.exit("Command-line argument is not a number")

    return btc_demand


def connect_api():
    """Conect to CoinCap API to get datas (Bitcoin Price Index)."""
    try:
        response = requests.get(CAPCOIN_API_URL)
    except requests.ConnectionError:
        sys.exit("A Connection error occurred.")
    except requests.HTTPError:
        sys.exit("An HTTP error occurred.")
    except requests.TooManyRedirects:
        sys.exit("requests.TooManyRedirects")
    except requests.ConnectTimeout:
        sys.exit("The request timed out while trying to connect to the remote server.")
    except requests.ReadTimeout:
        sys.exit("The server did not send any data in the allotted amount of time.")
    except requests.Timeout:
        sys.exit("The request timed out.")
    except requests.JSONDecodeError:
        sys.exit("Couldn’t decode the text into json.")
    # Overall exception
    except requests.RequestException:
        sys.exit(
            "There was an ambiguous exception that occurred while handling your request."
        )

    return response


def main():
    """Display the price of the number of bitcoins the user wants to buy."""
    btc_demand = get_btc_demand()

    # Contain: status_code, text, content, json(), headers
    response = connect_api()

    # Get datas in json format
    datas = response.json()

    try:
        btc_price = float(datas["data"].get("priceUsd", "404-not-found"))
    except ValueError:
        sys.exit("Not found tag: priceUsd")
    else:
        print(f"${btc_price*btc_demand:,.4f}")


if __name__ == "__main__":
    main()
