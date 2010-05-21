class ValidateError(Exception):
	pass

def validate_number(val, minval=None, maxval=None):
	try:
		_val = float(val)
	except ValueError, e:
		raise ValidateError('NAN %s' % e)

	if minval is not None and _val < minval:
		raise ValidateError('MINVAL')

	if maxval is not None and _val > maxval:
		raise ValidateError('MAXVAL')
