import pygame
import os
import random

print ("Welcome to my game, use wasd to move and space to shoot. Good luck against your first enemy! Press enter to continue.")

wait = input("Press enter to continue")

os.chdir('images')
images = [pygame.image.load(file) for file in os.listdir()]
current_directory = os.getcwd()
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
os.chdir(parent_directory)
os.chdir('imaged')
imaged = [pygame.image.load(file) for file in os.listdir()]
current_directory = os.getcwd()
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
os.chdir(parent_directory)
os.chdir('imagea')
imagea = [pygame.image.load(file) for file in os.listdir()]
current_directory = os.getcwd()
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
os.chdir(parent_directory)
os.chdir('imagew')
imagew = [pygame.image.load(file) for file in os.listdir()]


dictionary_for_player_movements = {}
dictionary_for_player_movements['w'] = imagew
dictionary_for_player_movements['d'] = imaged
dictionary_for_player_movements['a'] = imagea
dictionary_for_player_movements['s'] = images

#functions
def character_movement(keys, character):
  global current_image

  # change cycle to imaged
  if keys[pygame.K_d] and character.x < WIDTH - 70:
    current_image = (current_image + 1) % 3
    character.x += 20
    return 'd'
    
  #change file cycle to imagea
  if keys[pygame.K_a] and character.x < WIDTH - 70:
    current_image = (current_image + 1) % 3
    character.x += -20
    return 'a'
    
  # Default
  if keys[pygame.K_s] and character.y < HEIGHT - 70:
    current_image = (current_image + 1) % 3
    character.y += 20
    return 's'
    
  #change file cycle to imagew
  if keys[pygame.K_w] and character.y < HEIGHT - 70:
    current_image = (current_image + 1) % 3
    character.y += -20
    return 'w'
  return 'i'


# Fireball2 and fireball3 are the other images, make it iterate through them.
def fireball_movement(fireball, speed):
  if fireball.x < WIDTH - fireball.width:
    # Adjust condition to check against fireball's width
    fireball.x += speed
  else:
    fireball.x = -40  # Reset the fireball position
    return False  # Return False when fireball is reset
  return True  # Return True to indicate the fireball is still moving

 


def enemy_movement(character, enemy, speed):
  if character.x - enemy.x > 0:
    enemy.x += speed
  elif character.x - enemy.x < 0:
    enemy.x += -speed

  if character.y - enemy.y > 0:
    enemy.y += speed
  elif character.y - enemy.y < 0:
    enemy.y += -speed


# colliderect
def collision(rect_1, rect_2):
  if rect_1.colliderect(rect_2):
    print("COLLISION")
    return True

  return False


# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 600, 500
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Elemental War')

current_image = 0



# Set character position
image_rect = images[current_image].get_rect()
image_rect.width = 50
image_rect.height = 50
image_rect.center = (30, 250)
print(
    f"the width and height of the player rect is {image_rect.width}, {image_rect.height}"
)

# Load fireball images
current_directory = os.getcwd()
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
os.chdir(parent_directory)
os.chdir('Fire projectile')  # gets the fireball file
fireballframes = [pygame.image.load(file)
                  for file in os.listdir()]  # fireball images

current_directory = os.getcwd()

# Change to the parent directory
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
os.chdir(parent_directory)
os.chdir('Enemy Frames')
enemyframes = [pygame.image.load(file) for file in os.listdir()]
enemy_rect = images[0].get_rect()
enemy_rect.width = 50
enemy_rect.height = 75
random_spawn_point = (random.randint(250, 500), random.randint(1, 400))
enemy_rect.center = random_spawn_point

#Enemy Hurt Pictures
os.chdir(parent_directory)
os.chdir('Enemy Hurt')
enemy_hurt_frames = [pygame.image.load(file) for file in os.listdir()]

#Player Hurt Pictures
os.chdir(parent_directory)
os.chdir('Player Hurt')
player_hurt_frames = [pygame.image.load(file) for file in os.listdir()]

fireball_rect = fireballframes[2].get_rect()

# Game variables
fireball_launched = False

# Set up the game clock
FPS = 5
clock = pygame.time.Clock()

#tracks the fireball
curr_fireball = 0  #related to which frame of firebsll animation
fireball_cooldown = 0  #related to the time of the fireball
fireball_waiting = False

