### GENERIC OBJECTIVE FUNCTIONS ###

def count_violations(state):
	""" Count no. of violated constraints """
	problem = state.problem
	solution = state.solution

	count = 0
	for constraint in problem.constraints:
		pass_test = constraint.test(solution)
		if not pass_test:
			count += 1
	return count

def count_violators(state):
	""" Count no. of variables involved in violated constraints """
	problem = state.problem
	solution = state.solution

	violators = []
	for constraint in problem.constraints:
		pass_test = constraint.test(solution)
		if not pass_test:
			violators += constraint.variables
	return len(set(violators))

### SPECIFIC OBJECTIVE FUNCTIONS ###

def maxone_objective(state):
	""" Count no. of 1s """
	problem = state.problem
	solution = state.solution

	count = 0
	for var in problem.variables:
		count += solution[var] # 0 or 1
	return count

def knapsack_objective(state): 
	""" Total value of items inside knapsack based on solution """
	problem = state.problem
	solution = state.solution

	# INSERT CODE HERE
	# If solution violates hard constraint, score should be 0 (invalid) -- worst score for max
	# Hint: use problem.find_hard_violation
	# Compute total value of items included in knapsack based on the solution

	violation = problem.find_hard_violation(solution)
	if violation is not None:
		return 0

	value = 0
	for item, taken in solution.items():
		if taken:
			value += item.value
	return value


def vertex_cover_objective(state): 
	""" Number of vertices used in solution """
	problem = state.problem
	solution = state.solution 

	# INSERT CODE HERE
	# If solution violates hard constraint, score should be infinity (invalid) -- worst score for min
	# Hint: use problem.find_hard_violation
	# Count vertices included in the solution

	violation = problem.find_hard_violation(solution)
	if violation is not None:
		return float('inf')

	included = 0
	for vertex, state in solution.items():
		if state == 1:
			included += 1
	return included
