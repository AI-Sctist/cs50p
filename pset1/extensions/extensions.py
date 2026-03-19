def main():
    name = input("File name: ").lower().strip()

    index = name.rfind(".")
    if index == -1:
        print("application/octet-stream")
        return
    else:
        extension = name[index:]

    match extension:
        case ".gif":
            print("image/gif")
        case ".jpg" | ".jpeg":
            print("image/jpeg")
        case ".png":
            print("image/png")
        case ".pdf":
            print("application/pdf")
        case ".txt":
            print("text/plain")
        case ".zip":
            print("application/zip")
        case _:
            print("application/octet-stream")


if __name__ == "__main__":
    main()
