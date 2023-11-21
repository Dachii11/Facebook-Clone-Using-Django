def human_format(n):
	num = float('{:.3g}'.format(n))
	magnitude = 0
	while abs(num)>=1000:
			magnitude += 1
			num /= 1000.0
	# return ['{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.')),magnitude]
	return ['{}'.format('{:f}'.format(num).rstrip('0').rstrip('.')),magnitude]

def get_letter_for_number_format(magnitude):
	print(magnitude)
	return '{}'.format(['','K','M','B','T'][magnitude])