input_file_name = "data.csv"
output_file_name = "sorted_data.csv"
column = 5

def sort_csv(infile_name, outfile_name, field):
	with open(infile_name, "r") as infile:
		lines = sorted(filter(lambda line: line[0] != '#', infile.readlines()), \
						key = lambda line: line.split(',')[field])
		with open(outfile_name, "w") as outfile:
			for line in lines:
				outfile.write(line)


if __name__ == "__main__":
	sort_csv(input_file_name, output_file_name, column)
