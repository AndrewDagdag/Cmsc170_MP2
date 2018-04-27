import random

### VARIABLE ORDERING FUNCTIONS ###

def first_unassigned(state):
	problem = state.problem
	solution = state.solution

	unassigned_vars = problem.unassigned_variables(solution)	
	return unassigned_vars[0]

def random_unassigned(state):
	problem = state.problem
	solution = state.solution

	unassigned_vars = problem.unassigned_variables(solution)	
	return random.choice(unassigned_vars)

def custom_variable_selector(state):
	problem = state.problem
	solution = state.solution
	domain = state.domain

	# INSERT CODE HERE
	# Write your variable ordering code here 
	# Return an unassigned variable

	unassigned_var = first_unassigned(state)
	unassigned_vars = problem.unassigned_variables(solution)
	constraints = problem.constraints

	constraint_dict = dict()

	for un_var in unassigned_vars:
		cntr = 0
		for constraint in constraints:
			for const_var in constraint.variables:
				if const_var!=un_var and const_var in unassigned_vars:
					cntr += 1
				constraint_dict[const_var] = cntr

	for variable in unassigned_vars:
		var_cntr = unassigned_var_cntr = 0
		# MRV, if the length of the domain values of the variable
		# is less than that of the unassigned variable, select the variable
		if len(domain[variable]) < len(domain[unassigned_var]):
			unassigned_var = variable
		# DH
		elif len(domain[variable]) == len(domain[unassigned_var]):
			if constraint_dict[variable] >= constraint_dict[unassigned_var]:
				unassigned_var = variable

	return unassigned_var
	
	# Suggestions: 
	# Heuristic 1: minimum remaining values = select variables with fewer values left in domain
	# Heuristic 2: degree heuristic = select variables related to more constraints
	# Can use just one heuristic, or chain together heuristics (tie-break)

### VALUE ORDERING FUNCTIONS ###

def default_order(state,variable):
	problem = state.problem
	domain = state.domain[variable]

	values = domain
	return values # return as-is

def random_order(state,variable):
	problem = state.problem
	domain = state.domain[variable]

	values = domain[:] # make copy
	random.shuffle(values)
	return values

def custom_value_ordering(state,variable):
	problem = state.problem
	domain = state.domain[variable]

	# INSERT CODE HERE
	# Write your value ordering code here 
	# Return sorted values, accdg. to some heuristic
	
	state_domain = state.domain
	temp_dict = dict()
	
	new_domain_lengths = []
	return_val = []
	
	domainLength = len(domain)

	if domainLength != 0:
		for domain_val in domain:
			new_domain_length = 0

			new_state = state.copy()
			new_state.assign(variable, domain_val)
			forward_checking(new_state, variable)

			new_state_domain = new_state.domain
			for var in new_state_domain.items():
				new_domain_length = new_domain_length + len(var[1])

			temp_dict[domain_val] = new_domain_length
		
		sorted_dict = sorted(temp_dict.items(), key=lambda x: x[1], reverse=True)
		
		for val in sorted_dict:
			return_val.append(val[0])
		
		return return_val
	else:
		return random_order(state, variable)

	# Suggestions:
	# Heuristic: least constraining value (LCV)
	# LCV = prioritize values that filter out fewer values in other variables' domains
	# Hint: you will use state.copy() for new_state, use new_state.assign, and use forward_checking() on new_state
	# Count the number of filtered values by comparing the total from current state and new_state

### FILTERING FUNCTIONS ###

def do_nothing(state,variable):
	problem = state.problem
	return # do nothing

def forward_checking(state,variable):
	problem = state.problem
	solution = state.solution

	for constraint in problem.constraints:
		if variable not in constraint.variables:
			continue # skip if unrelated to variable

		for other_var in constraint.variables:
			if other_var == variable: continue # skip self
			if other_var in solution: continue # skip assigned 

			valid_values = []
			for value in state.domain[other_var]:
				new_solution = solution.copy()
				new_solution[other_var] = value 

				pass_test = constraint.test(new_solution)
				if pass_test:
					valid_values.append(value)

			state.domain[other_var] = valid_values

