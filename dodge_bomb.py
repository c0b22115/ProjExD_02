import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1200, 600

delta = {
    pg.K_UP: (0, -5), 
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し、真理値タプルを返す関数
    引数 rct:こうかとんor爆弾SurfaceのRect
    戻り値:横横行、縦方向判定結果(画面内:True/画面外:False)
    """
    
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:#横方向はみだし判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:#縦方向はみだし判定
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))#練習１:透明のSurfaceをつくる
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()#練習２　爆弾Surfaceを作る
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5

    kk_zis = {
        (5, 0):pg.transform.rotozoom(kk_img, 0, 1.0),
        (5, -5):pg.transform.rotozoom(kk_img, 316, 1.0),
        (0, -5):pg.transform.rotozoom(kk_img, 270, 1.0),
        (-5, -5):pg.transform.rotozoom(kk_img, 315, 1.0),
        (-5, 0):pg.transform.rotozoom(kk_img, 0, 1.0),
        (-5, 5):pg.transform.rotozoom(kk_img, 45, 1.0),
        (0, 5):pg.transform.rotozoom(kk_img, 90, 1.0),
        (5, 5):pg.transform.rotozoom(kk_img, 45, 1.0)
    }
    accs = [a for a in range(1, 100)]
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):
            print("Game Over")
            return
            
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:#キーが押されたら
               sum_mv[0] += tpl[0]
               sum_mv[1] += tpl[1]

        

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        """
        演習課題１のための
        """
        if(sum_mv[0] >= 5):
            kk_img = pg.transform.flip(kk_img, False, True)
        if sum_mv != [0, 0]:
            kk_img = kk_zis[tuple(sum_mv)]
            if sum_mv[0] >= 5:
                kk_img = pg.transform.flip(kk_img, True, False)

        screen.blit(kk_img, kk_rct)
        avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)#練習２:爆弾を移動させる
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()