#enemy & player variables
curr_enemy_animation = 0
curr_player_animation = 0
player_hurt = False
enemy_hurt = False
enemy_invincible = 25
Player_invincible = 25
ENEMY_INVINCIBLE_VALUE = 5
PLAYER_INVINCIBLE_VALUE = 5
enemy_speed = 5
Enemy_life = 5
Player_life = 5
timer = 0

print(f"Enemy has {Enemy_life} lives left")


def enemyAnimFunction():
  DISPLAYSURF.blit(enemy_hurt_frames[curr_enemy_animation], enemy_rect)


def player_hurt_animation():
  DISPLAYSURF.blit(player_hurt_frames[curr_player_animation], image_rect)


# Main game loop
run = True
while run:
  print(f"the current player animation is {curr_player_animation}")
  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
      print(f"the mouse was clicked at {event.pos}")
    elif event.type == pygame.QUIT:
      run = False

  keys = pygame.key.get_pressed()
  direction = character_movement(keys, image_rect)
  if timer % 5 == 0:
    print(f"{timer // 5} seconds have passed")
    print("")
    print(f"{fireball_cooldown} is the fireball cooldown")
  timer += 1
  print(f"The fireball is currently at this position {fireball_rect.center}")
  if fireball_waiting:
    if fireball_cooldown == 30:
      fireball_cooldown = 0
      fireball_waiting = False
    else:
      fireball_cooldown += 1

  if enemy_hurt:
    if enemy_invincible == 0:
      Enemy_life -= 1
      enemy_hurt = False
      enemy_invincible = ENEMY_INVINCIBLE_VALUE - 5
      ENEMY_INVINCIBLE_VALUE = enemy_invincible
      enemy_speed += 2.5
      print(f"Enemy has {Enemy_life} lives left")
    else:
      enemy_invincible -= 1

  if player_hurt:
    if Player_invincible == 0:
      Player_life -= 1
      player_hurt = False
      Player_invincible = PLAYER_INVINCIBLE_VALUE - 5
      PLAYER_INVINCIBLE_VALUE = Player_invincible
      print(f"Player has {Player_life} lives left")
    else:
      Player_invincible -= 1

  if Enemy_life == 0:
    print("You win, Congratulations!!!")
    break
  if Player_life <= 0: 
    print("You Lose!!! Womp Womp")
    break

  if keys[pygame.K_SPACE] and not fireball_launched and fireball_cooldown == 0:
    fireball_launched = True
    fireball_waiting = True
    # Launch fireball from character's position
    fireball_rect.x, fireball_rect.y = image_rect.x, image_rect.y

  if collision(enemy_rect, image_rect):
    player_hurt = True

  if player_hurt:
    print("the player is hurt")
    player_hurt_animation()
    curr_player_animation = (curr_player_animation + 1) - 1
  else:
    DISPLAYSURF.blit(images[0], image_rect)
    player_hurt = False
  if fireball_launched:
    fireball_launched = fireball_movement(fireball_rect, 40)
    if not enemy_hurt:
      if collision(enemy_rect, fireball_rect):
        enemy_hurt = True

  # Clear the screen
  DISPLAYSURF.fill((255, 255, 255))

  # Draw the character and fireball
  if player_hurt:
    player_hurt_animation()
    curr_player_animation = (curr_player_animation + 1) % 2
  else:
    if direction == 'i':
      DISPLAYSURF.blit(images[0], image_rect)
    else:
      DISPLAYSURF.blit(dictionary_for_player_movements[direction][current_image], image_rect)

  if enemy_hurt:
    enemy_movement(image_rect, enemy_rect, 5)
  else:
    enemy_movement(image_rect, enemy_rect, enemy_speed)

  if enemy_hurt:
    enemyAnimFunction()
    curr_enemy_animation = (curr_enemy_animation + 1) % 2
  else:
    DISPLAYSURF.blit(enemyframes[0], enemy_rect)

  if fireball_launched:
    DISPLAYSURF.blit(fireballframes[curr_fireball],
                     fireball_rect)  # Draw fireball if launched
    curr_fireball = (curr_fireball + 1) % 3
  # Update the display
  pygame.display.update()

  # Control the frame rate
  clock.tick(FPS)

# Quit Pygame properly when the game loop exits
pygame.quit()