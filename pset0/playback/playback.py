# Prompt the user for input
text = input()

# Print the same but replace each space with three dots
for character in text:
    print("..." if character == " " else character, end="")

# Make a newline
print("\n", end="")
