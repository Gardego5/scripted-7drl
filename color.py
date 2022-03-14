#       Basic Colors        # ####  ####  ####
white                       = 0xFF, 0xFF, 0xFF
gray_85                     = 0xD9, 0xD9, 0xD9
gray_75                     = 0xBF, 0xBF, 0xBF
gray_50                     = 0x80, 0x80, 0x80
gray_25                     = 0x40, 0x40, 0x40
gray_15                     = 0x26, 0x26, 0x26
black                       = 0x00, 0x00, 0x00
red                         = 0xFF, 0x00, 0x00
yellow                      = 0xFF, 0xFF, 0x00
green                       = 0x00, 0xFF, 0x00
cyan                        = 0x00, 0xFF, 0xFF
blue                        = 0x00, 0x00, 0xFF
magenta                     = 0xFF, 0x00, 0xFF

bright_orange               = 0xFF, 0xAC, 0x1C

#         UI Colors         # ####  ####  ####
ui_main                     = gray_85
ui_subdued                  = gray_50
ui_very_subdued             = gray_25
ui_bg_highlighted           = gray_15
ui_bg                       = black
welcome_text                = 0x20, 0xA0, 0xFF
invalid                     = 0xFF, 0xFF, 0x00
impossible                  = gray_50
error                       = 0xFF, 0x40, 0x40

menu_title                  = 0xFF, 0xFF, 0x20
menu_text                   = white
menu_author                 = gray_15

selected_window             = 0xFF, 0xD9, 0x66

hp_bar_text                 = black
hp_bar_filled               = 0xE1, 0xF0, 0x9E
hp_bar_empty                = 0xFC, 0xFF, 0xF0

#       Status Colors       # ####  ####  ####
player_atk                  = 0xE0, 0xE0, 0xE0
enemy_atk                   = 0xFF, 0xC0, 0xC0

player_die                  = 0xFF, 0x30, 0x30
enemy_die                   = 0xFF, 0xA0, 0x30

health_recovered            = 0x00, 0xFF, 0x00

needs_target                = 0x3F, 0xFF, 0xFF
status_effect_applied       = 0x3F, 0xFF, 0x3F
stairs                      = 0x9F, 0x3F, 0xFF

#       Leveled Colors      # ####  ####  ####
def leveled(level):
    if level == 0:
        return                0x33, 0x3D, 0x7E
    elif level == 1:
        return                0x33, 0x3D, 0x7E
    elif level == 2:
        return                0x20, 0x60, 0xDC
    elif level == 3:
        return                0xFF, 0x47, 0x4A
    elif level == 4:
        return                0xDE, 0xDE, 0x21
    elif level == 5:
        return                0xAD, 0xFF, 0xA8
    else:
        return                0xF4, 0xF7, 0xF9