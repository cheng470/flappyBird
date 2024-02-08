import random

WIDTH = 138*4
HEIGHT = 396
SPEED = 3 # 背景滚动速度
GAP = 150 # 上水管与下水管的间隙
GRAVITY = 0.2 # 重力加速度
FLAP_VELOCITY = -5 # 小鸟飞的初始速度

score = 0
score_flag = False
started = False
backgrounds = []
for i in range(5):
    backgrounds.append(Actor("flappybird_background", topleft=(i*138, 0)))
ground = Actor("flappybird_ground", bottomleft=(0, HEIGHT))

pipe_top = Actor("flappybird_top_pipe")
pipe_bottom = Actor("flappybird_bottom_pipe")

bird = Actor("flappybird1", (WIDTH//2, HEIGHT//2))
bird.vy = 0
bird.dead = False

gui_title = Actor("flappybird_title", (WIDTH//2, 72))
gui_ready = Actor("flappybird_get_ready", (WIDTH//2, 204))
gui_start = Actor("flappybird_start_button", (WIDTH//2, 245))
gui_over = Actor("flappybird_game_over", (WIDTH//2, HEIGHT//2))


def check_collision():
    if bird.colliderect(ground):
        sounds.fall.play()
        bird.dead = True
    if bird.colliderect(pipe_top) or bird.colliderect(pipe_bottom):
        sounds.collide.play()
        bird.dead = True
        music.stop()

def fly():
    global score, score_flag
    if score_flag and bird.x > pipe_top.right:
        score += 1
        score_flag = False
    bird.vy += GRAVITY
    bird.y += bird.vy
    if bird.top < 0:
        bird.top = 0

# 飞行动画实现
anim_counter = 0
def animation():
    global anim_counter
    anim_counter += 1
    if anim_counter == 4:
        bird.image = "flappybird1"
    elif anim_counter == 8:
        bird.image = "flappybird2"
    elif anim_counter == 12:
        bird.image = "flappybird3"
    elif anim_counter == 16:
        bird.image = "flappybird2"
        anim_counter = 0

def reset_pipes():
    global score_flag
    score_flag = True
    pipe_top.bottom = random.randint(50, 150)
    pipe_bottom.top = pipe_top.bottom + GAP
    pipe_top.left = WIDTH
    pipe_bottom.left = WIDTH
    #print("reset pipes")
reset_pipes()

def update_pipes():
    pipe_top.x -= SPEED
    pipe_bottom.x -= SPEED
    if pipe_top.right < 0:
        reset_pipes()

def update_background():
    for b in backgrounds:
        b.x -= SPEED
        if b.right <= 0:
            b.left = WIDTH

def update_ground():
    ground.x -= SPEED
    if ground.right < WIDTH:
        ground.left = 0

def draw():
    for b in backgrounds:
        b.draw()
    if not started:
        gui_title.draw()
        gui_ready.draw()
        gui_start.draw()
        return
    ground.draw()
    pipe_top.draw()
    pipe_bottom.draw()
    bird.draw()
    screen.draw.text(str(score), topleft=(30, 30), fontsize=30)
    if bird.dead:
        gui_over.draw()

def update():
    if not started:
        return
    if bird.dead:
        return
    update_background()
    update_ground()
    update_pipes()
    fly()
    animation()
    check_collision()

def on_mouse_down(pos):
    global started
    if bird.dead:
        return
    if started:
        bird.vy = FLAP_VELOCITY
        sounds.flap.play()
    elif gui_start.collidepoint(pos):
        started = True
        music.play("flappybird")
        #reset_pipes()
