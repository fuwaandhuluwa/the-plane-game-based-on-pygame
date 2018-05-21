import pygame
import sys
import traceback
import backgroundload
import promptsound
import aircraftimage
import bullet
import random
import enemy
import math
import fighter

class AircraftWar:
    EIXT = False#游戏是否退出
    GAMEOVER = False#游戏是否结束
    LAUNCHBULLET = True#战机发是否处于战斗状态
    our_bullets = []#子弹列表
    enemys = []#敌机列表
    enemys_img = [aircraftimage.enemy1_down1, aircraftimage.enemy1_down2, aircraftimage.enemy1_down3, aircraftimage.enemy1_down4]
    START = True#是否是游戏初始化，用于放置初始战机的位置

    fighter_img = aircraftimage.me1
    shield_img = aircraftimage.shield01
    shield_position = (0, 0)
    our_fighter = fighter.Fighter(fighter_img, shield_position)
    fighters = []
    fighterposition = (0, 0)#战机位置
    me1_rect = (0, 0, 0, 0)#战机的矩形
    fighter_move_speed = [0, 0]#键盘控制战机的移动速度
    SHIELD = False #防护罩是否开启

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.bgsize = self.width, self.height = 520, 600
        self.screen = pygame.display.set_mode(self.bgsize)
        self.title = pygame.display.set_caption('飞机大战', 'icon/title_icon.jpg')

        #设置背景音乐
        pygame.mixer.music.load('sound/game_music.ogg')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

        self.clock = pygame.time.Clock()

        #设置鼠标图标
        self.mouse_iocn = pygame.image.load('icon/hand_meitu_2.png').convert()
        self.mouse_iocn.set_colorkey((255, 255, 255))
        #pygame.mouse.set_visible(False)

    def event_processing(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.GAMEOVER = True
                if event.key == pygame.K_UP:
                    self.fighter_move_speed = [0, -10]
                if event.key == pygame.K_DOWN:
                    self.fighter_move_speed = [0, 10]
                if event.key == pygame.K_LEFT:
                    self.fighter_move_speed = [-10, 0]
                if event.key == pygame.K_RIGHT:
                    self.fighter_move_speed = [10, 0]
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.fighter_move_speed = [0, 0]
                if event.key == pygame.K_DOWN:
                    self.fighter_move_speed = [0, 0]
                if event.key == pygame.K_LEFT:
                    self.fighter_move_speed = [0, 0]
                if event.key == pygame.K_RIGHT:
                    self.fighter_move_speed = [0, 0]

    def background_fill(self):
        self.screen.blit(backgroundload.background_2, (0, 0))

    '''己方战机'''
    def fighter(self):
        if self.START:#初始化战机的位置在中心
            self.me1_rect = aircraftimage.me1.get_rect()
            self.fighterposition = ((self.width - self.me1_rect.width) // 2, self.height - self.me1_rect.height)
            self.me1_rect.center = (self.width // 2, self.height - self.me1_rect.height // 2)
            self.our_fighter.rect = self.me1_rect
            self.our_fighter.rect.center = self.me1_rect.center
            self.fighters.append(self.our_fighter)
            self.START = False
        else:
            self.me1_rect = self.me1_rect.move(self.fighter_move_speed)
            if self.me1_rect.top > self.height - self.me1_rect.height:
                self.me1_rect.top = self.height - self.me1_rect.height
            if self.me1_rect.left + self.me1_rect.width > self.width:
                self.me1_rect.left = self.width - self.me1_rect.width
            if self.me1_rect.top < 0:
                self.me1_rect.top = 0
            if self.me1_rect.left < 0:
                self.me1_rect.left = 0
            self.fighterposition = (self.me1_rect.left, self.me1_rect.top)
            self.our_fighter.rect = self.me1_rect

        for each in self.fighters:
            self.screen.blit(each.image, self.fighterposition)
        if len(self.fighters) == 0:
            self.LAUNCHBULLET = False
        if self.SHIELD:
            self.shield_position = (self.me1_rect.left - self.me1_rect.width //4, self.me1_rect.top - self.me1_rect.height //8)
            self.our_fighter = fighter.Fighter(self.shield_img, self.shield_position)
            self.screen.blit(self.shield_img, self.shield_position)
        bullet_position = (self.fighterposition[0] + self.me1_rect.width // 2, self.fighterposition[1])
        speed = [0, -40]
        bullet_img = aircraftimage.bullet3
        if self.LAUNCHBULLET:
            self.launch_bullet(bullet_img, bullet_position, speed)

    '''敌方战机'''
    def enemy_fighters(self):
        if random.randint(0,5) == 1:
            position = (random.randint(1, self.width), 0)
            self.screen.blit(aircraftimage.enemy1, position)
            enemy_img = aircraftimage.enemy1
            speed = [0, 5]
            enemy_obj = enemy.Enemy(enemy_img, position, speed, self.bgsize)
            self.enemys.append(enemy_obj)

        for each in self.enemys:
            if each.move():
                self.screen.blit(each.image, (each.rect[0], each.rect[1]))
            else:
                self.enemys.remove(each)

    '''检测子弹与战机是否碰撞'''
    def detect_collision(self, source, destination, dest_img):
        source_need_remove = []
        destination_need_remove = []
        for i in source:
            for j in destination:
                if (math.sqrt((i.rect.center[0] - j.rect.center[0]) ** 2 + (i.rect.center[1] - j.rect.center[1]) ** 2) < i.rect.height // 2 + j.rect.height // 2):
                    source_need_remove.append(i)
                    j.collide_count += 1
                    if j.collide_count < len(dest_img) + 1:
                        j.image = dest_img[j.collide_count - 1]
                    elif j.collide_count == len(dest_img) + 1:
                        destination_need_remove.append(j)
        for each in source_need_remove:
            try:
                source.remove(each)
            except:#这里抛出异常的原因是，这个子弹已经被我在launch_bullet函数里处理掉了，一旦子弹超出屏幕我就会处理掉
                pass
        for each in destination_need_remove:
            destination.remove(each)

    '''检测战机与敌机是否碰撞'''
    def detect_fighter_enemy_collision(self,  source, destination, dest_img):
        source_need_remove = []
        destination_need_remove = []
        for i in source:
            for j in destination:
                if (i.rect.left > j.rect.left  and i.rect.left + i.rect.width < j.rect.left + j.rect.width) and \
                        (i.rect.top > j.rect.top and i.rect.top + i.rect.height < j.rect.top + j.rect.height):
                    source_need_remove.append(i)
                    j.collide_count += 1
                    if j.collide_count < len(dest_img) + 1:
                        j.image = dest_img[j.collide_count - 1]
                    else:
                        destination_need_remove.append(j)
        for each in source_need_remove:
            try:
                source.remove(each)
            except:
                pass
        for each in destination_need_remove:
            destination.remove(each)

    '''发射子弹'''
    def launch_bullet(self,bullet_img, position, speed):
        bullet_obj = bullet.Bullet(bullet_img, position, speed, self.bgsize)
        self.our_bullets.append(bullet_obj)
        for each in self.our_bullets:
            if each.move():
                self.screen.blit(each.image, (each.rect[0], each.rect[1]))
            else:
                self.our_bullets.remove(each)

    def run(self):
        while not self.EIXT:
            self.event_processing()
            self.background_fill()

            self.fighter()
            self.enemy_fighters()
            self.detect_collision(self.our_bullets, self.enemys, self.enemys_img)
            if not self.SHIELD:
                self.detect_fighter_enemy_collision( self.enemys, self.fighters, [aircraftimage.me_destroy_1, aircraftimage.me_destroy_2, aircraftimage.me_destroy_3,aircraftimage.me_destroy_4])
            else:
                pass


            if self.LAUNCHBULLET:
                promptsound.bullet.play()
                promptsound.bullet.set_volume(0.1)

            if self.GAMEOVER:
                position = pygame.mouse.get_pos()
                self.screen.blit(self.mouse_iocn, position)
                promptsound.me_down.play()
                promptsound.me_down.set_volume(0.4)
                self.LAUNCHBULLET = False
                self.GAMEOVER = False

            #检查背景音乐是否在播放,如果没有播放则开启播放
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()

            pygame.display.update()
            self.clock.tick(20)


if __name__ == '__main__':
    try:
        aircraft = AircraftWar()
        aircraft.run()
    except SystemExit:
        pass
    except Exception as e:
        print(e)
        pygame.quit()
