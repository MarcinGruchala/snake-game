import pygame, sys, os, random
from pygame.locals import *
clear = lambda: os.system('cls')


class Snake:
	directions = ('up', 'down', 'left', 'right')
	def __init__(self):
		self.length = 7
		self.head_color = (204,0,0)
		self.body_color = (204,102,0)
		self.snake_body = [[4,5],[5,5],[6,5],[7,5],[8,5],[9,5],[10,5]]
		self.direction =  'left'
		self.back_direction = 'right'
		self.collision_status = False

	def  draw(self,surface):
		for body_part in range(self.length):
			if body_part == 0:
				pygame.draw.rect(surface,self.head_color,self.get_body_part_parameters(body_part))
			else:
				pygame.draw.rect(surface,self.body_color,self.get_body_part_parameters(body_part))

	def get_body_part_parameters(self,body_number):
		return (50+self.snake_body[body_number][0]*25,50+self.snake_body[body_number][1]*25,25,25)

	def get_snake_body(self):
		return self.snake_body

	def get_head_position(self):
		return self.snake_body[0]

	def change_direction(self, new_direction):
		if self.direction == 'up' and new_direction == 'down':
			return
		elif self.direction == 'down' and new_direction == 'up':
			return
		elif self.direction == 'left' and new_direction == 'right':
			return
		elif self.direction == 'right' and new_direction == 'left':
			return
		else:
			self.direction = new_direction

	def follow_back_direction(self):
		#check nex position of last block
		current_position = self.snake_body[-1]
		next_position = self.snake_body[-2]
		#difference on x axis
		if current_position[1] == next_position[1]:
			if current_position[0] < next_position[0]:
				self.back_direction = 'right'
			elif current_position[0] > next_position[0]:
				self.back_direction = 'left'
		#difference on y axis 
		elif current_position[0] == next_position[0]:
			if current_position[1] < next_position[1]:
				self.back_direction = 'down'
			elif current_position[1] > next_position[1]:
				self.back_direction = 'up'

	def move(self):
		self.collision_check()
		if self.collision_status == False:
			if self.direction == 'up':
				new_head_positon = [self.snake_body[0][0], self.snake_body[0][1]-1]
				for body_part in range(1,self.length):
					self.snake_body[-body_part] = self.snake_body[-(body_part+1)]
				self.snake_body[0] = new_head_positon

			elif self.direction == 'down':
				new_head_positon = [self.snake_body[0][0], self.snake_body[0][1]+1]
				for body_part in range(1,self.length):
					self.snake_body[-body_part] = self.snake_body[-(body_part+1)]
				self.snake_body[0] = new_head_positon

			elif self.direction == 'left':
				new_head_positon = [self.snake_body[0][0]-1, self.snake_body[0][1]]
				for body_part in range(1,self.length):
					self.snake_body[-body_part] = self.snake_body[-(body_part+1)]
				self.snake_body[0] = new_head_positon

			elif self.direction == 'right':
				new_head_positon = [self.snake_body[0][0]+1, self.snake_body[0][1]]
				for body_part in range(1,self.length):
					self.snake_body[-body_part] = self.snake_body[-(body_part+1)]
				self.snake_body[0] = new_head_positon

	def  next_head_position(self):
		if self.direction == 'up':
			return [self.snake_body[0][0],self.snake_body[0][1]-1]
		elif self.direction == 'down':
			return [self.snake_body[0][0],self.snake_body[0][1]+1]
		elif self.direction == 'left':
			return [self.snake_body[0][0]-1,self.snake_body[0][1]]
		elif self.direction == 'right':
			return [self.snake_body[0][0]+1,self.snake_body[0][1]]

	def collision_check(self):
		#snake collison:
		for body_part in self.snake_body:
			if self.next_head_position() ==  body_part:
				self.collision_status = True
				return 
			else:
				self.collision_status = False
		#board collison:
		#x axis c0llison 
		if self.next_head_position()[0] < 0 or self.next_head_position()[0]>19:
			self.collision_status = True
			return
		#y axis collison
		elif self.next_head_position()[1] < 0 or self.next_head_position()[1] > 19:
			self.collision_status = True
			return
		else:
			self.collision_status = False

	def add_body_part(self):
		if self.back_direction == 'up':
			self.snake_body.append([self.snake_body[-1][0],self.snake_body[-1][1]+1])
		elif self.back_direction == 'down':
			self.snake_body.append([self.snake_body[-1][0],self.snake_body[-1][1]-1])
		elif self.back_direction == 'left':
			self.snake_body.append([self.snake_body[-1][0]+1,self.snake_body[-1][1]])
		elif self.back_direction == 'right':
			self.snake_body.append([self.snake_body[-1][0]-1,self.snake_body[-1][1]])

	def eat(self):
		self.length+=1
		self.add_body_part()
		
