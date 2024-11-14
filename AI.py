import copy
import sys 
sys.setrecursionlimit(10**6) 
import heapq

# Create the transition operators
def go_to_floor(state, floor):
    sum = 0
    # Calculate the floors that have emptied.
    for i in range(1, len(state)-1):
        if state[i] == 0:
            sum += 1
    # The operator that goes to the rooftop
    # If the elevator is full, it ascends to the rooftop and empties
    if state[-1] == 8 and floor == len(state)-1:
        new_state = copy.deepcopy(state)
        new_state[-1] = 0
        new_state[0] = len(state)-1
        # Return the new state that has resulted
        return new_state
    # Apply the operators and create the new state 
    # Based on the floor value, create the corresponding operator
    if state[-1] < 8 and state[floor] > 0 and floor != len(state)-1:
        # Copy the list
        new_state = copy.deepcopy(state)
        # If the people on the floor exceed the elevator capacity
        # then we use the formula state[floor] + state[-1] -8.
        if state[floor] > 8 - state[-1]:
            new_state[floor] = state[floor] + state[-1] - 8
            new_state[0] = floor
            new_state[-1] = 8
        # If the above condition is not satisfied, execute new_state[-1] = new_state[-1] + state[floor]
        else:
            new_state[-1] += state[floor]
            new_state[0] = floor
            new_state[floor] = 0
        # Return the new state that has resulted
        return new_state
    # If the elevator isn’t full and floors are emptied, it ascends to the rooftop and empties
    if state[-1] != 8 and floor == len(state)-1:
        if sum == len(state)-2:
            new_state = copy.deepcopy(state)
            new_state[-1] = 0
            new_state[0] = len(state)-1
            # Return the new state that has resulted
            return new_state
    # If none of the checks are met, return None
    else:
        return None

# Based on the state, find child states and store them in the children list
def find_children(state):
    children = []
    size_of_list = len(state)
    for i in range(size_of_list-1, 0, -1):
        floor_state = copy.deepcopy(state)
        floor_child = go_to_floor(floor_state, i)

        if floor_child != None:
            children.append(floor_child)
    # Return the children of the state
    return children

# Put the state in the search front
def make_front(state):
    return [state]

# Create the heuristic function
def heuristic(state):
    temp = []
    # Sum of tenants on the floors
    priority_sum = 0
    size_of_list = len(state)
    # Create temp list of same size as state
    temp = [0] * size_of_list
    # Copy tenants to temp
    for k in range(1, size_of_list-1):
        temp[k] = state[k]
    # Find the 2 largest values in temp
    max_val = heapq.nlargest(2, temp)
    for i in range(1, size_of_list-1):
        priority_sum += state[i]
    # Sum all elements in state
    general_sum = sum(state)
    # Sum priority_sum, general_sum, and the second largest value
    global_sum =  priority_sum + general_sum + max_val[1]
    # Multiply global_sum by the largest value
    Sum =  global_sum * max_val[0]
    return Sum

# Expand the front based on the selected method
def expand_front(front, method):  
    if method == 'DFS':        
        if front:
            print("Front:")
            print(front)
            # Remove the first element from the front and find its children
            node = front.pop(0)
            # Insert children at the beginning of the front
            for child in find_children(node):     
                front.insert(0, child)
    elif method == 'BFS':
        if front:
            print("Front:")
            print(front)
            # Remove the first element from the front and find its children
            node = front.pop(0)
            # Append children to the end of the front
            for child in find_children(node):     
                front.append(child) 
    elif method == 'BestFS':   
        if front:
            print("Front:")
            print(front)
            # Remove the first element from the front and find its children
            node = front.pop(0)
            children = find_children(node)
            # Find the number of children 
            n =  sum(1 for child in find_children(node)) 
            if n > 1:  
                # Sort children based on the heuristic value                    
                children.sort(key=heuristic)
                # Insert children at the beginning of the front
                for child in children:     
                    front.insert(0, child)
            else:
                # Insert children at the beginning of the front
                for child in children:    
                    front.insert(0, child)  
    elif method == 'Hill-climbing':
        if front:
            print("Front:")
            print(front)
            # Remove the first element from the front and find its children
            node = front.pop(0)
            children = find_children(node)
            # Find the number of children 
            n =  sum(1 for child in find_children(node)) 
            if n > 1:  
                # Sort children based on the heuristic value                    
                children.sort(key=heuristic)
                child = children[-1]
                front.insert(0, child)
            else:
                # Insert children at the beginning of the front
                for child in children:    
                    front.insert(0, child)
    else:
        print("It doesn't exist.")
        return
    # Return the front 
    return front

