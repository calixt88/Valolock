import tkinter as tk
import pyautogui
from tkinter import ttk
from PIL import Image, ImageTk
import time
import os

# Set dimensions
WIDTH = int(1920 * 0.5)
HEIGHT = int(1080 * 0.55)


# Function to quit the application
def quit_app():
    root.destroy()


# Function to lock in the selected agent
def lock_in(image_path):
    print(f"Locked in with image: {image_path}")
    found_agent = False

    time.sleep(5)

    while not found_agent:
        locate_agent = pyautogui.locateOnScreen(image_path, grayscale=False, confidence=.75)
        print(locate_agent)
        if locate_agent is not None:
            found_agent = True
            print("Found an Agent, Starting lock in process")
            for i in range(15):
                if pyautogui.locateOnScreen(image_path, grayscale=False, confidence=.75) is not None:
                    agent_location = pyautogui.center(locate_agent)
                    agentx, agenty = agent_location
                    pyautogui.moveTo(agentx, agenty)
                    pyautogui.click()
                    locate_lockIn = pyautogui.locateOnScreen("Assests/lockin.PNG", grayscale=False, confidence=.75)
                    if locate_lockIn is not None:
                        lockIn_location = pyautogui.center(locate_lockIn)
                        lockInx, lockIny = lockIn_location
                        pyautogui.moveTo(lockInx, lockIny)
                        pyautogui.click()
                    else:
                        print("Couldn't find the lock in button, going to try to move to it manually.")
                        print(pyautogui.position())
                        pyautogui.moveTo(972, 799)
                        pyautogui.click()
                else:
                    print("Can't seem to find the agent you're looking for.")


# Function to update the agentSelectedLabel image and store the image path
def update_agent_image(image, image_path):
    # Resize the image using Pillow
    image = image.resize((125, 125), Image.ANTIALIAS)
    resized_image = ImageTk.PhotoImage(image)
    agentSelectedLabel.configure(image=resized_image)
    agentSelectedLabel.image = resized_image
    agentSelectedLabel.image_path = image_path  # Store the image path


root = tk.Tk()
root.title("Valorant Instalock")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.configure(bg="grey")
root.iconbitmap("Assests/icon.ico")

# Create label at the top middle
label = ttk.Label(root, text="Agent Selected", background="grey", font=("Helvetica", 14, "bold"))
label.place(relx=0.5, rely=0.05, anchor="center")

agentSelectedLabel = ttk.Label(root, background="grey")
agentSelectedLabel.place(relx=0.5, rely=0.2, anchor="center", height=125, width=125)

# Create a grid of 22 buttons
grid_frame = ttk.Frame(root)
grid_frame.place(relx=0.5, rely=0.57, anchor="center")

num_rows = 3
num_columns = 8
agents = [f"Agent {i + 1}" for i in range(21)]

current_dir = os.path.dirname(os.path.realpath(__file__))

for i in range(num_rows):
    for j in range(num_columns):
        index = i * num_columns + j
        if index < len(agents):
            # Load image
            image_path = ("Assests/" + f'agent{index + 1}.png')
            img = Image.open(image_path)
            agent_image = ImageTk.PhotoImage(img)
            btn = tk.Button(grid_frame, image=agent_image, compound="top",
                            command=lambda img=img, img_path=image_path: update_agent_image(img, img_path))
            btn.agent_image = agent_image  # Store a reference to the image to prevent garbage collection
            btn.grid(row=i, column=j, padx=3, pady=3)

# Create "Lock In" button below the grid
lock_in_btn = tk.Button(root, text="Lock In", bg="lightgreen", fg="white", font=("Helvetica", 14, "bold"),
                        command=lambda: lock_in(agentSelectedLabel.image_path))
lock_in_btn.place(relx=0.5, rely=0.9, anchor="center", height=50, width=150)

root.mainloop()
