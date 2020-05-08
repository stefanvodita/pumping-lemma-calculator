from random import randrange

import parser


conf = 2  # conf in {1, 2, 3}
alphabet = "abcdefghijklmnopqrstuvwxyz"		# all characters in the alphabet in a string
variables = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"	# all variables in a string
w_picks = 100		# we try 100 different, random words
k_picks = 10		# we try k in range(k_picks)
max_exponent = 25	# no point in picking a^100 when the language is a^n


def is_digit(character):
	"""
	Checks whether a CHARACTER is a digit. NOT for numbers.
	"""
	return character >= '0' and character <= '9'


def merge_powers(powers):
	"""
	There is no point in having w = [('a', 1), ('a', 1)],
	when we could have w = [('a', 2)].
	"""

	# delete powers with exponent 0
	non_redundant_powers = []
	for power in powers:
		if power[1] != 0:
			non_redundant_powers.append(power)
	powers = non_redundant_powers

	# merge
	merged_powers = []
	i = 0
	while i < len(powers):
		base = powers[i][0]
		power = powers[i][1]
		i += 1
		while i < len(powers) and base == powers[i][0]:
			power += powers[i][1]
			i += 1
		merged_powers.append((base, power))
	return merged_powers


def parse_element(element):
	"""
	Transform a language expressed as string, into a list of tuples.
	E.g: aa^nb ---> [('a', 1), ('a', 'n'), ('b', 1)]
	"""
	powers = []
	i = 0
	while i < len(element):
		if element[i] in alphabet:
			if i + 1 == len(element) or element[i + 1] != '^':
				powers.append((element[i], 1))
				i += 1
			else:
				if element[i + 2] == '(':
					print("Bad if condition")
					pass
				else:
					if is_digit(element[i + 2]):
						power = 0
						j = i + 2
						while j < len(element) and is_digit(element[j]):
							power *= 10
							power += int(element[j])
							j += 1
						powers.append((element[i], power))
						i = j
					else:
						powers.append((element[i], element[i + 2]))
						i += 3
		else:
			print("Badly formed language")
			return None
	print("Rewrote language as:", powers)
	return powers


def compute_len(powers):
	"""
	Returns the sum of all exponents
	"""
	length = 0
	for (_, power) in powers:
		length += power
	return length


def min_len(powers):
	"""
	Every word has a minimum length
	(when all the variables appearing as exponents are 0).
	"""
	length = 0
	for (_, power) in powers:
		if str != type(power):
			length += power
	return length


def check_conditions(w, conditions, exponent_values):
	return parser.check_conditions(conditions, w, exponent_values)


def choose_random_word(powers, conditions):
	"""
	Create a random word matching the given parameter
	and pick a random pumping length.
	"""
	found_valid_word = False
	while not found_valid_word:
		found_valid_word = True
		exponent_value = {}
		w = []
		for (base, power) in powers:
			if type(power) == str:
				if power in exponent_value:
					w.append((base, exponent_value[power]))
				else:
					exponent_value[power] = randrange(1, max_exponent)  # don't allow missing powers
					w.append((base, exponent_value[power]))
			else:
				w.append((base, power))
		w = merge_powers(w)
		print("Computed random w:", w)
		try:
			pumping_len = randrange(min_len(powers) + 1, compute_len(w) + 1)
			# print("Computed pumping length:", pumping_len)
		except:
			found_valid_word = False

		if found_valid_word:
			print("Checking conditions...")
			found_valid_word = check_conditions(w, conditions, exponent_value)
			print("Conditions passed!" if found_valid_word else "Conditions failed :(")		
	return pumping_len, w


def pick_x(w, n):
	x = []
	length = 0
	for (base, power) in w:
		if length + power < n:
			length += power
			x.append((base, power))
		else:
			x.append((base, n - length))
			print("x =", x)
			return x


def pick_y(w, i, j):
	y = []
	lengthx = 0
	lengthy = 0
	k = 0
	
	# pass x
	power = w[k][1]
	while lengthx + power < i:
		lengthx += power
		k += 1
		power = w[k][1]
	
	# build y
	power = power - i + lengthx
	while lengthy + power < j - i:
		lengthy += power
		y.append((w[k][0], power))
		k += 1
		power = w[k][1]
	if y:
		y.append((w[k][0], j - i - lengthy))
	else:
		y.append((w[k][0], j - i))
	print("y =", y)
	return y


def pick_z(w, j):
	z = []
	lengthxy = 0
	k = 0
	
	# pass xy
	power = w[k][1]
	while lengthxy + power < j:
		lengthxy += power
		k += 1
		power = w[k][1]
	
	# build z
	z.append((w[k][0], power - j + lengthxy))
	k += 1
	while k < len(w):
		z.append((w[k][0], w[k][1]))
		k += 1
	print("z =", z)
	return z


def split_word1(w, n):
	"""
	Return all possible x, y, z divisions as tuples in a list.
	n is the upper bound.
	"""
	res = []
	for i in range(n):  # x has length i
		x = pick_x(w, i)
		for j in range(i + 1, n + 1):  # xy has length j
			y = pick_y(w, i, j)
			z = pick_z(w, j)
			res.append((x, y, z))
	return res


def split_word2(w, lower_bound, upper_bound):
	"""
	Return all possible x, y, z divisions as tuples in a list.
	"""
	res = []
	for i in range(upper_bound - 1):  # x has length i
		x = pick_x(w, i)
		for j in range(max(i + 1, lower_bound), upper_bound):  # xy has length j
			y = pick_y(w, i, j)
			z = pick_z(w, j)
			res.append((x, y, z))
	return res


