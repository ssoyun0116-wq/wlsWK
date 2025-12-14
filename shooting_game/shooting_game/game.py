import tkinter as tk
import random


class MemoryShootingGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Memory Shooting Game")
        self.window.geometry("3840x2160")

        
        self.canvas = tk.Canvas(self.window, width=3840, height=2160)
        self.canvas.pack()

       
        self.bg_image = tk.PhotoImage(file="grass_template2.png")
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        
        self.score = 0
        self.time_left = 30
        self.game_running = False

        
        self.time_text = self.canvas.create_text(
            1000, 2000, text=f"Time: {self.time_left}",
            fill="white", font=("Arial", 24, "bold")
        )
        self.score_text = self.canvas.create_text(
            1100, 2000, text=f"Score: {self.score}",
            fill="white", font=("Arial", 24, "bold")
        )

        
        self.tutorial_text = [
            "게임 규칙 안내",
            "화살표 키로 강아지를 위아래로 움직이고,",
            "스페이스 바로 뼈를 발사하여 강아지를 도와주세요",
            "적을 맞추면 점수가 올라갑니다.",
            "시간 내에 최대한 많이 처치하세요!"
        ]
        self.current_tutorial_index = 0
        self.show_tutorial()

        
        self.keys = set()
        self.space_pressed = False
        self.window.bind("<KeyPress>", self.keyPressHandler)
        self.window.bind("<KeyRelease>", self.keyReleaseHandler)

        self.window.mainloop()

   
    def show_tutorial(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 3840, 2160, fill="black")
        self.canvas.create_text(
            1000, 450,
            text=self.tutorial_text[self.current_tutorial_index],
            fill="white", font=("Arial", 24, "bold")
        )

        self.current_tutorial_index += 1
        if self.current_tutorial_index < len(self.tutorial_text):
            self.window.after(2000, self.show_tutorial)
        else:
            self.window.after(1000, self.start_game)

   
    def start_game(self):
        self.game_running = True
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        self.time_text = self.canvas.create_text(
            1000, 50, text=f"Time: {self.time_left}",
            fill="white", font=("Arial", 24, "bold")
        )
        self.score_text = self.canvas.create_text(
            1000, 100, text=f"Score: {self.score}",
            fill="white", font=("Arial", 24, "bold")
        )

       
        self.dog_img = tk.PhotoImage(file="dog.png")
        self.dog = self.canvas.create_image(100, 600, image=self.dog_img)

        
        self.bullets = []
        self.enemies = []
        self.enemy_speed = 2
        self.bullet_speed = 10

        self.update_timer()
        self.spawn_enemy()
        self.update_game()


    
    def update_timer(self):
        if not self.game_running:
            return

        if self.time_left > 0:
            self.time_left -= 1
            self.canvas.itemconfig(self.time_text, text=f"Time: {self.time_left}")
            self.window.after(1000, self.update_timer)
        else:
            self.show_ending_screen()

    
    def show_ending_screen(self):
        self.game_running = False
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 3860, 2160, fill="black")

        self.canvas.create_text(
            1000, 350, text="GAME OVER",
            fill="white", font=("Arial", 48, "bold")
        )
        self.canvas.create_text(
            1000, 450, text=f"최종 점수: {self.score}",
            fill="white", font=("Arial", 36, "bold")
        )
        self.canvas.create_text(
            1000, 550, text="플레이해 주셔서 감사합니다!",
            fill="white", font=("Arial", 24)
        )

    
    def keyPressHandler(self, event):
        if not self.game_running:
            return

        self.keys.add(event.keysym)

        if event.keysym == "space" and not self.space_pressed:
            self.shoot_bullet()
            self.space_pressed = True

    def keyReleaseHandler(self, event):
        if event.keysym in self.keys:
            self.keys.remove(event.keysym)

        if event.keysym == "space":
            self.space_pressed = False

    
    def shoot_bullet(self):
        bullet_img = tk.PhotoImage(file="femur.png")
        x, y = self.canvas.coords(self.dog)
        bullet = self.canvas.create_image(x + 50, y, image=bullet_img)
        self.bullets.append((bullet, bullet_img))


    
    def spawn_enemy(self):
        if not self.game_running:
            return

        enemy_img = tk.PhotoImage(file="Ghost.png")
        y = random.randint(50, 1600)
        enemy = self.canvas.create_image(1900, y, image=enemy_img)
        self.enemies.append((enemy, enemy_img))

        self.window.after(random.randint(1000, 2000), self.spawn_enemy)

    
    def update_game(self):
        if not self.game_running:
            return

        if "Up" in self.keys:
            self.canvas.move(self.dog, 0, -5)
        if "Down" in self.keys:
            self.canvas.move(self.dog, 0, 5)

        
        for bullet, img in self.bullets[:]:
            x, y = self.canvas.coords(bullet)
            self.canvas.move(bullet, self.bullet_speed, 0)
            if x > 2000:
                self.canvas.delete(bullet)
                self.bullets.remove((bullet, img))

        
        for enemy, img in self.enemies[:]:
            ex, ey = self.canvas.coords(enemy)
            self.canvas.move(enemy, -self.enemy_speed, 0)
            if ex < 0:
                self.canvas.delete(enemy)
                self.enemies.remove((enemy, img))

        
        for bullet, b_img in self.bullets[:]:
            bx, by = self.canvas.coords(bullet)
            for enemy, e_img in self.enemies[:]:
                ex, ey = self.canvas.coords(enemy)
                if abs(bx - ex) < 50 and abs(by - ey) < 50:
                    self.canvas.delete(bullet)
                    self.canvas.delete(enemy)
                    self.bullets.remove((bullet, b_img))
                    self.enemies.remove((enemy, e_img))
                    self.score += 10
                    self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
                    break

        self.enemy_speed += 0.02
        self.window.after(33, self.update_game)


if __name__ == "__main__":
    MemoryShootingGame()
