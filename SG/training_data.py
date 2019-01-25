from game import *
import keyboard

def generate_training_data(display, clock):
	training_data_x = []
	training_data_y = []
	games = 2000
	steps = 8000
	
	for _ in tqdm(range(games)):
		snake_start, snake_pos, apple_pos, score = starting_positions()
		prev_apple_distance = apple_distance_from_snake(apple_pos, snake_pos)
		
		if keyboard.is_pressed('q'):
				break
		
		for _ in range(steps):
			angle, snake_dir_vect, napple_dir_vect, nsnake_dir_vect = angle_with_apple(snake_pos, apple_pos)
			dir, button_dir = generate_random_direction(snake_pos, angle)
			current_dir_vect, front_block, left_block, right_block = blocked_directions(snake_pos)
			
			dir, button_dir, training_data_y = generate_y_data(snake_pos, angle, button_dir, dir, training_data_y, front_block, left_block, right_block)
			
			if keyboard.is_pressed('q'):
				break
			
			if front_block == 1 and left_block == 1 and right_block == 1:
				break
				
			training_data_x.append(
				[left_block, front_block, right_block, napple_dir_vect[0], nsnake_dir_vect[0], napple_dir_vect[1], nsnake_dir_vect[1]])
				
			snake_pos, apple_pos, score = play_game(snake_start, snake_pos, apple_pos, button_dir, score, display, clock)
			
	return training_data_x, training_data_y

def generate_y_data(snake_pos, angle_w_apple, button_dir, dir, training_data_y, front_block, left_block, right_block):
	if dir == -1:
		if left_block == 1:
			if front_block == 1 and right_block == 0:
				dir, button_dir = direction_vector(snake_pos, angle_w_apple, 1)
				training_data_y.append([0,0,1])
			elif front_block == 0 and right_block == 1:
				dir, button_dir = direction_vector(snake_pos, angle_w_apple, 0)
				training_data_y.append([0,1,0])
			elif front_block == 0 and right_block == 0:
				dir, button_dir = direction_vector(snake_pos, angle_w_apple, 1)
				training_data_y.append([0,0,1])
		else:
			training_data_y.append([1,0,0])
			
	elif dir == 0:
		if front_block == 1:
			if left_block == 1 and right_block == 0:
				dir, button_dir = direction_vector(snake_pos, angle_w_apple, 1)
				training_data_y.append([0,0,1])
			elif left_block == 0 and right_block == 1: 
				dir, button_dir = direction_vector(snake_pos, angle_w_apple, -1)
				training_data_y.append([1,0,0])
			elif left_block == 0 and right_block == 0:
				dir, button_dir = direction_vector(snake_pos, angle_w_apple, 1)
				training_data_y.append([1,0,0])
		else:
			training_data_y.append([0,1,0])
	else:
		if right_block == 1:
			if left_block == 1 and front_block == 0:
				dir, button_dir = direction_vector(snake_pos, angle_w_apple, 0)
				training_data_y.append([0, 1, 0])
			elif left_block == 0 and front_block == 1:
				dir, button_dir = direction_vector(snake_pos,angle_w_apple, -1)
				training_data_y.append([1, 0, 0])
			elif left_block == 0 and front_block == 0:
				dir, button_dir = direction_vector(snake_pos,angle_w_apple,-1)
				training_data_y.append([1,0,0])
		else:
			training_data_y.append([0,0,1])
			
	return dir, button_dir, training_data_y
	
