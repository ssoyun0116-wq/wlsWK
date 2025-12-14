# -*- coding: utf-8 -*-

import tkinter as tk
import random

class MemoryShootingGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Memory Shooting Game")
        self.window.geometry("1280x720")
       
        
        # 캔버스 설정
        self.canvas = tk.Canvas(self.window, width=1280, height=720)
        self.canvas.pack()

        # 배경 이미지 로드 (self.bg_image에 저장)
        self.bg_image = tk.PhotoImage(file="grass_template2.png")  # 배경 이미지 경로
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")  # 배경 추가

        # 게임 규칙과 타이머
        self.score = 0
        self.time_left = 60  # 게임 시간 1분

        #
        self.time_text = self.canvas.create_text(640, 50, text=f"Time: {self.time_left}", fill="white", font=("Arial", 24, "bold"))
        self.score_text = self.canvas.create_text(1100, 50, text=f"Score: {self.score}", fill="white", font=("Arial", 24, "bold"))

        # 튜토리얼 텍스트 추가
        self.tutorial_text = [
            "게임 규칙 안내",
            "화살표 키로 강아지를 위아래로 움직이고,",
            "스페이스 바를 눌러서 총알을 발사하세요!",
            "적을 맞추면 점수가 올라갑니다.",
            "시간 내에 최대한 많은 적을 처치해 보세요!"
        ]
        self.current_tutorial_index = 0
        self.show_tutorial()

        # 메인 루프 시작
        self.window.mainloop()

    def show_tutorial(self):
        # 튜토리얼 화면을 표시
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 1280, 720, fill="black")  # 배경을 검은색으로

        # 튜토리얼 텍스트 띄우기
        self.canvas.create_text(640, 330, text=self.tutorial_text[self.current_tutorial_index], fill="white", font=("Arial", 24, "bold"))
        
        self.current_tutorial_index += 1
        if self.current_tutorial_index < len(self.tutorial_text):
            self.window.after(2000, self.show_tutorial)  # 2초마다 튜토리얼 메시지 변경
        else:
            self.window.after(1000, self.start_game)  # 튜토리얼 끝나면 게임 시작

    def start_game(self):
        # 게임 시작
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")  # 배경 추가

        # 게임 규칙 텍스트
        self.time_text=self.canvas.create_text(640, 50, text=f"Time: {self.time_left}", fill="white", font=("Arial", 24, "bold"))
        self.score_text=self.canvas.create_text(640, 100, text=f"Score: {self.score }", fill="white", font=("Arial", 24, "bold"))
        
        # 플레이어 (강아지) 설정
        self.dog_img = tk.PhotoImage(file="강아지 서있음.png")  # 강아지 이미지
        self.dog = self.canvas.create_image(100, 600, image=self.dog_img)
        
        # 적 설정
        self.enemies = []
        self.enemy_speed = 2  # 초기 적 속도

        # 총알 설정
        self.bullets = []
        self.bullet_speed = 15

        # 타이머 시작
        self.update_timer()

        # 키 입력 처리
        self.keys = set()
        self.window.bind("<KeyPress>", self.keyPressHandler)
        self.window.bind("<KeyRelease>", self.keyReleaseHandler)

        # 스페이스 키 눌림 확인 변수 추가
        self.space_pressed = False  # 이 줄을 추가


        # 게임 시작
        self.spawn_enemy()
        self.update_game()

        # 메인 루프 시작
        self.window.mainloop()

    # 타이머 갱신
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.canvas.itemconfig(self.time_text, text=f"Time: {self.time_left}")
            self.window.after(1000, self.update_timer)  # 1초마다 갱신
        else:
            self.end_game()

    # 게임 종료
    def end_game(self):
        self.canvas.delete("all")
        self.canvas.create_text(640, 300, text="게임 종료!", fill="white", font=("Arial", 40, "bold"))
        self.canvas.create_text(640, 400, text=f"최종 점수: {self.score}", fill="white", font=("Arial", 30, "bold"))

    # 키 입력 처리
    def keyPressHandler(self, event):
        if event.keysym == "space" and not self.space_pressed:
            self.shoot_bullet()
            self.space_pressed = True  # 스페이스 키가 눌렸으면 플래그 설정

        self.keys.add(event.keysym)

    def keyReleaseHandler(self, event):
        if event.keysym in self.keys:
            self.keys.remove(event.keysym)

        if event.keysym == "space":
            self.space_pressed = False  # 스페이스 키를 떼면 플래그 초기화

    # 총알 발사
    def shoot_bullet(self):
        bullet_img = tk.PhotoImage(file="ball1.png")  # 총알 이미지
        x, y = self.canvas.coords(self.dog)  # 강아지의 좌표
        bullet = self.canvas.create_image(x + 50, y, image=bullet_img)  # 총알 위치
        self.bullets.append((bullet, bullet_img))  # (총알 객체, 총알 이미지) 추가
        self.bullet_img = bullet_img  # 총알 이미지 객체를 인스턴스 변수로 저장 (필요시 사용)

    # 적 생성
    def spawn_enemy(self):
        enemy_img = tk.PhotoImage(file="baseball_mitt.png")  # 적 이미지
        y = random.randint(50, 650)  # 적의 y좌표를 랜덤으로 설정
        enemy = self.canvas.create_image(1280, y, image=enemy_img)  # 적의 초기 x좌표
        self.enemies.append((enemy, enemy_img))  # (적 객체, 적 이미지) 추가
        self.window.after(random.randint(1000, 2000), self.spawn_enemy)  # 1~2초마다 적 생성

    # 게임 루프
    def update_game(self):
        if "Up" in self.keys:
            self.canvas.move(self.dog, 0, -5)
        if "Down" in self.keys:
            self.canvas.move(self.dog, 0, 5)

        # 총알 이동
        for bullet, img in self.bullets[:]:
            self.canvas.move(bullet, self.bullet_speed, 0)  # 총알을 오른쪽으로 이동
            x, y = self.canvas.coords(bullet)
            if x > 1280:  # 화면 밖으로 나가면 총알 삭제
                self.canvas.delete(bullet)
                self.bullets.remove((bullet, img))

        # 적 이동
        for enemy, img in self.enemies[:]:
            self.canvas.move(enemy, -self.enemy_speed, 0)  # 적을 왼쪽으로 이동
            ex, ey = self.canvas.coords(enemy)
            if ex < 0:  # 화면 밖으로 나가면 적 삭제
                self.canvas.delete(enemy)
                self.enemies.remove((enemy, img))

        # 충돌 체크
        for bullet, b_img in self.bullets[:]:
            bx, by = self.canvas.coords(bullet)
            for enemy, e_img in self.enemies[:]:
                ex, ey = self.canvas.coords(enemy)
                if abs(bx - ex) < 50 and abs(by - ey) < 50:  # 충돌 범위 내에서 충돌 확인
                    self.canvas.delete(bullet)
                    self.canvas.delete(enemy)
                    self.bullets.remove((bullet, b_img))
                    self.enemies.remove((enemy, e_img))
                    self.score += 10
                    self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

        # 적의 속도를 점차적으로 증가시킴
        self.enemy_speed += 0.025

        # 계속해서 게임 업데이트
        self.window.after(33, self.update_game) 

# 게임 시작
if __name__ == "__main__":
    game = MemoryShootingGame()


