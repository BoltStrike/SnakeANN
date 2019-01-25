import tensorflow as tf
from game import *
import keyboard
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.log_device_placement = True

sess = tf.Session(config = config)
set_session(sess)

from game import *
from keras.models import model_from_json

def run_game(model, display, clock):
	max_score = 3
	avg_score = 0
	games = 1000
	steps = 2000
	
	for _ in tqdm(range(games)):
		snake_start, snake_pos, apple_pos, score = starting_positions()
		if keyboard.is_pressed('q'):
				break
		
		count_same_dir = 0
		prev_dir = 0
		
		for _ in range(steps):
			current_dir_vect, front_block, left_block, right_block = blocked_directions(snake_pos)
			angle, snake_dir_vect, napple_dir_vect, nsnake_dir_vect = angle_with_apple(snake_pos, apple_pos)
			
			predictions = []
			
			predicted_direction = np.argmax(np.array(model.predict(
				np.array([left_block,front_block,right_block, napple_dir_vect[0], nsnake_dir_vect[0], napple_dir_vect[1], nsnake_dir_vect[1]]).reshape(-1,7))))-1
			
			
			if predicted_direction == prev_dir:
				count_same_dir += 1;
			else:
				count_same_dir = 0
				prev_dir = predicted_direction
		
			new_dir = np.array(snake_pos[0]) - np.array(snake_pos[1])
			if predicted_direction == -1:
				new_dir = np.array([new_dir[1], - new_dir[0]])
			if predicted_direction == 1:
				new_dir = np.array([-new_dir[1], new_dir[0]])
			
			button_dir = generate_button_direction(new_dir)
		
			next_step = snake_pos[0] + current_dir_vect
			if collision_with_boundaries(snake_pos[0]) == 1 or collision_with_self(next_step.tolist(), snake_pos) == 1:
				break
			
			snake_pos, apple_pos, score = play_game(snake_start, snake_pos, apple_pos, button_dir, score, display, clock)
		
			if score > max_score:
				max_score = score
			
		avg_score += score
	return max_score, avg_score/1000
	
json_file = open('model.json', 'r')
loaded_json_model = json_file.read()
model = model_from_json(loaded_json_model)
model.load_weights('model.h5')


display_width = 500
display_height = 500
pygame.init()
display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
max_score, avg_scor = run_game(model, display, clock)
print("Max score was ", max_score)
print("Avg score was ", avg_scor)
	