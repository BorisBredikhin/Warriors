from enum import Enum, auto

from pygame import SurfaceType
from pygame.font import Font, FontType

main_font: FontType = Font(None, 16)


class Alignment(Enum):
    LEFT = auto()
    RIGHT = auto()


def show_text(surface: SurfaceType, text: str, position: (int, int), font: FontType = main_font, antialiasing=0,
              color=(0, 0, 0), align=Alignment.LEFT):
    for line_number, line in enumerate(text.splitlines()):
        obj = font.render(line, antialiasing, color)
        surface.blit(obj,
                     (position[0] - (0
                                     if align == Alignment.LEFT else
                                     font.size(line)[0]
                                     ),
                      position[1] + line_number * font.size(line)[1]))
