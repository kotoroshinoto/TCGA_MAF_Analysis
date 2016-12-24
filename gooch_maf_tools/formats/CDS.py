from enum import Enum, unique
import re
import sys
from io import StringIO

char_to_loctype = dict()  # type: dict[str, LocusType]
loctype_to_char = dict()  # type: dict[LocusType, str]

@unique
class LocusType(Enum):
	GENOME = 1
	CODING = 2
	NONCODING = 3
	PROTEIN = 4

	@staticmethod
	def from_character(c: str) -> 'LocusType':
		assert (len(c) == 1)
		return char_to_loctype[c.lower()]

	@staticmethod
	def to_character(lt: 'LocusType') -> 'str':
		return loctype_to_char[lt]

char_to_loctype['g'] = LocusType.GENOME
char_to_loctype['c'] = LocusType.CODING
char_to_loctype['n'] = LocusType.NONCODING
char_to_loctype['p'] = LocusType.PROTEIN

loctype_to_char[LocusType.GENOME] = 'g'
loctype_to_char[LocusType.CODING] = 'c'
loctype_to_char[LocusType.NONCODING] = 'n'
loctype_to_char[LocusType.PROTEIN] = 'p'

str_to_changetype = dict()  # type: dict[str, ChangeType]
changetype_to_str = dict()  # type: dict[ChangeType, str]

@unique
class ChangeType(Enum):
	SEQ_VARIANT = 1
	INS = 2
	DEL = 3
	DUP = 4
	@staticmethod
	def from_str(text: str) -> 'ChangeType':
		return str_to_changetype[text]

	@staticmethod
	def to_str(ct: 'ChangeType') -> str:
		return changetype_to_str[ct]

str_to_changetype[""] = ChangeType.SEQ_VARIANT
str_to_changetype["ins"] = ChangeType.INS
str_to_changetype["del"] = ChangeType.DEL
str_to_changetype["dup"] = ChangeType.DUP

changetype_to_str[ChangeType.SEQ_VARIANT] = ""
changetype_to_str[ChangeType.INS] = "ins"
changetype_to_str[ChangeType.DEL] = "del"
changetype_to_str[ChangeType.DUP] = "dup"


class CDS:
	nv_regex = re.compile("^[gcn][.]([*]?[-]?\d+(?:[-+]\d+)?)(?:_([*]?[-]?\d+(?:[-+]\d+)?))?(\S+)>(\S+)$")
	indel_or_dup_regex = re.compile("^[gcn][.]([*]?[-]?\d+(?:[-+]\d+)?)(?:_([*]?[-]?\d+(?:[-+]\d+)?))?(ins|del|dup)(\S+)$")
	prot_amino_regex = re.compile("^p[.]([A-z]+)(\d+)(\S+)$")  # (fs(?:[*]|Ter)\d+)?

	def __init__(self, text:str):
		self.start = None
		self.end = None
		self.orig_seq = None
		self.new_seq = None
		self.loctype = LocusType.from_character(text[0])  # type: LocusType
		self.cdstype = None
		if text == 'p.=':
			return
		match_count = 0
		match_obj_nv = CDS.nv_regex.match(text)
		match_obj_indul_or_dup = CDS.indel_or_dup_regex.match(text)
		match_prot = CDS.prot_amino_regex.match(text)
		if match_obj_nv:
			match_count += 1
		if match_obj_indul_or_dup:
			match_count += 1
		if match_prot:
			match_count += 1
		if match_count > 1:
			raise(RuntimeError("[CDS].__Init__ both regexes matched text: '%s'" % text))
		if match_count < 1:
			raise(RuntimeError("unmatchable text: '%s'" % text))
		if match_obj_nv:
			groups = match_obj_nv.groups()
			# i = 0
			# for item in groups:
			# 	print("group[%d] : '%s'" % (i, item), file=sys.stderr)
			# 	i += 1
			self.start = groups[0]
			self.end = groups[1]
			self.orig_seq = groups[2]
			self.new_seq = groups[3]
			self.cdstype = ChangeType.SEQ_VARIANT
		if match_obj_indul_or_dup:
			groups = match_obj_indul_or_dup.groups()
			# i = 0
			# for item in groups:
			# 	print("group[%d] : '%s'" % (i, item), file=sys.stderr)
			# 	i += 1
			self.start = groups[0]
			self.end = groups[1]
			self.new_seq = groups[3]
			self.cdstype = ChangeType.from_str(groups[2])
		if match_prot:
			groups = match_prot.groups()
			self.orig_seq = groups[0]
			self.start = groups[1]
			self.new_seq = groups[2]
			# i = 0
			# for item in groups:
			# 	print("group[%d] : '%s'" % (i, item), file=sys.stderr)
			# 	i += 1

	def __str__(self):
		if self.loctype != LocusType.PROTEIN:
			loctype_c = LocusType.to_character(self.loctype)
			pos_seq = None
			if self.end is not None:
				pos_seq = "%s.%s_%s" % (loctype_c, self.start, self.end)
			else:
				pos_seq = "%s.%s" % (loctype_c, self.start)
			change_text = None
			if self.cdstype == ChangeType.SEQ_VARIANT:
				change_text = "%s>%s" % (self.orig_seq, self.new_seq)
			else:
				change_text = "%s%s" % (ChangeType.to_str(self.cdstype), self.new_seq)
			return pos_seq+change_text
		else:
			return "%s%s%s" % (self.orig_seq, self.start, self.new_seq)


for line in sys.stdin:
	cds = CDS(line.rstrip())
	print(cds)
