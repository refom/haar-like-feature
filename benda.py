import pygame
from pygame import Vector2

import numpy as np
from PIL import Image
from warna import COLORS
from integral import integral_image
from haar import FeatureType, HaarLikeFeature

class Benda:
    first_mouse_pos = (0,0)
    last_mouse_pos = (0,0)

    def __init__(self, nama, img, pos):
        self.nama = nama
        self.img = pygame.image.load(img)
        self.pos = Vector2(pos)
        self.rect = self.img.get_rect()

        self.button_down = False
        self.draw_rect = False
        self.hide_rect = True

        images = Image.open(img).convert("L")
        image_arr = np.array(images)
        self.int_img = integral_image(image_arr)

    def render(self, surface):
        width, height = surface.get_size()

        # render gambar
        self.pos.x = width/2
        self.pos.y = height/2
        self.rect = self.img.get_rect(center=(self.pos.x, self.pos.y))
        surface.blit(self.img, self.rect)

    def render_rect(self, surface):
        p1 = self.first_mouse_pos
        p2 = (self.first_mouse_pos[0], self.last_mouse_pos[1])
        p3 = self.last_mouse_pos
        p4 = (self.last_mouse_pos[0], self.first_mouse_pos[1])
        
        if self.rect.collidepoint(p1) and self.rect.collidepoint(p2) and self.rect.collidepoint(p3) and self.rect.collidepoint(p4):
            pygame.draw.polygon(surface, COLORS.light_green, [p1, p2, p3, p4], 2)


    def eksekusi_haar(self):
        if not self.hide_rect:
            if not self.button_down:
                
                result = []
                for feature in FeatureType.ALL:
                    fitur = HaarLikeFeature(feature, ())



    def grab(self):
        # Jika gak gambar
        if not self.draw_rect:
            # Jika ditekan
            if self.button_down:
                # Simpan posnya
                self.draw_rect = True
                self.hide_rect = False
                self.first_mouse_pos = pygame.mouse.get_pos()
        # Jika lagi gambar
        else:
            # mouse di lepas
            if not self.button_down:
                self.draw_rect = False
            self.last_mouse_pos = pygame.mouse.get_pos()


    def get_input(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.button_down = True
                if event.button == 3:
                    self.hide_rect = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.button_down = False




