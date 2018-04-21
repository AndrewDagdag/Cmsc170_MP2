def maxone_fitness(state,feasibility_minimum):
	""" Fitness = no. of 1s """
	solution = state.solution
	score = sum(solution.values())
	# always add feasibility_minimum, since there are no constraints
	return feasibility_minimum + score

def knapsack_fitness(state,feasibility_minimum):
	problem = state.problem
	solution = state.solution

	if problem.find_hard_violation(solution) is not None: 
		# has violation: total weight exceeds capacity
		max_score = int(feasibility_minimum * 0.75)

		# INSERT CODE HERE
		# Idea: less excess weight = higher score
		# Hint: use item.weight, problem.capacity

		total_weight = 0
		for item, present in solution.items():
			if present:
				total_weight += item.weight

		return max_score - max(0, total_weight - problem.capacity)
	else:
		# no violations
		score = feasibility_minimum # min score for being valid solution

		# INSERT CODE HERE
		# Idea: higher total item value = higher score
		# Hint: use item.value

		for item, present in solution.items():
			if present:
				score += item.value
		return score

def vertex_cover_fitness(state,feasibility_minimum):
	problem = state.problem
	solution = state.solution

	if problem.find_hard_violation(solution) is not None: 
		# has violation: some edges are not covered
		max_score = int(feasibility_minimum * 0.75)
		used_vertices = [v for v in problem.variables if solution[v] == 1]

		# INSERT CODE HERE
		# Idea: less uncovered edges = higher score
		# Hint: use problem.edges, used_vertices

		# edges for which no vertex in used_vertices is a substring
		uncovered = [e for e in problem.edges if not any(v in e for v in used_vertices)]
		return max_score - len(uncovered)
	else:
		# no violations
		score = feasibility_minimum # min score for being valid solution

		# INSERT CODE HERE
		# Idea: less vertices used = better
		# So, higher no. of unused vertices in solution = higher score

		unused_vertices = [v for v in problem.variables if solution[v] == 0]
		return score + len(unused_vertices)
