import functions

with open('cab/CAB_195_25_0_0050.txt', 'r') as text:
    data = text.read().replace('\n', ' ')

print(functions.summarize(data, 3, False, 300))
