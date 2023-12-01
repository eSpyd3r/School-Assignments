#Author: Ethan Lim 261029610
from contactTracker import *

def id_to_student(student_id_str):
	"""(str) -> str
	Returns Student object as string from a given ID
	"""

	for student in ContactTracker.default_students:
		if student_id_str == student.student_id:
			return repr(student)

def define_sick_students(csv_dictionary, student_list):
	"""(dict, list) -> dict, list
	Updates is_sick attribute for the sick students in csv_dictionary
	"""
	list_to_update = student_list[:] #deep copies student_list, as we don't want to modify the input list
	for sick_student in csv_dictionary:
		for student in list_to_update:
			if sick_student == student.student_id: #identifies which students to declare is_sick = True
				student.is_sick = True
				break
	return list_to_update

def load_file(file_name):
	"""(str) -> str
	Opens file and returns contents as string
	"""
	file_object = open(file_name, "r")

	try:
		data = file_object.read()
		file_object.close()

		return data
	except:
		file_object.close()

def JSON_to_students(json):
	"""(str) -> list
	Returns list of Student objects converted from json string
	>>> data = load_file("all_students.json")

	>>> print(JSON_to_students(data))
	[Bob (260808934), Paul (260840155), Mark (260248711), Carol (260996175), Leanne (260476020), \
	Will (260561504), Farley (260675874), Sarai (260758421), Larry (260386543), \
	Philip (260212160), Zach (260970944)]

	>>> data = load_file("all_students.json")

	>>> print(JSON_to_students(data))
	[Alice (260018288), Bob (260808934), Carol (260996175), Darryl (260084903), \
	Ettienne (260026473), Forbert (260072990), Gordie (260039118), Hanes (260041845), \
	Illersley (260092533), Job (260013314), Kirk (260041812), Lammle (260065208), Molly (260061737)]

	>>> data = load_file("all_students.json")

	>>> print(JSON_to_students(data))
	[Angelina (260095234), Francesca (260032440), Rory (260092283), Piper (260055764), Sanaa (260025405), Danna (260068680), Ayla (260005925), Leonardo (260031356), Reed (260010997), Jackson (260014616), \
	Zara (260026754), Avah (260072488), Anahi (260068501), Hailee (260012075), Naima (260071927), Weston (260094691), Maddison (260031971), Brittany (260092902), Jasmine (260094997), Hadley (260064375)]

	"""
	json = json[1:len(json) - 1] #doesn't include first and last indexes since they are brackets; spliting into list anyway
	
	json_as_list = json.split("\n\t") #each new line is a new set of students
	json_as_list = json_as_list[1:] #index 0 is empty, thus neglected


	list_of_students = []
	for identity in json_as_list: #each student exists in json_as_list as strings; converting into Student objects
		list_of_students.append(Student.from_JSON(identity))

	for students in list_of_students: #form_JSON successfully creates Student objects for every student except the last; due to the fact that there is no ',' at the send as it is the last in the list. This removes the extra '"' in the student's name as a result
		if '"' in students.name:
			students.name = students.name.replace('"', "")

	
	return list_of_students


def csv_to_dictionary(csv_string):
	"""(str) -> dict
	Returns dictionary, based on csv_string, that contains keys of sick student ids with values as lists of student ids that the sick student had contact with

	>>> data = load_file("cases.csv")

	>>> print(csv_to_dictionary(data))
	{'260808934': ['260840155', '260248711', '260996175', '260476020', '260561504'],\
	'260996175': ['260248711', '260476020'], '260675874': ['260840155'], '260476020': ['260758421'],\
	'260386543': ['260996175', '260248711', '260476020', '260561504'], '260248711': ['260212160', '260970944'],\
	'260840155': ['260970944'], '260561504': ['260476020', '260248711'], '260970944': ['260212160']}

	>>>data = load_file("cases.csv")

	>>>print(csv_to_dictionary(data))
	{'260018288': ['260808934', '260996175', '260084903', '260026473', '260072990', '260039118'],\
	'260041845': ['260808934', '260996175', '260026473', '260072990'], '260092533': ['260084903', '260026473', '260072990', '260013314', '260041812', '260039118'],\
	'260013314': ['260065208'], '260072990': ['260061737', '260013314'], '260041812': ['260013314'], '260084903': ['260065208'], '260808934': ['260065208'],\
	'260026473': ['260065208'], '260996175': ['260065208'], '260061737': ['260013314', '260041812'], '260039118': ['260041812']}

	>>> data = load_file("cases.csv")

	>>> print(csv_to_dictionary(data))
	{'260064375': ['260005925', '260032440'], '260094997': ['260072488', '260026754', '260010997', '260031971'], '260092902': ['260010997', '260068501', '260005925', '260064375'], '260031971': ['260092283', '260092902', '260010997', '260005925'], \
	'260010997': ['260005925', '260031356'], '260068680': ['260094691', '260092283', '260005925'], '260071927': ['260068680', '260094691', '260014616'], '260014616': ['260064375', '260026754', '260092902', '260010997', '260092283'], \
	'260094691': ['260005925', '260092902'], '260026754': ['260064375', '260010997', '260005925', '260092902', '260068501'], '260072488': ['260064375'], '260092283': ['260064375', '260068501', '260010997', '260092902', '260005925'], \
	'260012075': ['260095234'], '260025405': ['260094997'], '260055764': ['260031971'], '260068501': ['260005925'], '260095234': ['260092902']}

	"""

	csv_string_list = csv_string.split("\n") #each new line represents a new viral student; these sets are organized into their own indexes in a list

	csv_dictionary = {}
	for viral_student_set in csv_string_list: #iterates through each viral_student_set and adds the first student as a key to the dictionary with the rest representing the values/ids of contact
		viral_student_set_list = viral_student_set.split(', ')
		csv_dictionary[viral_student_set_list[0]] = viral_student_set_list[1:]

	return csv_dictionary

