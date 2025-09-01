from ultralytics import YOLO
import cv2
import pygame
from random import choice, randint, uniform
from particles import Particle

pygame.init()
#screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
maxParticles = 500

particle_group = pygame.sprite.Group()

# Load an official model
model = YOLO("yolo11n-pose.pt")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not start video stream.")
    exit()

def main_loop():
    while True:
        # read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        #results = model(frame)

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting game.")
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for _ in range(maxParticles):
                    pos = pygame.mouse.get_pos()
                    color = choice( ("red", "blue", "yellow") )
                    direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
                    direction = direction.normalize()
                    speed = randint(50, 400)
                    Particle(particle_group, pos, color, direction, speed)

        # clock
        dt = clock.tick() / 1000

        # display
        screen.fill((0,0,0))
        particle_group.draw(screen)
        #qqcv2.imshow("Live feed", frame)

        # update
        particle_group.update(dt)
        pygame.display.update()

        print(len(particle_group.sprites()))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    pygame.init()
    main_loop()

cap.release()
cv2.destroyAllWindows()  