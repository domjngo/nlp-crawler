import functions

with open('cab/CAB_23_1_0_0003.txt', 'r') as text:
    data = text.read().replace('\n', ' ')

print(functions.summarize(data, 3, False, 300))
