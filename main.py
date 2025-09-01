from ultralytics import YOLO
import cv2
import pygame
from random import choice, randint, uniform
from particles import Particle
from circleParticles import CircleParticle

pygame.init()
#screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
maxParticles = 500
start_point, end_point = (400, 400), (600, 600)
# duration affects speed at which the partcles move at
durationToMove = 5
flipParticle = False
path = []

particle_group = pygame.sprite.Group()

# Load an official model
model = YOLO("yolo11n-pose.pt")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not start video stream.")
    exit()

# Convert from OpenCV to Pygame scale 
# ex. flip y-axis or scale to Pygame surface
def convert_point(pt, scale = 1.0):
    x, y = pt
    return (int(x* scale), int(y * scale))

def main_loop():
    while True:
        # read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        results = model(frame)

        if results:
            kp = results[0].keypoints.xy[0].cpu().numpy()
        
        path_points = kp
        pyg_points = [convert_point(p) for p in path_points]
        
        floatParticle = CircleParticle(pyg_points, 3)

        # clock
        dt = clock.tick() / 1000

        # events
        #for event in pygame.event.get():
            #if event.type == pygame.QUIT:
                #print("Quitting game.")
                #exit()
            #if event.type == pygame.MOUSEBUTTONDOWN:
                #for _ in range(maxParticles):
                    #pos = pygame.mouse.get_pos()
                    #color = choice( ("red", "blue", "yellow") )
                    #direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
                    #direction = direction.normalize()
                    #speed = randint(50, 400)
                    #Particle(particle_group, pos, color, direction, speed)
        
        # display
        screen.fill((0,0,0, 20))
        if dt % 3 == 0:
            floatParticle.update(dt)
            
        floatParticle.draw(screen)
        pygame.display.flip()
        #particle_group.draw(screen)
        #qqcv2.imshow("Live feed", frame)

        # update
        #particle_group.update(dt)
        #pygame.display.update()

        #print(len(particle_group.sprites()))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    pygame.init()
    main_loop()

cap.release()
cv2.destroyAllWindows()
pygame.quit()