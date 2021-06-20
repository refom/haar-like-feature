import pygame
from pygame import Vector2
from font_teks import FontText

FontText.update()

class ButtonText:
	all_buttons = []
	last_mouse_pos = (0,0)

	def __init__(self, teks, xy, color=(255,255,255), hover_color=(150,150,150)):
		self.text = teks
		self.pos = Vector2(xy)
		self.rect = pygame.Rect(xy, (10,10))

		self.clicked = False

		self.color = color
		self.hover_color = hover_color

		self.all_buttons.append(self)

	def render(self, surface):
		color = self.color
		
		if self.check_collisions(self.last_mouse_pos):
			color = self.hover_color

		teks = FontText.font_normal.render(f"- {self.text}", True, color)
		self.rect = teks.get_rect()
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
		surface.blit(teks, self.rect)


	@classmethod
	def handle_event(cls, events):
		for event in events:
			for btn in cls.all_buttons:
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1 and btn.check_collisions(event.pos):
						btn.clicked = True
				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						btn.clicked = False

		cls.last_mouse_pos = pygame.mouse.get_pos()

	def get_click(self):
		return self.clicked

	def check_collisions(self, mouse_pos):
		return self.rect.collidepoint(mouse_pos)

	@classmethod
	def check_all_col(cls, mouse_pos):
		for btn in cls.all_buttons:
			if btn.check_collisions(mouse_pos): return True

	@classmethod
	def clear_all(cls):
		cls.all_buttons.clear()


