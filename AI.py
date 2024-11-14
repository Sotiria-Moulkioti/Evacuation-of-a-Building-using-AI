import copy
import sys 
sys.setrecursionlimit(10**6) 
import heapq

# Δημιουργούμε τους τελεστές μετάβασης
def go_to_floor(state, floor):
    sum = 0
    #Υπολογίζουμε τους ορόφους που έχουν αδειάσει.
    for i in range(1,len(state)-1):
        if state[i] == 0:
            sum +=1
    # Ο τελεστής που πηγαίνει στην ταράτσα 
    # Αν έχει γεμίσει το ασανσέρ, τότε αναβαίνει στην ταράτσα και μηδενίζει το ασανσέρ
    if state[-1] == 8 and floor == len(state)-1:
        new_state = copy.deepcopy(state)
        new_state[-1] = 0
        new_state[0] = len(state)-1
        # Επιστρέφει την νέα κατάσταση που έχει προκύψει
        return new_state
    # Εφαρμόζουμε τους τελεστές και δημιουργούμε την νέα κατάσταση 
    # Με βάση την τιμή του floor δημιουργούμε τον αντίστοιχο τελεστή
    if state[-1] < 8 and state[floor] > 0 and floor != len(state)-1:
        # Κάνουμε την αντιγραφή της λίστας
        new_state = copy.deepcopy(state)
        # Αν τα άτομα που βρίσκονται στον όροφο είναι περισσότερα από την χωριτικότητα του ασανσέρ
        # τότε χρησιμοποιούμε τον τύπο state[floor] + state[-1] -8.
        if state[floor] > 8 - state[-1]:
            new_state[floor] = state[floor] + state[-1] -8
            new_state[0] = floor
            new_state[-1] = 8;
        # Αν δεν ικανοποείται ο παραπάνω έλεγχος, τότε εκτελούμε την πράξη  new_state[-1] = new_state[-1] + state[floor]
        else:
            new_state[-1] += state[floor]
            new_state[0] = floor
            new_state[floor] = 0
	 # Επιστρέφει την νέα κατάσταση που έχει προκύψει
        return new_state
    # Αν δεν έχει γεμίσει το ασανσέρ και οι όροφοι έχουν μηδενιστεί, τότε αναβαίνει στην ταράτσα και μηδενίζει το ασανσέρ
    if state[-1] != 8 and floor == len(state)-1:
        if sum == len(state)-2:
            new_state = copy.deepcopy(state)
            new_state[-1] = 0
            new_state[0] = len(state)-1
             # Επιστρέφει την νέα κατάσταση που έχει προκύψει
            return new_state
    # Αν δεν ισχύει κανένες από τους ελέγχους, τότε επιστρέφουμε None
    else:
        return None

# Με βάση την κατάσταση state, βρίσκουμε τις καταστάσεις-παιδία και τα αποθηκεύουμε στην λίστα children
def find_children(state):
    children=[]
    size_of_list = len(state)
    for i in range(size_of_list-1,0,-1):
        floor_state = copy.deepcopy(state)
        floor_child = go_to_floor(floor_state, i)

        if floor_child != None:
            children.append(floor_child)
    # Επιστρέφουμε τα παιδία της κατάστασης
    return children

# Βάζουμε την κατάσταση στο μέτωπο αναζήτησης
def make_front(state):
    return [state]

# Δημιουργούμε την ευριστική συνάρτηση    
def heuristic(state):
    temp = []
    # Το άθροισμα των ενοίκων που βρίσκονται στους ορόφους
    priority_sum = 0
    size_of_list = len(state)
    # Φτιάχνουμε την λίστα temp να έχει το ίδιο μέγεθος με την state
    # Το πρώτο στοιχείο και το τελευταίο είναι 0 της temp
    temp = [0] * size_of_list
    # Αντιγράφουμε τους ενοίκους στην λίστα temp
    for k in range(1,size_of_list-1):
        temp[k] = state[k]
    # Βρίσκουμε τις 2 μεγαλύτερες τιμές της temp
    max_val = heapq.nlargest(2, temp)
    for i in range(1,size_of_list-1):
        priority_sum += state[i]
    # Αθροίζουμε όλα τα στοιχεία της state
    general_sum = sum(state)
    # Αθροίζουμε το priority_sum, το general_sum και την δεύτερη μεγαλύτερη τιμή
    global_sum =  priority_sum + general_sum + max_val[1]
    # Πολλαπλασιάζουμε το global_sum με την πρώτη μεγαλύτερη τιμή
    Sum =  global_sum*max_val[0]
    return Sum

