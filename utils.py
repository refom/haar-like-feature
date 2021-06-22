
import os
import pygame
from pygame import Vector2


def get_all_image(images_path):

    list_img = os.listdir(images_path)

    images = []

    for _file in list_img:
        if _file.endswith(".jpg") or _file.endswith(".png") or _file.endswith(".jpeg"):
            img_path = os.path.join(images_path, _file)
            images.append(img_path)
    
    return images


class BoxBergerak:
    def __init__(self, xy, wh, color=(255,255,255)):
        self.pos = Vector2(xy)
        self.rect = pygame.Rect(xy, wh)
        self.color = color

        self.mouse_down = False
        self.gerak = False

        self.first_mouse_pos = Vector2(0,0)
        self.last_mouse_pos = Vector2(0,0)
    
    def render(self, surface):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        pygame.draw.rect(surface, self.color, self.rect)
    
    def grab(self):
        if not self.gerak:
            if self.mouse_down:
                self.gerak = True
                self.first_mouse_pos = Vector2(pygame.mouse.get_pos())
        else:
            if not self.mouse_down:
                self.gerak = False
            else:
                self.last_mouse_pos = Vector2(pygame.mouse.get_pos())
                self.pos.x += self.last_mouse_pos.x - self.first_mouse_pos.x
                self.pos.y += self.last_mouse_pos.y - self.first_mouse_pos.y
                self.first_mouse_pos = self.last_mouse_pos


    def get_input(self, events):
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.rect.collidepoint(event.pos):
                    self.mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_down = False











