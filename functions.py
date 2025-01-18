import sys
import pygame
from bullets import Bullets
import birds
from pygame import mixer




def check_event(airplane, bullets_Group, screen):  # to check every event in game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                airplane.Down = True
            elif event.key == pygame.K_UP:
                airplane.Up = True
            elif event.key == pygame.K_SPACE:
                if len(bullets_Group) < 6:
                    new_bullet = Bullets(screen, airplane)
                    bullets_Group.add(new_bullet)
                    bullet_sound = mixer.Sound("audio/bullet.mp3")
                    bullet_sound.play()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                airplane.Down = False
            elif event.key == pygame.K_UP:
                airplane.Up = False


def screen_update(screen, bg, ai_settings, scroll, Airplane_Group, birds_Group, airp, bullets_Group, birds_images,
                  birds_colors, hearts, HIGESTSCORE):
    # --------------------------update background--------------------------
    update_background(screen, bg, ai_settings, scroll)
    # ---------------------------------------------------------------------
    # ---------------------------update airplane---------------------------
    update_airplane(Airplane_Group, birds_Group, screen, airp)
    # ----------------------------update birds---------------------------
    update_birds(birds_Group, bullets_Group, airp, birds_images, birds_colors, screen)
    # -----  check if one of bullets out of screen to delete it + update_bullets-----------

    update_bullets(screen, bullets_Group, birds_Group)
    ammo(bullets_Group, screen)

    # ------------------------draw hearts-------------------------------
    draw_hearts(airp, hearts, screen)
    # -------------------------update score and check highest score-------------------------------
    update_score(airp, screen)
    highest_score(HIGESTSCORE, screen)


def update_background(screen, bg, ai_settings, scroll):  # this function update background
    screen.blit(bg, (0 - scroll, 0))
    screen.blit(bg, (ai_settings.game_width - scroll, 0))


def update_scroll(scroll, ai_settings):  # this  function update scroll value
    scroll += 1
    if scroll == ai_settings.game_width:
        scroll = 0
    return scroll


def update_bullets(screen, bullets_Group, birds_Group):  # this fucntion will  give u  bullet when your shot collided
    # with bird
    for b in bullets_Group:
        if pygame.sprite.spritecollide(b, birds_Group, True) and birds_Group.check_x < screen.width - 50:
            bullets_Group.remove(b)

    bullets_Group.update()
    bullets_Group.draw(screen)


def birds_spawn(birds_Group, screen, time, birds_image, birds_colors):
    if len(birds_Group) < 10 and time % 32 == 0:  # every 32  iteartions we will spawn  1 more bird
        new_bird = birds.birds(screen, birds_image, birds_colors)
        birds_Group.add(new_bird)


def update_birds(birds_Group, bullets_Group, airp, birds_images, birds_colors,
                 screen):  # will  load birds  on screen and  update their frames
    birds_Group.update(bullets_Group, airp, birds_images, birds_colors)
    birds_Group.draw(screen)


def update_airplane(Airplane_Group, birds_Group, screen, airp):  # update  airplane image and  update  its position
    Airplane_Group.update(birds_Group)
    Airplane_Group.draw(screen)
    airp.update_key()


def draw_hearts(airp, hearts, screen):  # draw hearts
    for i in range(0, airp.lives):
        screen.blit(hearts[i].image, hearts[i].image_rect)


def choose_background(airp):  # this function will choose background every 15 score
    bg = 0
    if airp.score % 45 >= 30:
        bg = pygame.image.load("images/bg2.jpg")

    elif 15 <= airp.score % 45 < 30:
        bg = pygame.image.load("images/bg3.jpg")

    elif 0 <= airp.score % 45 < 15:
        bg = pygame.image.load("images/bg4.jpg")

    return bg


def check_lives_to_play_game_over_audio(airp):
    if airp.lives == 0:
        mixer.music.stop()
        game_over = mixer.Sound("audio/failure-1-89170.mp3")
        game_over.play()


def ammo(bullets_Group, screen):
    ammo_FONT = pygame.font.Font(pygame.font.get_default_font(), 20)
    text = ammo_FONT.render(f"AMMO : {6 - len(bullets_Group)}/ 6", True, "black")
    text_rect = text.get_rect()
    text_rect.left = 20
    text_rect.centery = 100
    screen.blit(text, text_rect)


def highest_score(HIGESTSCORE, screen):  # this function will update highest score on screen
    highest_score_FONT = pygame.font.Font(pygame.font.get_default_font(), 20)
    highest_score_text = highest_score_FONT.render(f"HIGHEST SCORE : {HIGESTSCORE[0]}", True, "black")
    highest_score_text_rect = highest_score_text.get_rect()
    highest_score_text_rect.left = 20
    highest_score_text_rect.centery = 40
    screen.blit(highest_score_text, highest_score_text_rect)


def update_score(airp, screen):  # this funtion will update score  on screen
    update_score_FONT = pygame.font.Font(pygame.font.get_default_font(), 20)
    score_text = update_score_FONT.render(f"SCORE : {airp.score}", True, "black")
    score_text_rect = score_text.get_rect()
    score_text_rect.left = 20
    score_text_rect.centery = 70
    screen.blit(score_text, score_text_rect)


def game_over_screen(ai_settings, screen, airp):  # load game over screen
    # ---------------------load  play again text------------------------------
    game_over_font = pygame.font.Font(pygame.font.get_default_font(), 24)
    play_again_text1 = game_over_font.render("play again(Y / N)", True, "red")
    play_again_text2 = game_over_font.render(f"score is {airp.score}", True, "red")
    # ---------------------------set position  on screen for play_again_text1 and load it----------------------
    play_again_text1_rect = play_again_text1.get_rect()
    play_again_text1_rect.centerx = ai_settings.game_width // 2
    play_again_text1_rect.centery = ai_settings.game_height // 2 + 50
    screen.blit(play_again_text1, play_again_text1_rect)
    # -----------------------set position on screen for  play_again_text2 and load it-----------------------------
    play_again_text2_rect = play_again_text2.get_rect()
    play_again_text2_rect.x = play_again_text1_rect.x + 40
    play_again_text2_rect.y = play_again_text1_rect.y + 30
    screen.blit(play_again_text2, play_again_text2_rect)
    # ------------------------set position on screen for  game_over_image  and load it----------------------------
    game_over_image = pygame.image.load("images/gameover.png")
    game_over_image = pygame.transform.scale(game_over_image, (200, 200))
    game_over_image_rect = game_over_image.get_rect()
    game_over_image_rect.x = ai_settings.game_width // 2 - 110
    game_over_image_rect.y = ai_settings.game_height // 2 - 150
    screen.blit(game_over_image, game_over_image_rect)
    # --------------------------------------------------------------
