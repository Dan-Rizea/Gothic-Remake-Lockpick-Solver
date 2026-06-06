from collections import deque

# Puzzle bounds
MIN_POS = 0
MAX_POS = 6
TARGET_POS = 3  # The middle hole

def solve_slider_puzzle(initial_state, interactions):
    """
    Optimized BFS that treats continuous multi-unit drags as a single move,
    guaranteeing the absolute minimum number of slider interactions.
    """
    num_sliders = len(initial_state)
    target_state = tuple(TARGET_POS for _ in range(num_sliders))
    
    if initial_state == target_state:
        return []

    # Pre-compute base "deltas" for 1 step
    step_deltas = []
    for slider_idx in range(num_sliders):
        up_delta = []
        down_delta = []
        for affected_idx in range(num_sliders):
            effect = interactions.get(slider_idx, {}).get(affected_idx, 0)
            up_delta.append(effect)
            down_delta.append(-effect)
        step_deltas.append((tuple(up_delta), tuple(down_delta)))

    # visited maps state -> (previous_state, (slider_idx, net_move))
    visited = {initial_state: None}
    queue = deque([initial_state])

    while queue:
        current_state = queue.popleft()

        for slider_idx in range(num_sliders):
            for move_idx, direction in enumerate((1, -1)):
                delta = step_deltas[slider_idx][move_idx]
                
                # Explore dragging this slider as far as valid in this direction
                temp_state = list(current_state)
                steps_taken = 0
                
                while True:
                    is_valid_step = True
                    next_state_list = []
                    
                    for i in range(num_sliders):
                        val = temp_state[i] + delta[i]
                        if val < MIN_POS or val > MAX_POS:
                            is_valid_step = False
                            break
                        next_state_list.append(val)
                        
                    if not is_valid_step:
                        break # Bounds exceeded; cannot drag slider further
                        
                    steps_taken += 1
                    temp_state = next_state_list
                    new_state = tuple(temp_state)
                    
                    # If we haven't seen this state, record the ENTIRE drag as 1 move
                    if new_state not in visited:
                        visited[new_state] = (current_state, (slider_idx, direction * steps_taken))
                        
                        if new_state == target_state:
                            path = []
                            curr = new_state
                            while visited[curr] is not None:
                                prev_state, move = visited[curr]
                                path.append(move)
                                curr = prev_state
                            return path[::-1] 
                        
                        queue.append(new_state)

    return None

# ==========================================================
# CONFIGURATION AREA
# ==========================================================

if __name__ == "__main__":
    INITIAL_STATE = (4, 2, 5, 6, 1, 6) 

    FORWARD = 1
    BACKWARD = -1

    INTERACTIONS = {
        0: {0: FORWARD, 2: FORWARD, 5: BACKWARD},        
        1: {1: FORWARD},  
        2: {2: FORWARD, 0: FORWARD, 3: BACKWARD, 5: FORWARD},         
        3: {3: FORWARD, 4: FORWARD, 1: FORWARD, 5: BACKWARD},                
        4: {4: FORWARD},                
        5: {5: FORWARD, 2: BACKWARD}                
    }

    print("Searching for solution...")
    solution = solve_slider_puzzle(INITIAL_STATE, INTERACTIONS)

    if solution is not None:
        if not solution:
            print("\nThe puzzle is already solved!")
        else:
            total_clicks = sum(abs(move) for _, move in solution)
            
            print(f"\nSolution found! ({len(solution)} total slider interactions)")
            print("-" * 40)
            
            for step_num, (slider, net_move) in enumerate(solution, 1):
                dir_str = "Left" if net_move > 0 else "Right"
                print(f"Step {step_num}: Drag Slider {slider} {dir_str} by {abs(net_move)}")
                
            print("-" * 40)
            print(f"Total individual 1-unit clicks: {total_clicks}")
            
            print("\nAutomation complete!")
            
    else:
        print("\nNo solution found. Check your interaction matrix and initial state.")