def expand_front(front, method):  
    if method=='DFS':        
        if front:
            print("Front:")
            print(front)
            # Βγάζουμε το πρώτο στοιχείο του μετώπου και βρίσκουμε τα παιδία του
            node=front.pop(0)
            # Βάζουμε τα παιδία στην αρχή του μετώπου
            for child in find_children(node):     
                front.insert(0,child)
    elif method=='BFS':
        if front:
            print("Front:")
            print(front)
            # Βγάζουμε το πρώτο στοιχείο του μετώπου και βρίσκουμε τα παιδία του
            node=front.pop(0)
             # Βάζουμε τα παιδία στο τέλος του μετώπου
            for child in find_children(node):     
                front.append(child) 
    elif method == 'BestFS':   
    	if front:
            print("Front:")
            print(front)
            # Βγάζουμε το πρώτο στοιχείο του μετώπου και βρίσκουμε τα παιδία του
            node=front.pop(0)
            children = find_children(node)
            # Βρίσκουμε τον αριθμό των παιδιών του 
            n =  sum(1 for child in find_children(node)) 
            if n > 1:  
                # Ταξινομούμε τα παιδία με βάση το ευριστικό κριτήριο                       
                children.sort(key=heuristic)
                # Βάζουμε τα παιδία στην αρχή του μετώπου
                for child in children:     
                    front.insert(0,child)
            else:
                # Βάζουμε τα παιδία στην αρχή του μετώπου
                for child in children:    
                    front.insert(0,child)  
    elif method == 'Hill-climbing':
        if front:
            print("Front:")
            print(front)
            # Βγάζουμε το πρώτο στοιχείο του μετώπου και βρίσκουμε τα παιδία του
            node=front.pop(0)
            children = find_children(node)
            # Βρίσκουμε τον αριθμό των παιδιών του 
            n =  sum(1 for child in find_children(node)) 
            if n > 1:  
                # Ταξινομούμε τα παιδία με βάση το ευριστικό κριτήριο                       
                children.sort(key=heuristic)
                child = children[-1]
                front.insert(0,child)
            else:
                # Βάζουμε τα παιδία στην αρχή του μετώπου
                for child in children:    
                    front.insert(0,child)
    else:
        print("It doesn't exist.")
        return
    # Επιστρέφουμε το μέτωπο 
    return front

# Βάζουμε την κατάσταση στην ούρα αναζήτησης
def make_queue(state):
    return [[state]]


