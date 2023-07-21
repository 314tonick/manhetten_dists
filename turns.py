__all__ = "AVALIBLE_TURNS"
AVALIBLE_TURNS = {
    "SINGLE": (1, [(0, 0)]),
    "CROSS": (4, [(0, 0), (0, 1), (0, 2), (0, 3), (0, -1), (0, -2), (0, -3),
                                (1, 0), (2, 0), (3, 0), (-1, 0), (-2, 0), (-3, 0)]),
    "HORIZONTAL": (4, [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6)]),
    "VERTICAL": (4, [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0)]),
    "FRAME": (6, [(6, -6), (-6, -6), (-6, 6), (6, -5), (-6, -5), (-5, 6), (-5, -6), (6, -4), (-6, -4), (-4, 6), (-4, -6), (6, -3), (-6, -3),
    (-3, 6), (-3, -6), (6, -2), (-6, -2), (-2, 6), (-2, -6), (6, -1), (-6, -1), (-1, 6), (-1, -6), (6, 0), (-6, 0), (0, 6), (0, -6), (6, 1), 
    (-6, 1), (1, 6), (1, -6), (6, 2), (-6, 2), (2, 6), (2, -6), (6, 3), (-6, 3), (3, 6), (3, -6), (6, 4), (-6, 4), (4, 6), (4, -6), (6, 5), 
    (-6, 5), (5, 6), (5, -6), (6, 6)]),
    "SQUARE_SMALL": (3, [(0, 0), (0, 1), (0, 2), (0, -1), (0, -2),
                         (-1, 0), (-1, 1), (-1, 2), (-1, -1), (-1, -2),
                         (1, 0), (1, 1), (1, 2), (1, -1), (1, -2),
                         (-2, 0), (-2, -1), (-2, 1),
                         (2, 0), (2, -1), (2, 1)]),
    "SQUARE_BIG": (5, [(0, 0), (0, -1), (0, -2), (0, -3), (0, -4), (0, 1), (0, 2), (0, 3), (0, 4),
                        (-1, 0), (-1, -1), (-1, -2), (-1, -3), (-1, -4), (-1, 1), (-1, 2), (-1, 3), (-1, 4),
                        (-2, 0), (-2, -1), (-2, -2), (-2, -3), (-2, -4), (-2, 1), (-2, 2), (-2, 3), (-2, 4),
                        (1, 0), (1, -1), (1, -2), (1, -3), (1, -4), (1, 1), (1, 2), (1, 3), (1, 4),
                        (2, 0), (2, -1), (2, -2), (2, -3), (2, -4), (2, 1), (2, 2), (2, 3), (2, 4),
                        (-3, 0), (-3, -1), (-3, -2), (-3, -3), (-3, 1), (-3, 2), (-3, 3), (3, 0), (3, -1), (3, -2), (3, -3), (3, 1), (3, 2), (3, 3),
                        (-4, 0), (-4, -1), (-4, -2), (-4, 1), (-4, 2), (4, 0), (4, -1), (4, -2), (4, 1), (4, 2)]),
    "ROMBUS": (7, [(-7, 0), (-6, -1), (-6, 0), (-6, 1), 
                   (-5, -2), (-5, -1), (-5, 0), (-5, 1), (-5, 2),
                   (-4, -3), (-4, -2), (-4, -1), (-4, 0), (-4, 1), (-4, 2), (-4, 3),
                   (-3, -4), (-3, -3), (-3, -2), (-3, -1), (-3, 0), (-3, 1), (-3, 2), (-3, 3), (-3, 4),
                   (-2, -5), (-2, -4), (-2, -3), (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-2, 3), (-2, 4), (-2, 5),
                   (-1, -6), (-1, -5), (-1, -4), (-1, -3), (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3), (-1, 4), (-1, 5), (-1, 6),
                   (0, -7), (0, -6), (0, -5), (0, -4), (0, -3), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
                   (1, -6), (1, -5), (1, -4), (1, -3), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                   (2, -5), (2, -4), (2, -3), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
                   (3, -4), (3, -3), (3, -2), (3, -1), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
                   (4, -3), (4, -2), (4, -1), (4, 0), (4, 1), (4, 2), (4, 3),
                   (5, -2), (5, -1), (5, 0), (5, 1), (5, 2),
                   (6, -1), (6, 0), (6, 1), (7, 0)])
}