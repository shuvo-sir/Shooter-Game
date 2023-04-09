import pygame, sys 
from random import randint, uniform


 

def laser_update(laser_list, speed = 300):
	for rect in laser_list:
		rect.y -= speed * dt 
		if rect.bottom < 0:
			laser_list.remove(rect)



def meteor_update(meteor_list, speed = 300):
	for meteor_tuple in meteor_list:

		direction = meteor_tuple[1]
		meteor_rect = meteor_tuple[0]
		meteor_rect.center +=  direction * speed * dt
		if meteor_rect.top > WINDOW_HEIGTH:
			meteor_list.remove(meteor_tuple)



def display_score():
	score_text = f"Score: {pygame.time.get_ticks() // 1000}"
	text_surf = font.render(score_text, True, ("white"))
	text_rect = text_surf.get_rect(midbottom = (WINDOW_WITH / 2, WINDOW_HEIGTH - 80))
	display_surface.blit(text_surf, text_rect)
	pygame.draw.rect(display_surface,(255,255,255),text_rect.inflate(22,22), width = 3, border_radius = 5)



def laser_timer(can_shoot, duration = 500):
	if not can_shoot:
		current_time = pygame.time.get_ticks()
		if current_time - shoot_time > duration:
			can_shoot = True
	return can_shoot		



# game init
pygame.init()
WINDOW_WITH, WINDOW_HEIGTH = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WITH,WINDOW_HEIGTH))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()


# ship import 
ship_surf = pygame.image.load("C:/Users/Shuvo/Documents/Python/Shooter Game/graphics/ship.png").convert_alpha()
ship_rect = ship_surf.get_rect(center = (WINDOW_WITH / 2, WINDOW_HEIGTH / 2))

# background 
bg_surf = pygame.image.load("C:/Users/Shuvo/Documents/Python/Shooter Game/graphics/background.png").convert()


# laser import
laser_surf = pygame.image.load("C:/Users/Shuvo/Documents/Python/Shooter Game/graphics/laser.png")
laser_list = []



# laser time 
can_shoot = True
shoot_time = None



# import text
font = pygame.font.Font("C:/Users/Shuvo/Documents/Python/Shooter Game/graphics/subatomic.ttf",30)



# import meteor surface 
meteor_surf = pygame.image.load("C:/Users/Shuvo/Documents/Python/Shooter Game/graphics/meteor.png").convert_alpha()
meteor_list = []




# meteor timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer,500)



# import sound 
laser_sound = pygame.mixer.Sound("C:/Users/Shuvo/Documents/Python/Shooter Game/sounds/laser.ogg")
explosion_sound = pygame.mixer.Sound("C:/Users/Shuvo/Documents/Python/Shooter Game/sounds/explosion.wav")
background_music = pygame.mixer.Sound("C:/Users/Shuvo/Documents/Python/Shooter Game/sounds/music.wav")
background_music.play(loops = -1)



while True: # run forever -> keeps our game running


	# event loop	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()



		if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:

			# laser
			laser_rect = laser_surf.get_rect(midbottom = ship_rect.midtop)
			laser_list.append(laser_rect)


			# timer
			can_shoot = False 
			shoot_time = pygame.time.get_ticks()


			# play laser sound
			laser_sound.play()


		if event.type == meteor_timer:

			# random position 
			x_pos = randint(-100,WINDOW_WITH + 100)
			y_pos = randint(-100,-50)


			# creationg a rect
			meteor_rect = meteor_surf.get_rect(center = (x_pos, y_pos))


			# create a random direction 
			direction = pygame.math.Vector2(uniform(-0.5, 0.5),1)

			meteor_list.append((meteor_rect,direction))
				



	# framerate limit
	dt = clock.tick(120) / 1000


	# mouse input
	ship_rect.center = pygame.mouse.get_pos()



	# update 
	laser_update(laser_list)
	meteor_update(meteor_list)
	can_shoot = laser_timer(can_shoot, 400)



	# meteor ship collisions 
	for meteor_tuple in meteor_list:
		meteor_rect = meteor_tuple[0]
		if ship_rect.colliderect(meteor_rect):
			pygame.quit()
			sys.exit()



	# laser meteor collisions 
	for laser_rect in laser_list:
		for meteor_tuple in meteor_list:
			if laser_rect.colliderect(meteor_tuple[0]):
				meteor_list.remove(meteor_tuple)
				laser_list.remove(laser_rect)
				explosion_sound.play()		



	# drawing 
	display_surface.fill((0,0,0))
	display_surface.blit(bg_surf,(0,0))

	display_score()


	

	
	# for loop that draws the laser surface where the reacts are 
	for rect in laser_list:
		display_surface.blit(laser_surf,rect)


	for meteor_tuple in meteor_list:
		display_surface.blit(meteor_surf,meteor_tuple[0])	


	display_surface.blit(ship_surf,ship_rect)
	



	# draw the final
	pygame.display.update()			
