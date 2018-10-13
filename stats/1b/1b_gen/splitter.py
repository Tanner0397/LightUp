file = open("log.txt", "r")

runs = 30
inital_line = 22
block_size = 991

for i in range(0, inital_line):
	file.readline()

for i in range(runs):
	buffer = ""
	for j in range(0, block_size):
		buffer += file.readline()
	file.readline()
	file.readline()#Move head
	new_file = open("run" + str(i+1) + ".txt", "w")
	new_file.write(buffer)
	new_file.close()