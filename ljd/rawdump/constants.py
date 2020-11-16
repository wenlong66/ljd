#
# Copyright (C) 2013 Andrian Nord. See Copyright Notice in main.py
#

import sys
import struct
from ljd.util.log import errprint

import ljd.bytecode.constants

import gconfig

BCDUMP_KGC_CHILD = 0
BCDUMP_KGC_TAB = 1
BCDUMP_KGC_I64 = 2
BCDUMP_KGC_U64 = 3
BCDUMP_KGC_COMPLEX = 4
BCDUMP_KGC_STR = 5


BCDUMP_KTAB_NIL = 0
BCDUMP_KTAB_FALSE = 1
BCDUMP_KTAB_TRUE = 2
BCDUMP_KTAB_INT = 3
BCDUMP_KTAB_NUM = 4
BCDUMP_KTAB_STR = 5


def read(parser, constants):
	r = True

	r = r and _read_upvalue_references(parser, constants.upvalue_references)
	r = r and _read_complex_constants(parser, constants.complex_constants)
	r = r and _read_numeric_constants(parser, constants.numeric_constants)

	return r


def _read_upvalue_references(parser, references):
	i = 0

	while i < parser.upvalues_count:
		i += 1
		upvalue = parser.stream.read_uint(2)
		# print("_read_upvalue_references upvalue:%x" % upvalue)
		references.append(upvalue)

	return True


def _read_complex_constants(parser, complex_constants):
	i = 0

	while i < parser.complex_constants_count:
		constant_type = parser.stream.read_uleb128()
		# print("_read_complex_constants constant_type:%x" % constant_type)
		if constant_type >= BCDUMP_KGC_STR:
			length = constant_type - BCDUMP_KGC_STR

			string = parser.stream.read_bytes(length)
			# print ("_read_complex_constants string:%s" % string.decode("unicode-escape"))
			#zzw 20180714 support str encode
			complex_constants.append(string.decode(gconfig.gFlagDic['strEncode']))
		elif constant_type == BCDUMP_KGC_TAB:
			table = ljd.bytecode.constants.Table()

			if not _read_table(parser, table):
				return False

			complex_constants.append(table)
		elif constant_type != BCDUMP_KGC_CHILD:
			number = _read_number(parser)
			# print("_read_complex_constants number:%x" % number)
			if constant_type == BCDUMP_KGC_COMPLEX:
				imaginary = _read_number(parser)
				# print("_read_complex_constants imaginary:%x" % imaginary)
				complex_constants.append((number, imaginary))
			else:
				complex_constants.append(number)
		else:
			complex_constants.append(parser.prototypes.pop())

		i += 1

	return True


def _read_numeric_constants(parser, numeric_constants):
	i = 0

	while i < parser.numeric_constants_count:
		isnum, lo = parser.stream.read_uleb128_from33bit()
		# print("_read_numeric_constants isnum %x lo %x" % (isnum,lo))
		if isnum:
			hi = parser.stream.read_uleb128()

			number = _assemble_number(lo, hi)
		else:
			number = _process_sign(lo)

		# print("_read_numeric_constants number %x" % number)
		numeric_constants.append(number)

		i += 1

	return True


def _read_number(parser):
	lo = parser.stream.read_uleb128()
	hi = parser.stream.read_uleb128()

	return _assemble_number(lo, hi)


def _read_signed_int(parser):
	number = parser.stream.read_uleb128()

	return _process_sign(number)


def _assemble_number(lo, hi):
	if sys.byteorder == 'big':
		float_as_int = lo << 32 | hi
	else:
		float_as_int = hi << 32 | lo

	raw_bytes = struct.pack("=Q", float_as_int)
	return struct.unpack("=d", raw_bytes)[0]


def _process_sign(number):
	if number & 0x80000000:
		return -0x100000000 + number
	else:
		return number


def _read_table(parser, table):
	array_items_count = parser.stream.read_uleb128()
	hash_items_count = parser.stream.read_uleb128()
	# print("_read_table array_items_count:%x" % array_items_count)
	# print("_read_table hash_items_count:%x" % hash_items_count)
	while array_items_count > 0:
		constant = _read_table_item(parser)
		# constant and print("_read_table constant:%s" % constant)

		table.array.append(constant)

		array_items_count -= 1

	while hash_items_count > 0:
		key = _read_table_item(parser)
		value = _read_table_item(parser)
		# print("_read_table key:%s" % key)
		# print("_read_table value:%s" % value)

		table.dictionary.append((key, value))

		hash_items_count -= 1

	return True


def _read_table_item(parser):
	data_type = parser.stream.read_uleb128()

	if data_type >= BCDUMP_KTAB_STR:
		length = data_type - BCDUMP_KTAB_STR
		# zzw 20180714 support str encode
		return parser.stream.read_bytes(length).decode(gconfig.gFlagDic['strEncode'])

	elif data_type == BCDUMP_KTAB_INT:
		return _read_signed_int(parser)

	elif data_type == BCDUMP_KTAB_NUM:
		return _read_number(parser)

	elif data_type == BCDUMP_KTAB_TRUE:
		return True

	elif data_type == BCDUMP_KTAB_FALSE:
		return False

	else:
		assert data_type == BCDUMP_KTAB_NIL

		return None
