# mohammed awwad 151689

from Airplane import airplane
from functions import *
from heart import *
from screen_settings import screen_settings

clock = pygame.time.Clock()
FPS = 50


def run():
    pygame.init()
    run = True
    # ------------------------HIGHEST_SCORE--------------------------------
    n = open("HIGEST_SCORE.txt", "r")
    higest_score = n.readlines()
    higest_score[0] = eval(higest_score[0])
    n.close()
    # ---------------------setting up the screen --------------------------
    ai_settings = screen_settings()
    screen_size = (ai_settings.game_width, ai_settings.game_height)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("FLOPPY_BIRDS")
    # ---------------------------------------------------------------------
    pygame.sprite.Group()

    bullets_Group = pygame.sprite.Group()
    # -------------------------  set background --------------------------

    scroll = 0
    # ---------------load birds images and save it in dictionary----------
    time = 0
    birds_colors = ["red", "yallow", "gray", "blue"]
    birds_images = {}

    for bird in birds_colors:
        birds_images[bird] = []
        for i in range(1, 5):
            image = pygame.image.load(f"images/Birds/{bird}-{i}.png")
            image = pygame.transform.scale(image, (50, 40))
            birds_images[bird].append(image)
    birds_Group = pygame.sprite.Group()
    # --------------------------- set Airplane-----------------------------
    Airplane_Group = pygame.sprite.Group()
    airp = airplane(screen)
    Airplane_Group.add(airp)
    # -------------------------hearts---------------------------------------
    x = ai_settings.game_width - 200
    y = 15
    hearts = []
    for i in range(1, 4):
        hearts.append(heart(screen, x, y))
        x += hearts[0].image_rect.width + 10

    # ---------------------------background_music--------------------------------
    mixer.music.load("audio/background.mp3")
    # -------------------------- LOAD STARTING SCREEN ------------------------------------
    starting_screen = True
    starting_screen_image = pygame.image.load("images/starting screen.png")
    starting_screen_image = pygame.transform.scale(starting_screen_image,
                                                   (ai_settings.game_width, ai_settings.game_height))
    while starting_screen:
        screen.blit(starting_screen_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT:
                    starting_screen = False
            elif event.type == pygame.QUIT:
                quit()
                sys.exit()

        pygame.display.update()
    # --------------------------- LOAD GAME --------------------------------------------------
    while run:
        if airp.score == 0:
            mixer.music.play()
            airp.score += 1

        clock.tick(FPS)
        # changing back ground------------------------
        bg = choose_background(airp)
        bg = pygame.transform.scale(bg, screen_size)
        # --------------------------------------------------
        check_event(airp, bullets_Group, screen)
        scroll = update_scroll(scroll, ai_settings)  # update scroll value
        screen_update(screen, bg, ai_settings,
                      scroll, Airplane_Group,
                      birds_Group, airp, bullets_Group, birds_images, birds_colors, hearts,
                      higest_score)  # update the entire screen
        # ----------------------------------------------------
        time += 1
        birds_spawn(birds_Group, screen, time, birds_images, birds_colors)  # spawn more birds
        # -----------------------------------------------------
        check_lives_to_play_game_over_audio(airp)
        while airp.lives == 0:  # CHECK GAME OVER OR NO
            game_over_screen(ai_settings, screen, airp)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        birds_Group.empty()
                        bullets_Group.empty()
                        Airplane_Group.empty()
                        airp = airplane(screen)
                        Airplane_Group.add(airp)
                    elif event.key == pygame.K_n:
                        run = False
                        break

            if higest_score[0] < airp.score:  # check if your score is higher than the highest score
                higest_score[0] = airp.score
                n = open("HIGEST_SCORE.txt", "w")
                n.write(str(higest_score[0]))
                n.close()

            if not run:
                break

        pygame.display.update()


run()
