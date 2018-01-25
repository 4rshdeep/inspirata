wr = open("encouraging_cleaned.txt", 'w')

with open("encouraging.txt", 'r') as f:
	for line in f:
		if(len(line) > 70):
			continue

		wr.write(line)
