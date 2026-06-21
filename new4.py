import tkinter as tk
import random

WIDTH = 400
HEIGHT = 400
SIZE = 20

root = tk.Tk()
root.geometry("550x650")
root.title("Snake Game")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack(pady=5)

snake = [(100, 100)]
direction = "Right"

apple_x = random.randint(0, 24) * SIZE
apple_y = random.randint(0, 24) * SIZE

score = 0
game_running = True

score_label = tk.Label(root, text="Score: 0", font=("Arial", 14))
score_label.pack()


def draw():
    canvas.delete("all")

    # Draw Apple
    canvas.create_oval(
        apple_x,
        apple_y,
        apple_x + SIZE,
        apple_y + SIZE,
        fill="red"
    )

    # Draw Snake
    for i, (x, y) in enumerate(snake):

        if i == 0:  # Head
            canvas.create_oval(
                x, y,
                x + SIZE, y + SIZE,
                fill="lime",
                outline="white",
                width=2
            )

            # Eyes
            canvas.create_oval(
                x + 4, y + 5,
                x + 7, y + 8,
                fill="black"
            )

            canvas.create_oval(
                x + 13, y + 5,
                x + 16, y + 8,
                fill="black"
            )

        else:  # Body
            canvas.create_oval(
                x, y,
                x + SIZE, y + SIZE,
                fill="green",
                outline="darkgreen",
                width=2
            )


def move():
    global apple_x, apple_y, score, game_running

    if not game_running:
        return

    head_x, head_y = snake[0]

    if direction == "Right":
        head_x += SIZE
    elif direction == "Left":
        head_x -= SIZE
    elif direction == "Up":
        head_y -= SIZE
    elif direction == "Down":
        head_y += SIZE

    new_head = (head_x, head_y)

    # Wall Collision
    if (
        head_x < 0 or
        head_x >= WIDTH or
        head_y < 0 or
        head_y >= HEIGHT
    ):
        game_over()
        return

    # Self Collision
    if new_head in snake:
        game_over()
        return

    snake.insert(0, new_head)

    # Eat Apple
    if head_x == apple_x and head_y == apple_y:

        score += 1
        score_label.config(text=f"Score: {score}")

        apple_x = random.randint(0, 24) * SIZE
        apple_y = random.randint(0, 24) * SIZE

    else:
        snake.pop()

    draw()
    root.after(150, move)


def change_direction(event):
    global direction

    if event.keysym == "Left" and direction != "Right":
        direction = "Left"

    elif event.keysym == "Right" and direction != "Left":
        direction = "Right"

    elif event.keysym == "Up" and direction != "Down":
        direction = "Up"

    elif event.keysym == "Down" and direction != "Up":
        direction = "Down"


def restart_game():
    global snake, direction
    global apple_x, apple_y
    global score, game_running

    canvas.delete("all")

    snake = [(100, 100)]
    direction = "Right"

    apple_x = random.randint(0, 24) * SIZE
    apple_y = random.randint(0, 24) * SIZE

    score = 0
    game_running = True

    score_label.config(text="Score: 0")

    draw()
    move()


def game_over():
    global game_running

    game_running = False

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2,
        text="GAME OVER",
        fill="white",
        font=("Arial", 24, "bold")
    )


# Restart Button (Always Visible)
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

restart_btn = tk.Button(
    button_frame,
    text="RESTART",
    bg="green",
    fg="black",
    font=("Arial", 14, "bold"),
    command=restart_game
)

restart_btn.pack()

root.bind("<Key>", change_direction)

draw()
move()

root.mainloop()