def get_variables(w):
	vars = []
	for (_, power) in w:
		if power not in vars and type(power) == str:
			vars.append(power)
	return vars


def is_finite(w, conditions):
	vars_in_desc = get_variables(w)
	print("vars_in_desc =", vars_in_desc)
	vars_in_cond = parser.check_finite(conditions)
	print("vars_in_cond =", vars_in_cond)
	return set(vars_in_desc).issubset(vars_in_cond)


def word_power(w, k):
	"""
	Compute w^k.

	E.g: w = [('a', 1)]
	w^0 = [('', 0)]
	w^1 = [('a', 1)]
	w^2 = [('a', 1), ('a', 1)]
	"""
	res = []
	for i in range(k):
		res += w
	return res if res else [('', 0)]


def select_first_power(w):
	"""
	Select the first power, ensuring that
	we merge powers with the same base.
	E.g: [('a', 1), ('a', 'n')] returns itself
	"""
	first_power = []
	i = 0
	for el in w:
		if el[0] != w[0][0]:
			break
		first_power.append(el)
		i += 1
	return first_power, w[i:]


def select_exponents(w):
	"""
	Return a list of all the exponents in w
	"""
	exponents = []
	for (_, exponent) in w:
		exponents.append(exponent)
	return exponents


def rec_compute_values(count, step, target, exponents, values):
	if count == 0:
		return values
	if step == count - 1:
		exponents[step] = target
		values.append(exponents)
		return values
	for i in range(target):
		exponents[step] = i
		values = rec_compute_values(count, step + 1, target - i, exponents, values)
	return values


def check_inclusion(w, powers, conditions):
	"""
	w: x y^k z
	powers: the language
	conditions: used to keep things such as n = 6
	"""

	# either w or powers is empty
	if not w and not powers:
		return True
	if not w:
		for el in powers:
			if isinstance(el[1], int) and el[1] != 0:
				return False
		return True
	if not powers:
		for el in w:
			if isinstance(el[1], int) and el[1] != 0:
				return False
		return True
	
	# first power does not match
	first_power, rest_power = select_first_power(powers)
	if w[0][0] != powers[0][0]:
		for power in first_power:
			if type(power[1]) == str:
				if power[1] in conditions:
					if conditions[power[1]] != 0:
						return False
				else:
					conditions[power[1]] = 0
			elif power[1] != 0:
				return False
		return check_inclusion(w, rest_power, conditions)
	
	# common case
	exponents = select_exponents(first_power)
	variables = []
	total_exponent = 0
	for exponent in exponents:
		if type(exponent) == str:
			if exponent in conditions:
				total_exponent += conditions[exponent]
			else:
				if exponent not in variables:
					variables.append(exponent)
		else:
			total_exponent += exponent
	if total_exponent > w[0][1]:
		return False
	if total_exponent == w[0][1]:
		return check_inclusion(w[1:], rest_power, conditions)
	values = rec_compute_values(len(variables), 0, w[0][1] - total_exponent, \
		                        [None for i in range(len(variables))], [])
	if not values:
		return check_inclusion(w[1:], rest_power, conditions)
	for value in values:
		for i, exponent in enumerate(value):
			conditions[variables[i]] = exponent
		if check_inclusion(w[1:], rest_power, conditions):
			return True
	return False


def main(lang_desc):
	description = lang_desc
	element, conditions = description.split('|')
	element = element.strip()
	conditions = conditions.strip()

	data = {"k_stop" : 10, "no_w_stop" : 100, "res" : 1}

	powers = parse_element(element)

	if is_finite(powers, conditions):
		print("Finite language")
		return data

	for i in range(w_picks):  # try this many times
		pumping_len, w = choose_random_word(powers, conditions)

		if len(powers) >= compute_len(w):  # no xyz split will be possible
			continue

		# configure
		if conf == 1:
			xyz = split_word1(w, pumping_len)
		elif conf == 2:
			if len(powers) >= pumping_len:  # no xyz split will be possible
				continue
			xyz = split_word2(w, len(powers) + 1, pumping_len + 1)
		elif conf == 3:
			xyz = split_word2(w, len(powers) + 1, compute_len(w) + 1)
		else:
			continue


		xyz_bool_acc = False  # True = at least one xyz validates the lemma
							  # False = no xyz validates the lemma
		for x, y, z in xyz:
			print("x, y, z =", x, y, z)
			k_bool_acc = True  # True = all k validate the lemma
			                   # False = there is at least one k
			                   #         that invalidates the lemma
			for k in range(2, k_picks):  # try consecutive k, but not 0 or 1
				y_pow_k = word_power(y, k)
				print("y^k = ", y_pow_k)
				new_w = x + y_pow_k + z
				new_w = merge_powers(new_w)
				print("neww =", new_w)
				exponent_values = {}
				if not check_inclusion(new_w, powers, exponent_values) \
				or not check_conditions(new_w, conditions, exponent_values):
					k_bool_acc = False
					data["k_stop"] = k
					break
			if k_bool_acc:
				xyz_bool_acc = True
				break
		if not xyz_bool_acc:
			data["no_w_stop"] = i
			data["res"] = 0
			print("Non-regular language")
			return data
	data["k_stop"] = 10
	data["no_w_stop"] = 100
	print("Regular language... probably")
	return data


if __name__ == "__main__":
	print(main(input()))
