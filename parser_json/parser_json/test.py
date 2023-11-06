# Your JSON string
json_string = ["	tab	character	in	string	"]

# Split the JSON string into individual items
items = json_string.split(",")

# Check for escaped tabs in each item
for item in items:
    if "\\t" in item:
        print(f"Escaped tab detected in: {item}")
