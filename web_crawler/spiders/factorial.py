
total_tags = 300
total_tags_factorial = total_tags

combinations = 20
combinations_factorial = combinations

final_part = total_tags - combinations
final_part_factorial = final_part

for i in range(1, total_tags - 1):
    total_tags_factorial = total_tags_factorial * (total_tags - 1)
    total_tags = total_tags - 1

print("Tags factorial:", total_tags_factorial)


for x in range(1, combinations - 1):
    combinations_factorial = combinations_factorial * (combinations - 1)
    combinations = combinations - 1

print("Combinations factorial:", combinations_factorial)

print("Final part:", final_part)
for y in range(1, final_part - 1):
    final_part_factorial = final_part_factorial * (final_part - 1)
    final_part = final_part - 1
print("Final part factorial:", final_part_factorial)

result = total_tags_factorial / (combinations_factorial * final_part_factorial)
print(result)