# Place the state in the search queue
def make_queue(state):
    return [[state]]


def extend_queue(queue, method):
     #--LIFO
    if method == 'DFS':
        print("Queue:")
        print(queue)
        # Remove the first element from the queue 
        node = queue.pop(0)
        # Copy the path
        queue_copy = copy.deepcopy(queue)
        # Find children of the last element in the node
        children = find_children(node[-1])
        for child in children:
            # Copy the state to path
            path = copy.deepcopy(node)
            # Append each child to the end of the path
            path.append(child)
            # Insert path at the beginning of the queue
            queue_copy.insert(0, path)
     #--FIFO
    elif method == 'BFS':
        print("Queue:")
        print(queue)
        # Remove the first element from the queue 
        node = queue.pop(0)
        # Copy the path
        queue_copy = copy.deepcopy(queue)
        # Find children of the last element in the node
        children = find_children(node[-1])
        for child in children:
            # Copy the state to path
            path = copy.deepcopy(node)
            # Append each child to the end of the path
            path.append(child)
            # Append path to the end of the queue
            queue_copy.append(path)     

    elif method == 'BestFS':
        print("Queue:")
        print(queue)
        # Remove the first element from the queue 
        node = queue.pop(0)
        # Copy the path
        queue_copy = copy.deepcopy(queue)
        # Find children of the last element in the node
        children = find_children(node[-1])
        # Find the number of children 
        n =  sum(1 for child in find_children(node[-1]))
        if n > 1 :
            # Sort children based on heuristic    
            children.sort(key=heuristic)
            for child in children:
                # Copy the state to path
                path = copy.deepcopy(node)
                # Append each child to the end of the path
                path.append(child)
                # Insert path at the beginning of the queue
                queue_copy.insert(0, path)
        else: 
            for child in children:
                # Copy the state to path
                path = copy.deepcopy(node)
                # Append each child to the end of the path
                path.append(child)
                # Insert path at the beginning of the queue
                queue_copy.insert(0, path)
    elif method == 'Hill-climbing':
        print("Queue:")
        print(queue)
        # Remove the first element from the queue 
        node = queue.pop(0)
        # Copy the path
        queue_copy = copy.deepcopy(queue)
        # Find children of the last element in the node
        children = find_children(node[-1])
        # Find the number of children 
        n =  sum(1 for child in find_children(node[-1]))
        if n > 1 : 
            children.sort(key=heuristic)
            child = children[-1]
            path = copy.deepcopy(node)
            path.append(child)
            queue_copy.insert(0, path)
        else: 
            for child in children:
                # Copy the state to path
                path = copy.deepcopy(node)
                # Append each child to the end of the path
                path.append(child)
                # Insert path at the beginning of the queue
                queue_copy.insert(0, path)
    else:
        print("It doesn't exist.")
        return
    return queue_copy

# We find the solution to the problem
def find_solution(front, queue, closed, goal, method):

    # If the front is empty, we did not find a solution
    if not front:
        print('_NO_SOLUTION_FOUND_')
    
    # If the first element is in the closed list:
    elif front[0] in closed:
        # Copy front to new_front
        new_front = copy.deepcopy(front)
        # Remove the first element
        new_front.pop(0)
        # Copy queue to new_queue
        new_queue = copy.deepcopy(queue)
        # Remove the first element
        new_queue.pop(0)
        # Recursively call the function
        find_solution(new_front, new_queue, closed, goal, method)
    
    # If the first element of front is the goal, then we found the solution
    elif front[0] == goal:
        print('_GOAL_FOUND_')
        print(queue[0])
        
    else:
        # Add the first element of front to closed
        closed.append(front[0])
        # Copy front to front_copy
        front_copy = copy.deepcopy(front)
        # Expand the front (based on the method): find children 
        front_children = expand_front(front_copy, method)
        # Expand the queue (based on the method): find children 
        queue_copy = copy.deepcopy(queue)
        queue_children = extend_queue(queue_copy, method)
        # Copy closed to closed_copy
        closed_copy = copy.deepcopy(closed)
        # Recursively call the function
        find_solution(front_children, queue_children, closed_copy, goal, method)
           
def main():
    
    initial_state = [0, 9, 4, 12, 7, 0]
    goal = [5, 0, 0, 0, 0, 0]
   
    try:
        method = input("Enter which method you want to use (BFS, DFS, BestFS, Hill-climbing): ")
    except KeyboardInterrupt:
        print("\nProgram interrupted by the user. Exiting.")
        exit()
    print(method)
    
    print('____BEGIN__SEARCHING____')
    find_solution(make_front(initial_state), make_queue(initial_state), [], goal, method)

if __name__ == "__main__":
    main()

