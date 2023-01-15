import pygame
from game import Snake, codes
from pygame.locals import *
from ui import UI

class GUI(UI):
    def __init__(self, game, cell_size = 25):
        super().__init__(game)

        self.cell_size = cell_size
        self.width, self.height = self.game.rows * self.cell_size, self.game.cols * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))


    def draw_lines(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self):
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                value = self.game.grid[row][col]
                color = pygame.Color("#004242") if value == codes['head'] \
                    else pygame.Color("#318CE7") if value == codes['body'] \
                    else pygame.Color("green") if value == codes['point'] else pygame.Color("white")
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size
                    ),
                )
        return None

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Snake!")
        self.screen.fill(pygame.Color("white"))

        font_score = pygame.font.SysFont('Arial', 26, bold=True)
        font_loss = pygame.font.SysFont('Arial', 66, bold=True)

        running = True
        is_pause = False
        while running:
            is_not_direction_edited = True
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        is_pause = not is_pause

                    if is_not_direction_edited and event.key == pygame.K_a:
                        is_not_direction_edited = False
                        self.game.set_direction('left')
                    elif is_not_direction_edited and event.key == pygame.K_w:
                        is_not_direction_edited = False
                        self.game.set_direction('top')
                    elif is_not_direction_edited and event.key == pygame.K_d:
                        is_not_direction_edited = False
                        self.game.set_direction('right')
                    elif is_not_direction_edited and event.key == pygame.K_s:
                        is_not_direction_edited = False
                        self.game.set_direction('bottom')

            self.draw_grid()
            self.draw_lines()
            self.screen.blit(font_score.render(f'{self.game.score}', 1, pygame.Color('red')), (5, 0))

            if not is_pause and not self.game.is_loss:
                self.game.step()

            if self.game.is_loss:
                self.screen.blit(font_loss.render('Game over', 1, pygame.Color('red')), (self.height//2-180, self.width//3))

            pygame.display.flip()
            clock.tick(self.game.speed)

        pygame.quit()

if __name__ == "__main__":
    game = Snake()
    gui = GUI(game)
    gui.run()