def extend_queue(queue, method):
     #--LIFO
    if method=='DFS':
        print("Queue:")
        print(queue)
        # Βγάζουμε το πρώτο στοιχείο της ουράς 
        node=queue.pop(0)
        # Αντιγράφουμε το μονοπάτι
        queue_copy=copy.deepcopy(queue)
        # Βρίσκουμε τα παιδία του τελευταίου στοιχείου του node
        children=find_children(node[-1])
        for child in children:
            # Αντιγράφουμε την κατάσταση στο path
            path=copy.deepcopy(node)
            # Βάζουμε το κάθε παιδί στο τέλος του path
            path.append(child)
            # Βάζουμε το μονοπάτι στην αρχή της ουράς
            queue_copy.insert(0,path)
     #--FIFO
    elif method=='BFS':
        print("Queue:")
        print(queue)
        # Βγάζουμε το πρώτο στοιχείο της ουράς 
        node=queue.pop(0)
        # Αντιγράφουμε το μονοπάτι
        queue_copy=copy.deepcopy(queue)
        # Βρίσκουμε τα παιδία του τελευταίου στοιχείου του node
        children=find_children(node[-1])
        for child in children:
            # Αντιγράφουμε την κατάσταση στο path
            path=copy.deepcopy(node)
            # Βάζουμε το κάθε παιδί στο τέλος του path
            path.append(child)
            # Βάζουμε το μονοπάτι στο τέλος της ουράς
            queue_copy.append(path)     

    elif method == 'BestFS':
        print("Queue:")
        print(queue)
        # Βγάζουμε το πρώτο στοιχείο της ουράς 
        node=queue.pop(0)
        # Αντιγράφουμε το μονοπάτι
        queue_copy=copy.deepcopy(queue)
        # Βρίσκουμε τα παιδία του τελευταίου στοιχείου του node
        children=find_children(node[-1])
         # Βρίσκουμε τον αριθμό των παιδιών του 
        n =  sum(1 for child in find_children(node[-1]))
        if n > 1 :
            # Ταξινομούμε τα παιδία με βάση το ευριστικό κριτήριο    
            children.sort(key=heuristic)
            for child in children:
                # Αντιγράφουμε την κατάσταση στο path
                path=copy.deepcopy(node)
                # Βάζουμε το κάθε παιδί στο τέλος του path
                path.append(child)
                # Βάζουμε το μονοπάτι στην αρχή της ουράς
                queue_copy.insert(0,path)
        else: 
            for child in children:
                # Αντιγράφουμε την κατάσταση στο path
                path=copy.deepcopy(node)
                # Βάζουμε το κάθε παιδί στο τέλος του path
                path.append(child)
                # Βάζουμε το μονοπάτι στην αρχή της ουράς
                queue_copy.insert(0,path)
    elif method == 'Hill-climbing':
        print("Queue:")
        print(queue)
        # Βγάζουμε το πρώτο στοιχείο της ουράς 
        node=queue.pop(0)
        # Αντιγράφουμε το μονοπάτι
        queue_copy=copy.deepcopy(queue)
        # Βρίσκουμε τα παιδία του τελευταίου στοιχείου του node
        children=find_children(node[-1])
         # Βρίσκουμε τον αριθμό των παιδιών του 
        n =  sum(1 for child in find_children(node[-1]))
        if n > 1 : 
            children.sort(key=heuristic)
            child = children[-1]
            path=copy.deepcopy(node)
            path.append(child)
            queue_copy.insert(0,path)
        else: 
            for child in children:
                # Αντιγράφουμε την κατάσταση στο path
                path=copy.deepcopy(node)
                # Βάζουμε το κάθε παιδί στο τέλος του path
                path.append(child)
                # Βάζουμε το μονοπάτι στην αρχή της ουράς
                queue_copy.insert(0,path)
    else:
        print("It doesn't exist.")
        return
    # Επιστρέφουμε την ούρα 
    return queue_copy

# Βρίσκουμε την λύση του προβλήματος
def find_solution(front, queue, closed, goal, method):

    # Αν το μέτωπο είναι κενό δεν βρήκαμε λύση 
    if not front:
        print('_NO_SOLUTION_FOUND_')
    
    # Αν το πρώτο στοιχείο βρίσκεται στο κλειστό χώρο:
    elif front[0] in closed:
        # Αντιγράφουμε το front στο new_front
        new_front=copy.deepcopy(front)
        # Βγάζουμε το πρώτο στοιχείο 
        new_front.pop(0)
        # Αντιγράφουμε τηνqueue στη new_queue
        new_queue=copy.deepcopy(queue)
        # Βγάζουμε το πρώτο στοιχείο 
        new_queue.pop(0)
        # Εκτελούμε ξανά στην συνάρτηση
        find_solution(new_front, new_queue, closed, goal, method)
    # το πρώτο στοιχείο του front είναι ο στόχος, τότε βρήκαμε την λύση
    elif front[0]==goal:
        print('_GOAL_FOUND_')
        print(queue[0])
        
    else:
        # Βάζουμε το πρώτο στοιχείο του front στο closed
        closed.append(front[0])
        # Αντιγράφουμε το front στο front_copy
        front_copy=copy.deepcopy(front)
        # Επεκτείνουμε το μέτωπο (με βάση την μέθοδο): βρίσκουμε τα παιδία 
        front_children=expand_front(front_copy, method)
        # Επεκτείνουμε την ούρα (με βάση την μέθοδο): βρίσκουμε τα παιδία 
        queue_copy=copy.deepcopy(queue)
        queue_children=extend_queue(queue_copy, method)
        # Αντιγράφουμε το closed στο closed_copy
        closed_copy=copy.deepcopy(closed)
        # Εκτελούμε ξανά στην συνάρτηση
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
