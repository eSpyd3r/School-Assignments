#Author: Ethan Lim 261029610
from student import *

class ContactTracker:
	'''Class that will make up the data in the analysis of the spread of COVID

	Attributes: students, cases_with_contacts'''
	default_students = []

	def __init__(self, students, cases_with_contacts):
		ContactTracker.default_students = self.define_sick_students(cases_with_contacts, students)
		cases_with_contacts_dup = {}

		ContactTracker.default_student_id_list = []
		for student in ContactTracker.default_students:
			ContactTracker.default_student_id_list.append(student.student_id)
		
		for student_id in cases_with_contacts: #deep copying of cases_with_contacts
			student_id_hold = []
			if student_id not in ContactTracker.default_student_id_list:
				raise ValueError("A student with id " + student_id +  " either doesn't exist or is not reported sick.")

			student_id_hold.append(student_id)

			exposed_id_hold = []
			for exposed_id in cases_with_contacts[student_id]: #continued deep copying of cases_with_contacts
				if exposed_id not in ContactTracker.default_student_id_list:
					raise ValueError("A student with id " + student_id +  " either doesn't exist or is not reported sick.")
				
				exposed_id_hold.append(exposed_id)

			cases_with_contacts_dup[student_id_hold[0]] = exposed_id_hold

		self.cases_with_contacts = cases_with_contacts_dup #attribute is equal to the deep copy

	def define_sick_students(self, csv_dictionary, student_list):
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

	def get_contacts_by_student_id(self, student_id):
		"""(str) -> list
		Returns list of students that student_id has been in contact with
		>>> students_list = contact_tracker.get_contacts_by_student_id('260996175')

		>>> print(students_list)
		[Mark (260248711), Leanne (260476020)]

		>>> student_list = analysis.get_contacts_by_student_id('260013314')
		
		>>> print(student_list)
		[Lammle (260065208)]
		
		>>> student_list = analysis.get_contacts_by_student_id('260')
		ValueError: A student with id 260 either doesn't exist or is not reported sick.
	
		"""

		if student_id not in ContactTracker.default_student_id_list: #not a real student/not found
			raise ValueError("A student with id " + student_id + " either doesn't exist or is not reported sick.")

		cases_with_contacts_dict = self.cases_with_contacts
		exposed_list = []
		for exposed_id in cases_with_contacts_dict[student_id]: #matches exposed student id to ids of students found in the default list, then adds the student to exposed_list
			for student in ContactTracker.default_students:
				if student.student_id == exposed_id:
					exposed_list.append(student)

		return exposed_list

	def collect_victims(self):
		"""(none) -> list
		Returns list of nested lists that contain all exposed victims
		"""
		exposure_victims = []

		cases_with_contacts_dict = self.cases_with_contacts
		for sick_student in cases_with_contacts_dict:
			exposure_victims.append(cases_with_contacts_dict[sick_student]) #each student list that was in contact with a viral student is appended to exposure_victims

		return exposure_victims


	def get_all_contacts(self):
		"""(none) -> dict
		Returns dictionary with keys of sick student_ids and values of students who came in contact with the sick student

		>>> print(contact_tracker.get_all_contacts())
		{'260808934': [Paul (260840155), Mark (260248711), Carol (260996175), Leanne (260476020),\
		Will (260561504)],\
		'260996175': [Mark (260248711), Leanne (260476020)],\
		'260675874': [Paul (260840155)],\
		'260476020': [Sarai (260758421)],\
		'260386543': [Carol (260996175), Mark (260248711), Leanne (260476020), Will (260561504)],\
		'260248711': [Philip (260212160), Zach (260970944)],\
		'260840155': [Zach (260970944)],\
		'260561504': [Leanne (260476020), Mark (260248711)],\
		'260970944': [Philip (260212160)]}\

		>>> print(contact_tracker.get_all_contacts())
		{'260018288': [Bob (260808934), Carol (260996175), Darryl (260084903), Ettienne (260026473), Forbert (260072990), Gordie (260039118)], \
		'260808934': [Lammle (260065208)], '260996175': [Lammle (260065208)], '260084903': [Lammle (260065208)], '260026473': [Lammle (260065208)], '260072990': [Molly (260061737), Job (260013314)], \
		'260039118': [Kirk (260041812)], '260041845': [Bob (260808934), Carol (260996175), Ettienne (260026473), Forbert (260072990)], '260092533': [Darryl (260084903), Ettienne (260026473), Forbert (260072990), Job (260013314), Kirk (260041812), Gordie (260039118)], \
		'260013314': [Lammle (260065208)], '260041812': [Job (260013314)], '260061737': [Job (260013314), Kirk (260041812)]}

		>>> print(contact_tracker.get_all_contacts())
		{'260095234': [Brittany (260092902)], '260092283': [Hadley (260064375), Anahi (260068501), Reed (260010997), Brittany (260092902), Ayla (260005925)], \
		'260055764': [Maddison (260031971)], '260025405': [Jasmine (260094997)], '260068680': [Weston (260094691), Rory (260092283), Ayla (260005925)], \
		'260010997': [Ayla (260005925), Leonardo (260031356)], '260014616': [Hadley (260064375), Zara (260026754), Brittany (260092902), Reed (260010997), Rory (260092283)], \
		'260026754': [Hadley (260064375), Reed (260010997), Ayla (260005925), Brittany (260092902), Anahi (260068501)], '260072488': [Hadley (260064375)], \
		'260068501': [Ayla (260005925)], '260012075': [Angelina (260095234)], '260071927': [Danna (260068680), Weston (260094691), Jackson (260014616)], \
		'260094691': [Ayla (260005925), Brittany (260092902)], '260031971': [Rory (260092283), Brittany (260092902), Reed (260010997), Ayla (260005925)], \
		'260092902': [Reed (260010997), Anahi (260068501), Ayla (260005925), Hadley (260064375)], '260094997': [Avah (260072488), Zara (260026754), Reed (260010997), Maddison (260031971)], \
		'260064375': [Ayla (260005925), Francesca (260032440)]}
		"""
		contact_dict = {}

		for student in ContactTracker.default_students:
			if student.is_sick == True: #only iterates for sick students
				contact_dict[student.student_id] = self.get_contacts_by_student_id(student.student_id) #key of dictionary is student.student_id, and its value is obtained form calling get_contacts_by_student_id

		return contact_dict

	def patient_zeros(self):
		"""(none) -> list
		Returns list of students who are possible patient zeros
		
		>>> print(contact_tracker.patient_zeros())
		[Bob (260808934), Farley (260675874), Larry (260386543)]

		>>> print(contact_tracker.patient_zeros())
		[Alice (260018288), Hanes (260041845), Illersley (260092533)]

		>>> print(contact_tracker.patient_zeros())
		[Piper (260055764), Sanaa (260025405), Hailee (260012075), Naima (260071927)]
		>>>
		"""
		patient_zero_list = []
		exposure_victims = self.collect_victims() #list of nested lists that represent every victim (exposed by another student)

		for student in ContactTracker.default_students:
			if student.is_sick == False: #patient_zero students are sick
				continue

			is_patient_zero = True #unless the student is found in the list of exposed victims, they are considered a patient zero
			for exposure_victims_groups in exposure_victims:
				if student.student_id in exposure_victims_groups:
					is_patient_zero = False 

			if is_patient_zero == True:
				patient_zero_list.append(student) #if is_patient_zero has remained true, student is appended to patient_zero_list

		return patient_zero_list

	def potential_sick_students(self):
		"""(none) -> list
		Returns list of students who might be sick because they appear in a sick student's contact list

		>>> print(contact_tracker.potential_sick_students())
		[Philip (260212160), Sarai (260758421)]

		>>> print(contact_tracker.potential_sick_students())
		[Lammle (260065208)]

		>>> print(contact_tracker.potential_sick_students())
		[Francesca (260032440), Ayla (260005925), Leonardo (260031356)]
		"""

		potential_sick_list = []
		exposure_victims = self.collect_victims()

		for student in ContactTracker.default_students:
			if student.is_sick == True: #potentially sick regards student.is_sick is False
				continue

			is_potential_sick = False
			for exposure_victims_groups in exposure_victims:
				if student.student_id in exposure_victims_groups:
					is_potential_sick = True #if student.is_sick is False but they are found in exposure_victims, they are considered potentially sick

			if is_potential_sick == True:
				potential_sick_list.append(student)

		return potential_sick_list


	def sick_from_another_student(self):
		"""(none) -> list
		Returns list of sick students who got sick from another student (appeared in a contact list of a stick student + is_sick)

		>>> print(contact_tracker.sick_from_another_student())
		[Carol (260996175), Leanne (260476020), Mark (260248711),
		Paul (260840155), Will (260561504), Zach (260970944)]


		>>> print(contact_tracker.sick_from_another_student())
		[Bob (260808934), Carol (260996175), Darryl (260084903), \
		Ettienne (260026473), Forbert (260072990), Gordie (260039118), Job (260013314), Kirk (260041812), Molly (260061737)]	

		>>> print(contact_tracker.sick_from_another_student())
		[Angelina (260095234), Rory (260092283), Danna (260068680), Reed (260010997), Jackson (260014616), Zara (260026754), Avah (260072488), \
		Anahi (260068501), Weston (260094691), Maddison (260031971), Brittany (260092902), Jasmine (260094997), Hadley (260064375)]
		"""

		sick_from_another_list = []
		exposure_victims = self.collect_victims()

		for student in ContactTracker.default_students:
			if student.is_sick == False: #regards students who are sick
				continue

			is_sick_from_another = False
			for exposure_victims_groups in exposure_victims:
				if student.student_id in exposure_victims_groups:
					is_sick_from_another = True #appended to sick_from_another_list if student.is_sick is True and they are found in exposure_victims

			if is_sick_from_another == True:
				sick_from_another_list.append(student)

		return sick_from_another_list


	def most_viral_students(self):
		"""(none) -> list
		Returns list of most viral students (students who contacted the largest amount of students)

		>>> print(contact_tracker.most_viral_students())
		[Bob (260808934)]

		>>> print(contact_tracker.most_viral_students())
		[Alice (260018288), Illersley (260092533)]

		>>> print(contact_tracker.most_viral_students())
		[Jackson (260014616), Zara (260026754), Rory (260092283)]
		"""

		cases_with_contacts_dict = self.cases_with_contacts
		most_viral_student_id_list = []

		most_contacts = 0
		for viral_student in cases_with_contacts_dict:
			if len(cases_with_contacts_dict[viral_student]) > most_contacts: #collects longest list of students who came in contact with a sick student
				most_contacts = len(self.cases_with_contacts[viral_student])

		for viral_student in cases_with_contacts_dict:
			if len(cases_with_contacts_dict[viral_student]) == most_contacts: #collects student ids who have contact list lengths of most_contacts
				most_viral_student_id_list.append(viral_student)

		most_viral_student_list = []
		for viral_student_id in most_viral_student_id_list: #mathces students ids to student objects in default list of students
			for student in ContactTracker.default_students:
				if viral_student_id == student.student_id:
						most_viral_student_list.append(student)
						break

		return most_viral_student_list

	def most_contacted_student(self):
		"""(none) -> list
		Returns list of students who have in contact with the most viral students

		>>> print(contact_tracker.most_contacted_student())
		[Philip (260212160)]

		>>> print(contact_tracker.most_contacted_student())
		[Lammle (260065208)]

		>>> print(contact_tracker.most_contacted_student())
		[Ayla (260005925)]
		"""
		cases_with_contacts_dict = self.cases_with_contacts
		exposure_victims = self.collect_victims()
		individual_exposed_victims = []

		for exposure_victims_groups in exposure_victims: #collects all contacts individually into a list (ids only appear once and are not sorted by spreader)
			for victim_id in exposure_victims_groups:
				if victim_id not in individual_exposed_victims:
					individual_exposed_victims.append(victim_id)

		number_of_times_contacted = {} #keys are student ids of those who have been in contact with a viral student, and the values represent the number of times they appeared in a contact list
		for victim in individual_exposed_victims:
			count = 0
			for viral_student in cases_with_contacts_dict:
				if victim in cases_with_contacts_dict[viral_student]:
					count += 1

			number_of_times_contacted[victim] = count

		most_times_contacted = 0
		for contacted_student in number_of_times_contacted: #collects maximum value in dictionary number_of_times_contacted
			if number_of_times_contacted[contacted_student] > most_times_contacted:
				most_times_contacted = number_of_times_contacted[contacted_student]

		most_contacted_student_id_list = [] #collects student ids that have been in contact with the most people
		for contacted_student in number_of_times_contacted:
			if number_of_times_contacted[contacted_student] == most_times_contacted:
				most_contacted_student_id_list.append(contacted_student)

		most_contacted_student_list = []
		for viral_student_id in most_contacted_student_id_list: #matches student ids in most_contacted_student_id_list to student objects in default list
			for student in ContactTracker.default_students:
				if student.student_id == viral_student_id:
					most_contacted_student_list.append(student)
					break

		return most_contacted_student_list

	def ultra_spreaders(self):
		"""(none) -> list
		Returns list of students who have only been in contact with potentially sick students

		>>> print(contact_tracker.ultra_spreaders())
		[Leanne (260476020), Zach (260970944)]

		>>> print(contact_tracker.ultra_spreaders())
		[Job (260013314), Darryl (260084903), Bob (260808934), Ettienne (260026473), Carol (260996175)]

		>>> print(contact_tracker.ultra_spreaders())
		[Hadley (260064375), Reed (260010997), Anahi (260068501)]
		"""

		ultra_spreaders_id_list = []
		cases_with_contacts_dict = self.cases_with_contacts

		for viral_student in cases_with_contacts_dict: #iterates through each spreader
			is_ultra_spreader = True
			for contacted_student in cases_with_contacts_dict[viral_student]: #iterates through each contact in the spreader's value
				for student in ContactTracker.default_students: #matches contact id to its respective Student object in default lsit
					if student.student_id == contacted_student:
						if student.is_sick == True: #since looking for ultra spreader, condition is_ultra_spreader is false if one of its contacts is already reported sick
							is_ultra_spreader = False
						break

			if is_ultra_spreader == True:
				ultra_spreaders_id_list.append(viral_student)

		ultra_spreaders_list = []
		for viral_student_id in ultra_spreaders_id_list: #matches student ids in ultra_spreaders_id_list to student objects in default list
			for student in ContactTracker.default_students:
				if student.student_id == viral_student_id:
					ultra_spreaders_list.append(student)
					break

		return ultra_spreaders_list


	def non_spreaders(self):
		"""(none) -> list
		Returns list students who are sick but only had contact with other sick students

		>>> print(contact_tracker.non_spreaders())
		[Bob (260808934), Carol (260996175), Farley (260675874), Larry (260386543),
		Paul (260840155), Will (260561504)]

		>>> print(contact_tracker.non_spreaders())
		[Alice (260018288), Hanes (260041845), Illersley (260092533), Forbert (260072990), Kirk (260041812), Molly (260061737), Gordie (260039118)]

		>>> print(contact_tracker.non_spreaders())
		[Jasmine (260094997), Naima (260071927), Jackson (260014616), Avah (260072488), Hailee (260012075), Sanaa (260025405), Piper (260055764), Angelina (260095234)]
		"""
		non_spreaders_id_list = []
		cases_with_contacts_dict = self.cases_with_contacts

		for viral_student in cases_with_contacts_dict: #iterates through each spreader
			is_non_spreader = True
			for contacted_student in cases_with_contacts_dict[viral_student]: #iterates through each contact in the spreader's value
				for student in ContactTracker.default_students: #matches contact id to tis respective Student object in default list
					if student.student_id == contacted_student:
						if student.is_sick == False: #since looking for non spreader, condistion is_non_spreader is False if one of its contacts hasn't been reported sick
							is_non_spreader = False
			if is_non_spreader == True:
				non_spreaders_id_list.append(viral_student)

		non_spreaders_list = []
		for viral_student_id in non_spreaders_id_list: #matches student ids in non_spreaders_id_list to student objects in default list
			for student in ContactTracker.default_students:
				if student.student_id == viral_student_id:
					non_spreaders_list.append(student)
					break

		return non_spreaders_list





