class Food:
	def __init__(self):
		self.color = (153,0,153)
		self.position = [9,9]
		#self.eaten = False

	def get_parameters(self):
		return (50 + self.position[0]*25, 50 + self.position[1]*25,25,25)

	def  get_position(self):
		return self.position

	def draw(self,surface):
		pygame.draw.rect(surface, self.color, self.get_parameters())

	def eat(self,board):
		new_food_position = None
		while True:
			new_food_position = [random.randint(0,19),random.randint(0,19)]
			if board[new_food_position[1]][new_food_position[0]] == 0:
				break
		self.position = new_food_position


class Game_driver:
	def __init__(self):
		pygame.init()
		self.FPS_value = 5
		self.FPS = pygame.time.Clock()

		self.frame_color = (51,102,0)
		self.surface = pygame.display.set_mode((600,600))
		self.surface.fill(self.frame_color)
		pygame.display.set_caption("Snake")

		self.snake = Snake()
		self.food = Food()

		rows, cols = (20,20)
		self.board = [[0 for i in range(cols)] for j in range(rows)]
		
		self.change_direction_queue = []
		self.score = 0
		self.is_over = False
	
	def handle_event(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					self.change_direction_queue.append('up')
				elif event.key == pygame.K_DOWN:
					self.change_direction_queue.append('down')
				elif event.key == pygame.K_LEFT:
					self.change_direction_queue.append('left')
				elif event.key == pygame.K_RIGHT:
					self.change_direction_queue.append('right')

	def handle_movement(self):
		if len(self.change_direction_queue) != 0:
			for direction in self.change_direction_queue:
				self.snake.change_direction(direction)
				self.snake.move()
			self.change_direction_queue.clear()
		else:
			self.snake.move()

		self.snake.follow_back_direction()
		self.board_update()

	def handle_eating(self):
		if self.snake.get_head_position() == self.food.get_position():
			self.snake.eat()
			self.food.eat(self.board)
			self.board_update()
			self.score+=1

	def handle_rendering(self):
		if self.snake.collision_status == True:
			self.game_over_render()
			pygame.display.update()
		else:
			self.surface.fill(self.frame_color)
			#pygame.draw.rect(DISPLAYSURF,(0,153,0),(50,50,500,500))
			self.draw_board()
			self.snake.draw(self.surface)
			self.food.draw(self.surface)
			self.put_score()
			pygame.display.update()
			self.FPS.tick(self.FPS_value)

	def handle_game_over(self):
		if self.snake.collision_status == True:
			self.is_over = True
			while True:
				self.handle_event()
				self.game_over_render()
				pygame.display.update()


	def draw_board(self):
		green1 = (100,153,0)
		green2 = (50,153,0)
		for i in range(20):
			for j in range(20):
				if j%2==0:
					if i%2==0:
						pygame.draw.rect(self.surface,green1,(50+i*25,50+j*25,25,25))
					else:
						pygame.draw.rect(self.surface,green2,(50+i*25,50+j*25,25,25))
				else:
					if i%2==0:
						pygame.draw.rect(self.surface,green2,(50+i*25,50+j*25,25,25))
					else:
						pygame.draw.rect(self.surface,green1,(50+i*25,50+j*25,25,25))

	def board_update(self):
		for row in self.board:
			for index in range(len(row)):
				row[index] = 0
	
		for body_part in self.snake.get_snake_body():
			self.board[body_part[1]][body_part[0]] = 1 

		self.board[self.food.get_position()[1]][self.food.get_position()[0]] = 2
		

	def game_over_render(self):
		#background
		pygame.draw.rect(self.surface,(0,0,0),(150,150,300,300))
		#writing
		font = pygame.font.SysFont("comicsansms", 42)
		text = font.render("Game Over",True,(255,0,0))
		self.surface.blit(text,(190,160))

		score_text = font.render(f"Score: {self.score}", True,(255,0,0))
		self.surface.blit(score_text,(190,210))

	def put_score(self):
		font = pygame.font.SysFont("comicsansms", 20)
		text = font.render(f"Score: {self.score}",True,(255,255,255))
		self.surface.blit(text,(10,10))

	def log(self):
		print(f"Snake length: {self.snake.length}")
		print(f"Snake head:{self.snake.get_head_position()}")
		print(f"Snake body: {self.snake.snake_body}")
		print(f"Food:{self.food.get_position()}")
		print(f"Collision status: {self.snake.collision_status}")
		for row in self.board:
			print(row)


def main():
	
	game = Game_driver()

	
	game.board_update()
	game.handle_rendering()
	#game loop
	while True:
		clear()
		
		game.handle_event()
								
		game.handle_movement()
		game.handle_game_over()

		game.handle_eating()

		game.handle_rendering()


if __name__ == '__main__':
	main()