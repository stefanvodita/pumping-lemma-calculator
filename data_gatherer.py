import main


def count_chars(lang_desc):
	lang = lang_desc.split('|')[0]
	chars = {}
	for char in lang:
		if char in main.alphabet:
			chars[char] = True
	return len(chars)


def count_vars(lang_desc):
	lang = lang_desc.split('|')[0]
	varbs = {}
	for var in lang:
		if var in main.variables:
			varbs[var] = True
	return len(varbs)


def count_conditions(lang_desc):
	if lang_desc.split('|')[1][0] == '.':
		return 0
	conds = (lang_desc.split('|')[1]).strip().split(',')
	return len(conds)


def write_data(outputs, lang_desc, data):
	char_no = count_chars(lang_desc)
	var_no = count_vars(lang_desc)
	cond_no = count_conditions(lang_desc)
	line = ','.join([lang_desc.strip(),													\
					str(char_no),														\
					str(var_no),														\
					str(cond_no),														\
					str(data["k_stop"])		if not data["k_stop"] is None else "",		\
					str(data["no_w_stop"])	if not data["no_w_stop"] is None else "",	\
					str(data["res"])		if not data["res"] is None else "",			\
					""]) + "\n"
	outputs.write(line)


def gather(in_file, outputs):
	with open(in_file, "r") as inputs:
		for lang_desc in inputs:
			if lang_desc[0] == '#':
				outputs.write("#\n")
				continue
			write_data(outputs, lang_desc, main.main(lang_desc))


if __name__ == "__main__":
	gather("inputs", open("data.csv", "a"))
