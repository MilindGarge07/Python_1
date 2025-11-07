from lorem_text import lorem

single = lorem.sentence()

len = len(single)

print(f"The length of the generated sentence is: {len}")

print(f"The generated sentence is: {single}")

print("--------------------------------------")

print(single[2:-10])