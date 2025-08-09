def convert(text):
    """Convert emoticon to corresponding emoji."""
    text = text.replace(":)", "🙂")
    text = text.replace(":(", "🙁")

    print(text)


if __name__ == "__main__":
    # Get user message
    text = input()

    # Convert any emoticon to corresponding emoji
    convert(text)
