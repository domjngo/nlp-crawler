import functions

with open('cab/CAB_23_1_0_0002.txt', 'r') as text:
    data = text.read().replace('\n', ' ')

print(functions.summarize(data, 3, 300))
