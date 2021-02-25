import pygame
from random import *
import csv


class Dino:
    def __init__(self, x, y, w, h, img, m_jump):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = img
        self.animation_count = -30
        self.jump_counter = 30
        self.make_jump = m_jump
        self.alp = 255
        self.make_collision = False
        self.alpha_counter = 30
        self.double_counter = 2

    def draw_dino(self):
        check = True
        if self.make_collision:
            if self.alpha_counter >= -30 and self.double_counter >= 0:
                self.alp -= self.alpha_counter / 2.5
                self.alpha_counter -= 1
            else:
                self.double_counter -= 1
                self.alpha_counter = 30
            if self.double_counter < 0:
                self.make_collision = False
                self.double_counter = 2
        if check:
            im = self.img[self.animation_count // 6]
            im.set_alpha(self.alp)
            screen.blit(im, (self.x, self.y))
            self.animation_count += 1
            if self.animation_count > 29:
                self.animation_count = 0
                check = False
        else:
            im = self.img[self.animation_count // 6]
            im.set_alpha(self.alp)
            screen.blit(im, (self.x, self.y))
            self.animation_count += 1
            if self.animation_count > 29:
                self.animation_count = 0
                check = True

    def draw_dino_jump(self):
        if self.make_collision:
            if self.alpha_counter >= -30 and self.double_counter >= 0:
                self.alp -= self.alpha_counter / 2.5
                self.alpha_counter -= 1
            else:
                self.double_counter -= 1
                self.alpha_counter = 30
            if self.double_counter < 0:
                self.make_collision = False
                self.double_counter = 2
        im = self.img[self.animation_count // 6]
        im.set_alpha(self.alp)
        screen.blit(self.img[self.animation_count // 6], (self.x, self.y))

    def jump(self):
        if self.jump_counter >= -30:
            if self.jump_counter == 30:
                pygame.mixer.Sound.play(jump_sound)
            self.y -= self.jump_counter / 2.5
            self.jump_counter -= 1
        else:
            pygame.mixer.Sound.play(fall_sound)
            self.jump_counter = 30
            self.make_jump = False


def print_text(text, x, y, font_color=(0, 0, 0), font_type=r'Materials/Font/PingPong.ttf', font_size=30):
    text_type = pygame.font.Font(font_type, font_size)
    text = text_type.render(text, True, font_color)
    screen.blit(text, (x, y))


class Enemy:
    def __init__(self, x, parametrs, speed):
        self.x = x
        self.h = parametrs[2]
        self.y = height - 100 - self.h
        self.w = parametrs[1]
        self.koef = 0
        self.v = speed
        self.img = parametrs[0]
        self.made_jump = False
        self.crash = False
        self.clk = pygame.time.Clock()

    def draw_enemy(self):
        self.enemies_range = {69: [69, randrange(250 + (70 * self.koef), 800 + (70 * self.koef)),
                                   randrange(250 + (70 * self.koef), 700 + (70 * self.koef)),
                                   randrange(250 + (70 * self.koef), 700 + (70 * self.koef))],
                              37: [37, randrange(250 + (70 * self.koef), 700 + (70 * self.koef)),
                                   randrange(250 + (70 * self.koef), 700 + (70 * self.koef)),
                                   randrange(250 + (70 * self.koef), 700 + (70 * self.koef))],
                              40: [40, randrange(250 + (70 * self.koef), 700 + (70 * self.koef)),
                                   randrange(250 + (70 * self.koef), 700 + (70 * self.koef)),
                                   randrange(250 + (70 * self.koef), 700 + (70 * self.koef))]}
        if self.x >= -self.w:
            screen.blit(self.img, (self.x, self.y))
            self.x -= self.v
        else:
            self.made_jump = False
            self.crash = False
            maximum = max([(en.x, en.w) for en in enemies_arr], key=lambda x: x[0])
            if maximum[0] < width + 1:
                self.x = maximum[0] + randrange(250 + (70 * self.koef), 700 + (70 * self.koef))
            else:
                self.x = maximum[0] + int(choice(self.enemies_range[maximum[1]]))

class Cloud:
    def __init__(self, x, y, speed, parametrs):
        self.x = x
        self.y = y
        self.w = parametrs[1]
        self.h = parametrs[2]
        self.img = parametrs[0]
        self.speed = speed
        self.check = True

    def draw_cloud(self):
        if self.x >= -self.w:
            screen.blit(self.img, (self.x, self.y))
            self.x -= self.speed
        else:
            self.check = False


class Button:
    def __init__(self, width, height, img=None, num=0):
        if img is not None:
            self.img = img
            self.w = width
            self.h = height
            self.check_img = True
            self.num = num
        else:
            self.w = width
            self.h = height
            self.action_color = (23, 204, 58)
            self.inaction_color = (13, 162, 58)
            self.check_img = False
            self.num = num

    def show(self, x, y, text='', font_size=30, action=None):
        mouse = pygame.mouse.get_pos()
        if x < mouse[0] < x + self.w and y < mouse[1] < y + self.h:
            if self.check_img:
                temp = pygame.transform.scale(self.img, (int(self.w * 1.1), int(self.h * 1.1)))
                x = x - int(self.w * 0.1 / 2)
                y = y - int(self.h * 0.1 / 2)
                screen.blit(temp, (x, y))
            else:
                pygame.draw.rect(screen, self.action_color, (x, y, self.w, self.h))
                print_text(text, x + 10, y + 10, font_size=font_size)
            click = pygame.mouse.get_pressed()
            if click[0] == 1 and action is not None:
                btn_sound.play()
                pygame.time.delay(100)
                if self.num:
                    action(self.num)
                else:
                    action()
        else:
            if self.check_img:
                screen.blit(self.img, (x, y))
            else:
                pygame.draw.rect(screen, self.inaction_color, (x, y, self.w, self.h))
                print_text(text, x + 10, y + 10, font_size=font_size)


def show_menu():
    global show

    show = True

    start_btn = Button(350, 80)
    record_btn = Button(500, 80)
    exit_btn = Button(120, 80)
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(menu_background, (0, 0))
        start_btn.show(230, 200, 'Start game!', font_size=60, action=choice_user)
        record_btn.show(150, 310, 'Table of records', font_size=60, action=show_records)
        exit_btn.show(350, 420, 'Exit', font_size=60, action=exit_game)
        pygame.display.update()
        clock.tick(60)

def show_records():
    global rec, show
    show = False
    list_of_records = []
    with open(r'Materials/data/table_of_records.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=':', quotechar='"')
        for row in reader:
            if row:
                list_of_records.append(row)
    rec = True
    back_btn = Button(80, 45)
    while rec:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.time.delay(100)
                show_menu()
        pygame.draw.rect(screen, (124, 193, 68), (100, 10, 600, 535))
        pygame.draw.rect(screen, (0, 0, 0), (100, 80, 300, 60), width=3)
        print_text('Player', 195, 90, font_size=40)
        pygame.draw.rect(screen, (0, 0, 0), (399, 80, 301, 60), width=3)
        print_text('Score', 500, 90, font_size=40)
        pygame.draw.line(screen, (0, 0, 0), (399, 90), (399, 545), width=3)
        print_text('Table of records!', 195, 20, font_size=50)
        x_player = 130
        y_player = 150
        x_record = 429
        y_record = 150
        if list_of_records:
            for ind, elem in enumerate(list_of_records):
                player = elem[0]
                record = elem[1]
                print_text(f'{ind + 1}. {player}', x_player, y_player, font_size=30)
                print_text(record, x_record, y_record, font_size=30)
                pygame.draw.line(screen, (0, 0, 0), (100, y_player + 35), (700, y_player + 35))
                y_player += 40
                y_record += 40
        back_btn.show(360, 550, 'Back', font_size=30, action=back_motion)
        pygame.display.update()
        clock.tick(60)

def exit_game():
    pygame.quit()
    quit()

def choice_user():
    global show, user
    show = False
    user = True
    img_1 = pygame.image.load(r'Materials/new_dino/1.png')
    img_1 = pygame.transform.scale(img_1, (140, 200))

    img_2 = pygame.image.load(r'Materials/new_dino/2.png')
    img_2 = pygame.transform.scale(img_2, (140, 200))

    choice_1 = Button(140, 200, img=img_1, num=1)
    choice_2 = Button(140, 200, img=img_2, num=2)
    while user:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.time.delay(100)
                show_menu()
        screen.blit(menu_background, (0, 0))
        pygame.draw.rect(screen, (124, 193, 68), (190, 190, 420, 320))
        pygame.draw.line(screen, (0, 0, 0), (190, 250), (610, 250), width=3)
        pygame.draw.line(screen, (0, 0, 0), (400, 250), (400, 510), width=3)
        print_text('Choice Dino!', 260, 195, font_size=50)
        choice_1.show(220, 280, action=choice_map)
        choice_2.show(430, 280, action=choice_map)
        back_btn.show(350, 520, 'Back', font_size=40, action=back_motion)
        pygame.display.update()
        clock.tick(60)

def choice_map(num):
    global user, maps, num_dino
    num_dino = num
    user = False
    maps = True
    map_1 = pygame.image.load(r'Materials/Backgrounds/Land.jpg')
    map_2 = pygame.image.load(r'Materials/Backgrounds/Land2.jpg')
    map_3 = pygame.image.load(r'Materials/Backgrounds/LandLevel.jpg')
    map_1 = pygame.transform.scale(map_1, (200, 150))
    map_2 = pygame.transform.scale(map_2, (200, 150))
    map_3 = pygame.transform.scale(map_3, (200, 150))
    choice_1 = Button(200, 150, img=map_1, num=1)
    choice_2 = Button(200, 150, img=map_2, num=2)
    choice_3 = Button(200, 150, img=map_3, num=3)
    while maps:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.time.delay(100)
                choice_user()
        screen.blit(menu_background, (0, 0))
        pygame.draw.rect(screen, (124, 193, 68), (50, 200, 700, 260))
        pygame.draw.line(screen, (0, 0, 0), (50, 260), (750, 260), width=3)
        print_text('Choice map!', 260, 210, font_size=50)
        choice_1.show(70, 280, action=start_game)
        choice_2.show(300, 280, action=start_game)
        choice_3.show(530, 280, action=start_game)
        back_btn.show(350, 520, 'Back', font_size=40, action=back_motion)
        pygame.display.update()
        clock.tick(60)

def back_motion():
    global show, user, maps, inp, rec

    if maps:
        maps = False
        choice_user()
    elif user or rec:
        user = False
        rec = False
        show_menu()
    elif inp:
        inp = False
        choice_map(num_land)


def start_game(num):
    global maps, num_land, inp, player
    num_land = num
    maps = False
    input_text = ''
    inp = True
    i = 0
    enter_btn = Button(115, 60)
    while inp:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.time.delay(100)
                choice_map(num_land)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                    player = input_text
                    if i > 0:
                        i -= 1
                elif event.key == pygame.K_RETURN and input_text:
                    enter_name()
                elif i <= 18:
                    input_text += event.unicode
                    player = input_text
                    i += 1
        screen.blit(menu_background, (0, 0))
        pygame.draw.rect(screen, (124, 193, 68), (225, 200, 360, 155))
        print_text('Enter your name:', 240, 205, font_size=40)
        print_text('(Max 16 symbols)', 320, 240, font_size=20)
        print_text('(Just english)', 335, 260, font_size=20)
        pygame.draw.rect(screen, (0, 0, 0), (245, 295, 320, 45), width=2)
        print_text(input_text, 251, 300, font_size=35)
        enter_btn.show(343, 375, text='enter', font_size=40, action=enter_name)
        back_btn.show(350, 445, 'Back', font_size=40, action=back_motion)
        pygame.display.update()
        clock.tick(60)

def enter_name():
    global show, user, maps, inp, rec, running
    show = False
    user = False
    maps = False
    rec = False
    inp = False
    running = True
    pygame.display.update()
    clock.tick(60)

def creat_enemies(arr, speed):
    arr.append(Enemy(width + 20, enemies_img[0], speed))
    arr.append(Enemy(width + 270, enemies_img[1], speed))
    arr.append(Enemy(width + 700, enemies_img[2], speed))


def draw_array(array):
    for enemy in array:
        enemy.draw_enemy()


def paused():
    paused_game = True
    pygame.mixer.music.pause()
    while paused_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                paused_game = False
        print_text('Pause. Press ENTER to continue game...', 130, 300)
        pygame.display.update()
        clock.tick(15)
    pygame.mixer.music.unpause()
    return True

def check_collision(enemies):
    for enemy in enemies:
        if enemy.y == 449:
            if not dino.make_jump:
                if enemy.x <= dino.x + dino.w - 31 <= enemy.x + enemy.w:
                    return enemy
            elif dino.jump_counter >= 0:
                if dino.y + dino.h - 5 >= enemy.y:
                    if enemy.x <= dino.x + dino.w - 31 <= enemy.x + enemy.w:
                        return enemy
            else:
                if dino.y + dino.h - 10 >= enemy.y:
                    if enemy.x <= dino.x <= enemy.x + enemy.w:
                        return enemy
        else:
            if not dino.make_jump:
                if enemy.x <= dino.x + dino.w - 5 <= enemy.x + enemy.w:
                    return enemy
            elif dino.jump_counter == 10:
                if dino.y + dino.h - 5 >= enemy.y:
                    if enemy.x <= dino.x + dino.w - 5 <= enemy.x + enemy.w:
                        return enemy
            elif dino.jump_counter >= -1:
                if dino.y + dino.h - 5 >= enemy.y:
                    if enemy.x <= dino.x + dino.w - 31 <= enemy.x + enemy.w:
                        return enemy
            else:
                if dino.y + dino.h - 10 >= enemy.y:
                    if enemy.x <= dino.x + 5 <= enemy.x + enemy.w:
                        return enemy
    return False

def game_over():
    stopped_game = True
    list_of_records = []
    with open(r'Materials/data/table_of_records.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=':', quotechar='"')
        for row in reader:
            if row:
                list_of_records.append(row)
    list_of_records.append([player, scores])
    list_of_records.sort(key=lambda el: int(el[1]), reverse=True)
    with open(r'Materials/data/table_of_records.csv', 'w', newline='') as csvfile:
        writer = csv.writer(
            csvfile, delimiter=':', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for el in list_of_records[:10]:
            writer.writerow(el)
    while stopped_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                return True
            if keys[pygame.K_ESCAPE]:
                return False
        print_text('Game over. Press ENTER to play again, ESC to exit...', 30, 300)
        pygame.display.update()
        clock.tick(15)
    return True

def score(enemies):
    global scores

    for enemy in enemies:
        if dino.x >= enemy.x + enemy.w + 1 and not enemy.made_jump:
            enemy.made_jump = True
            scores += 1

def draw_health(healths):
    x = 5
    for i in range(healths):
        screen.blit(health_img, (x, 5))
        x += 35

def continue_game():
    pass


if __name__ == '__main__':
    player = ''
    rec = False
    show = True
    maps = False
    inp = False
    run_game = True
    user = False
    while run_game:
        pygame.init()

        pygame.display.set_caption('Беги Дино!')

        img = pygame.image.load(r'Materials/dinosaur.png')
        pygame.display.set_icon(img)

        pygame.mixer.music.load(r'Materials/Sounds/background.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        size = width, height = 800, 600
        screen = pygame.display.set_mode(size)
        screen.fill(pygame.Color('white'))

        jump_sound = pygame.mixer.Sound(r'Materials/Sounds/jump.mp3')
        fall_sound = pygame.mixer.Sound(r'Materials/Sounds/fall.mp3')
        collision_sound = pygame.mixer.Sound(r'Materials/Sounds/Bdish.wav')
        over_game_sound = pygame.mixer.Sound(r'Materials/Sounds/loss.wav')
        btn_sound = pygame.mixer.Sound(r'Materials/Sounds/button.wav')
        back_btn = Button(100, 65)
        user_w, user_h = 70, 100
        user_x, user_y = width // 5, height - 100 - user_h

        clock = pygame.time.Clock()

        menu_background = pygame.image.load(r'Materials/Backgrounds/Menu.jpg')

        if show:
            show_menu()

        if num_dino == 1:
            dino_img = [pygame.image.load(r'Materials/Dino/Dino0.png'),
                        pygame.image.load(r'Materials/Dino/Dino1.png'),
                        pygame.image.load(r'Materials/Dino/Dino2.png'),
                        pygame.image.load(r'Materials/Dino/Dino3.png'),
                        pygame.image.load(r'Materials/Dino/Dino4.png')]
        else:
            dino_img = [pygame.image.load(r'Materials/Dino/Dino2_0.png'),
                        pygame.image.load(r'Materials/Dino/Dino2_1.png'),
                        pygame.image.load(r'Materials/Dino/Dino2_2.png'),
                        pygame.image.load(r'Materials/Dino/Dino2_3.png'),
                        pygame.image.load(r'Materials/Dino/Dino2_4.png')]
        dino = Dino(user_x, user_y, 70, 100, dino_img, False)

        make_jump = False

        enemies_arr = []
        enemies_img = [(pygame.image.load(r'Materials/Objects/Cactus0.png'), 69, 51),
                       (pygame.image.load(r'Materials/Objects/Cactus1.png'), 37, 90),
                       (pygame.image.load(r'Materials/Objects/Cactus2.png'), 40, 80)]
        speed = 4
        for_speed = 0
        creat_enemies(enemies_arr, speed)
        if num_land == 1:
            land = pygame.image.load(r'Materials/Backgrounds/Land.jpg')
        elif num_land == 2:
            land = pygame.image.load(r'Materials/Backgrounds/Land2.jpg')
        else:
            land = pygame.image.load(r'Materials/Backgrounds/LandLevel.jpg')

        clouds = [[pygame.image.load(r'Materials/Objects/Cloud0.png'), 69, 51],
                  [pygame.image.load(r'Materials/Objects/Cloud1.png'), 37, 90]]
        true = False
        make_cloud = 1
        speed_cloud = 2

        running = True

        scores = 0

        health_img = pygame.image.load(r'Materials/Effects/heart.png')
        health_img = pygame.transform.scale(health_img, (30, 30))
        healths = 3

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    run_game = False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    dino.make_jump = True
                if keys[pygame.K_ESCAPE]:
                    running = paused()
                    run_game = running
            screen.blit(land, (0, 0))
            if dino.make_jump:
                dino.jump()
                dino.draw_dino_jump()
                score(enemies_arr)
            else:
                dino.draw_dino()
            if make_cloud:
                make_cloud = randint(0, 2)
            if not make_cloud and not true:
                cloud = Cloud(width + 100, 100, speed_cloud, choice(clouds))
                true = True
            if not make_cloud and true:
                cloud.draw_cloud()
                true = cloud.check
            print_text('Jump: SPACE', 5, 539)
            print_text('Pause: ESC', 5, 570)
            print_text('Score: ' + str(scores), 650, 560)
            draw_array(enemies_arr)
            if scores // 15 > for_speed:
                for_speed = scores // 15
                for enemy in enemies_arr:
                    enemy.v += 1
                    enemy.koef += 1
            if not dino.make_collision:
                collision = check_collision(enemies_arr)
                if collision:
                    if not collision.crash:
                        healths -= 1
                        dino.make_collision = True
                        pygame.mixer.Sound.play(collision_sound)
                        collision.crash = True
                    if healths == 0:
                        pygame.mixer.music.stop()
                        pygame.mixer.Sound.play(over_game_sound)
                        over = game_over()
                        if not over:
                            run_game = False
                            running = False
                        else:
                            running = False
                    else:
                        continue_game()
            draw_health(healths)
            pygame.display.update()
            clock.tick(60)
    pygame.quit()