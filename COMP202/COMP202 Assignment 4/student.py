#Author: Ethan Lim 261029610

class Student:
	'''Class that defines a student at McGill University

	Attributes: student_id, name, is_sick'''
	
	def __init__(self, student_id, name, is_sick=False):
		self.student_id = student_id
		self.name = name
		self.is_sick = is_sick

		if not self.is_valid_id(student_id):
			raise ValueError("The student ID " + student_id + " is not a valid ID")

	def __str__(self):
		'''(none) -> str
		Overwrites printable representation of object
		>>> larry = Student('260745567', 'Larry', True)

		>>> str(larry)
		'Larry (260745567)'

		>>> ethan = Student('260029610', 'Ethan')

		>>> str(ethan)
		'Ethan (260029610)'

		>>> ethan = Student('261029610', 'Ethan')
		ValueError: The student ID 261029610 is not a valid ID
		'''

		return self.name + " (" + self.student_id + ")"

	def __repr__(self):
		'''(none) -> str
		Overwrites printable representation of object
		>>> larry = Student('260745567', 'Larry', True)

		>>> repr(larry)
		'Larry (260745567)'

		>>> ethan = Student('260029610', 'Ethan')

		>>> repr(ethan)
		'Ethan (260029610)'

		>>> ethan = Student('261029610', 'Ethan')
		ValueError: The student ID 261029610 is not a valid ID
	
		'''
		return self.__str__()

	@staticmethod
	def is_valid_id(student_id):
		"""(str) -> bool
		Returns True or False depending on if student_id is a valid McGill ID

		>>> Student.is_valid_id('123000000')
		False

		>>> Student.is_valid_id('McGill123')
		False

		>>> Student.is_valid_id('260029619')
		True

		"""
		alphabet = 'abcdefghijklmnopqrstuvwxyz'

		if student_id[0:3] != '260': #first 3 digits in id are checked
			return False
		if len(student_id) != 9:
			return False

		for char in student_id:
			if char in alphabet:
				return False

		return True

	@classmethod
	def from_JSON(cls, info_str):
		"""(str) -> Student
		Constructs Student Object given the details in info_str

		>>> larry = Student.from_JSON('{"id": "260745567", "name": "Larry"}')
		
		>>> str(larry)
		'Larry (260745567)'

		>>> ethan = Student.from_JSON('{"id": "260029610", "name": "Ethan"}')

		>>> str(ethan)
		'Ethan (260029610)'

		>>> ethan = Student.from_JSON('{"id": "261029610", "name": "Ethan"}')
		ValueError: The student ID 261029610 is not a valid ID
		"""
		info_list = info_str.replace("{", "").replace("}", "").split(",") #converts dictionary string into list, splitting by key-value pairs
		info_list[0] = info_list[0].split(":") #modifies first key value pair to prioritize the value (student_id)
		info_list[0][1] = info_list[0][1][2:len(info_list[0][1]) - 1] 
		
		info_list[1] = info_list[1].split(":") #modifies second key value pair top prioritize the value (name)
		info_list[1][1] = info_list[1][1][2:len(info_list[1][1]) - 1]
            
		return cls(info_list[0][1], info_list[1][1])

