import sys, pygame
pygame.init()

MOVING_PLATFORM = 0
MOVING_OBJECTS = 1
CHANGE = 1
size = width, height = 640, 480
black = 0, 0, 0
top_left = (0, 30)
top_right = (640, 30)
bottom_left = (0, 512)
bottom_right = (640, 512)

screen = pygame.display.set_mode(size)
surface = pygame.image.load("graphics/generic_platformer_tiles.png")
surface_rect = surface.get_rect()
ball = pygame.image.load("graphics/ania_small.gif")
ball_rect = ball.get_rect()


def is_inside(rect):
	#print(rect.top, rect.bottom, rect.left, rect.right)
	return True


mode = MOVING_PLATFORM
x_platform_change, y_platform_change = 0, 0
x_object_change, y_object_change = 0, 0

while True:
	# Moving around platform
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if mode == MOVING_PLATFORM:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_platform_change = CHANGE
				elif event.key == pygame.K_RIGHT:
					x_platform_change = -CHANGE
				elif event.key == pygame.K_UP:
					y_platform_change = CHANGE
				elif event.key == pygame.K_DOWN:
					y_platform_change = -CHANGE

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					x_platform_change -= CHANGE
				if event.key == pygame.K_RIGHT:
					x_platform_change += CHANGE
				if event.key == pygame.K_UP:
					y_platform_change -= CHANGE
				if event.key == pygame.K_DOWN:
					y_platform_change += CHANGE

		if event.type == pygame.KEYDOWN and event.key == pygame.K_i and mode == MOVING_PLATFORM:
			print("Changing mode to moving objects. Press esc to go back")
			mode = MOVING_OBJECTS

		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and mode == MOVING_OBJECTS:
			print("Changing mode to moving platform. Press i to move objects")
			mode = MOVING_PLATFORM

		if mode == MOVING_OBJECTS:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_object_change = -CHANGE
				elif event.key == pygame.K_RIGHT:
					x_object_change = CHANGE
				elif event.key == pygame.K_UP:
					y_object_change = -CHANGE
				elif event.key == pygame.K_DOWN:
					y_object_change = CHANGE

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					x_object_change += CHANGE
				if event.key == pygame.K_RIGHT:
					x_object_change -= CHANGE
				if event.key == pygame.K_UP:
					y_object_change += CHANGE
				if event.key == pygame.K_DOWN:
					y_object_change -= CHANGE



	new_surface_rect = surface_rect.move(x_platform_change, y_platform_change)
	if is_inside(new_surface_rect):
		surface_rect = new_surface_rect

	ball_rect = ball_rect.move(x_object_change, y_object_change)

	screen.fill(black)
	screen.blit(surface, surface_rect)
	screen.blit(ball, ball_rect)
	pygame.display.flip()
