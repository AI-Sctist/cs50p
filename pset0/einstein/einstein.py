LIGHT_SPEED = 300000000

# Prompts the user for mass
mass = int(input("m: "))

# E = mc^2 with E is energy, m is mass, c is the speed of light
print(mass * LIGHT_SPEED**2)
