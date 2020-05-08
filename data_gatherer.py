import main


input_file_name = "inputs"
output_file_name = "data.csv"
open_mode = "a"
tries = 20


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


def write_data(outputs, lang_desc, verdict, data):
	char_no = count_chars(lang_desc)
	var_no = count_vars(lang_desc)
	cond_no = count_conditions(lang_desc)
	line = ','.join(["\"" + lang_desc.strip() + "\"",									\
					str(char_no),														\
					str(var_no),														\
					str(cond_no),														\
					str(data["k_stop"])		if not data["k_stop"] is None else "",		\
					str(data["no_w_stop"])	if not data["no_w_stop"] is None else "",	\
					str(data["res"])		if not data["res"] is None else "",			\
					verdict.strip()]) + "\n"
	outputs.write(line)


def average(lang_desc, tries):
	avg = {"k_stop" : 0, "no_w_stop" : 0, "res" : 0}
	for _ in range(tries):
		data = main.main(lang_desc)
		# if data["res"]:  # no averaging for regular languages
		# 	return data
		avg = {key: avg[key] + (data[key] if data[key] else 0) for key in avg.keys()}
	return {key: value / tries for key, value in avg.items()}


def gather(in_file, outputs, tries):
	with open(in_file, "r") as inputs:
		for lang_desc in inputs:
			if lang_desc[0] == '#':
				outputs.write("#\n")
				continue
			[lang_desc, verdict] = lang_desc.split(' ')
			lang_desc.strip()
			verdict.strip()
			if tries > 1:
				write_data(outputs, lang_desc, verdict, average(lang_desc, tries))
			else:
				write_data(outputs, lang_desc, verdict, main.main(lang_desc))

if __name__ == "__main__":
	gather(input_file_name, open(output_file_name, open_mode), tries)
