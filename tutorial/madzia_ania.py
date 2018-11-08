import sys, pygame
pygame.init()

MOVING_PLATFORM = 0
MOVING_OBJECTS = 1
MOVING_MADZIA = 2
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
ania = pygame.image.load("graphics/ania_small.gif")
ania_rect = ania.get_rect()
madzia = pygame.image.load("graphics/madzia_small.png")
madzia_rect = madzia.get_rect()


def is_inside(rect):
	#print(rect.top, rect.bottom, rect.left, rect.right)
	return True


mode = MOVING_PLATFORM
x_platform_change, y_platform_change = 0, 0
x_object_change, y_object_change = 0, 0
x_madzia_change, y_madzia_change = 0, 0

def move(event, x_change, y_change):
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_LEFT:
			x_change = CHANGE
		elif event.key == pygame.K_RIGHT:
			x_change = -CHANGE
		elif event.key == pygame.K_UP:
			y_change = CHANGE
		elif event.key == pygame.K_DOWN:
			y_change = -CHANGE

	if event.type == pygame.KEYUP:
		if event.key == pygame.K_LEFT:
			x_change -= CHANGE if x_change > -CHANGE else 0
		if event.key == pygame.K_RIGHT:
			x_change += CHANGE if x_change < CHANGE else 0
		if event.key == pygame.K_UP:
			y_change -= CHANGE if y_change > -CHANGE else 0
		if event.key == pygame.K_DOWN:
			y_change += CHANGE if y_change < CHANGE else 0
	return x_change, y_change


while True:
	# Moving around platform
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN and event.key == pygame.K_i and mode != MOVING_OBJECTS:
			print("Changing mode to moving Ania. Press esc to go back")
			mode = MOVING_OBJECTS

		if event.type == pygame.KEYDOWN and event.key == pygame.K_m and mode != MOVING_MADZIA:
			print("Changing mode to moving Madzia. Press esc to go back")
			mode = MOVING_MADZIA

		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and mode != MOVING_PLATFORM:
			print("Changing mode to moving platform. Press i to move objects")
			mode = MOVING_PLATFORM

		if mode == MOVING_PLATFORM:
			x_platform_change, y_platform_change = move(event, x_platform_change, y_platform_change)

		if mode == MOVING_OBJECTS:
			x_object_change, y_object_change = move(event, x_object_change, y_object_change)

		if mode == MOVING_MADZIA:
			x_madzia_change, y_madzia_change = move(event, x_madzia_change, y_madzia_change)

	surface_rect = surface_rect.move(x_platform_change, y_platform_change)
	ania_rect = ania_rect.move(x_object_change, y_object_change)
	madzia_rect = madzia_rect.move(x_madzia_change, y_madzia_change)

	screen.fill(black)
	screen.blit(surface, surface_rect)
	screen.blit(ania, ania_rect)
	screen.blit(madzia, madzia_rect)
	pygame.display.flip()