def build_report(ContactTracker):
	"""(ContactTracker) -> str
	Returns string that is found in the final report; the information comes from the methods/attributes of the ContactTracker object
	"""
	sick_student_ids = ContactTracker.cases_with_contacts.keys()
	report_string = "Contact Records:" #string that is being returned; will constantly be added to

	for sick_id in sick_student_ids: #loop that it responisble for iterating through each spreader and its contacts
		student_line = "\n\t"
		student_obj = id_to_student(sick_id)
		student_line += student_obj + ' had contact with '
		
		contact_list = ContactTracker.get_contacts_by_student_id(sick_id)
		
		if len(contact_list) == 0: #specific scenario as described in the pdf
			student_line += 'none'
		else:
			for contact in contact_list:
				student_line += repr(contact) + ', ' #repr needed as we are adding to stirng student_line

			report_string += student_line[0: len(student_line) - 2]

	report_string += '\n\nPatient Zero(s): '

	patient_zeros = ContactTracker.patient_zeros()

	if len(patient_zeros) == 0: #specific scenario as described in pdf
		report_string += 'none'
	else:
		for patient_zero in patient_zeros:
			report_string += repr(patient_zero) + ', '

		report_string = report_string[0: len(report_string) - 2] #removes ','
	report_string += '\nPotential sick students: '

	potential_sick_students = ContactTracker.potential_sick_students()

	if len(potential_sick_students) == 0:	#specific scenario as described in pdf
		report_string += 'none'
	else:
		for potential_sick_student in potential_sick_students:
			report_string += repr(potential_sick_student) + ', '

		report_string = report_string[0: len(report_string) - 2] #removes ', ' that is added in previous line
	report_string += '\nSick students who got infected from another student: '

	sick_from_another_student_list = ContactTracker.sick_from_another_student()

	if len(sick_from_another_student_list) == 0:	#specific scenario as described in pdf
		report_string += 'none'
	else:
		for sick_from_another_student in sick_from_another_student_list:
			report_string += repr(sick_from_another_student)  + ', '

		report_string = report_string[0: len(report_string) - 2] #removes ', ' that is added in previous line
	report_string += '\nMost viral students: '

	most_viral_students_list = ContactTracker.most_viral_students()

	if len(most_viral_students_list) == 0:	#specific scenario as described in pdf
		report_string += 'none'
	else:
		for most_viral_student in most_viral_students_list:
			report_string += repr(most_viral_student) + ', '

		report_string = report_string[0: len(report_string) - 2] #removes ', ' that is added in previous line
	report_string += '\nMost contacted students: '

	most_contacted_students = ContactTracker.most_contacted_student()

	if len(most_contacted_students) == 0:	#specific scenario as described in pdf
		report_string += 'none'
	else:
		for most_contacted_student in most_contacted_students:
			report_string += repr(most_contacted_student) + ', '
		report_string = report_string[0: len(report_string) - 2] #removes ', ' that is added in previous line

	report_string += '\nUltra Spreaders: '

	ultra_spreaders = ContactTracker.ultra_spreaders()

	if len(ultra_spreaders) == 0:	#specific scenario as described in pdf
		report_string += 'none'
	else:
		for ultra_spreader in ultra_spreaders:
			report_string += repr(ultra_spreader) + ', '

		report_string = report_string[0: len(report_string) - 2] #removes ', ' that is added in previous line
	report_string += '\nNon-spreaders: '

	non_spreaders = ContactTracker.non_spreaders()

	if len(non_spreaders) == 0:	#specific scenario as described in pdf
		report_string += 'none'
	else:
		for non_spreader in non_spreaders:
			report_string += repr(non_spreader) + ', '

		report_string = report_string[0: len(report_string) - 2] #removes ', ' that is added in previous line

	return report_string.replace("'", "").replace('"', "")

def write_in_file(file_name, text):
	"""(str, str) -> none
	Writes contents of text to file_name
	"""
	file_object = open(file_name, "w")

	try:
		file_object.write(text)
		file_object.close()
	except: 
		file_object.close()

def main():
	"""(none) -> none
	Iterates through each process of the written data analysis; produces new file contact_tracing_report.txt consisting of the data string
	"""
	try:
		data = load_file('all_students.json')
		student_list = JSON_to_students(data)
	except FileNotFoundError:
		raise FileNotFoundError("Sorry, the file all_students.json could not be found.")

	try:
		data_cases = load_file('cases.csv')
		csv_dictionary = csv_to_dictionary(data_cases)
	except FileNotFoundError:
		raise FileNotFoundError("Sorry, the file cases.csv could not be found.")

	updated_list = define_sick_students(csv_dictionary, student_list)
	analysis = ContactTracker(updated_list, csv_dictionary)
	final_data = build_report(analysis)

	try:
		write_in_file('contact_tracing_report.txt', final_data)
	except FileNotFoundError:
		raise FileNotFoundError("Sorry, the file contact_tracing_report.txt could not be found.")