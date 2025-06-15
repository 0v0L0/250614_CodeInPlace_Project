import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np
import tkinter as tk

# Color palette
color_palette = ["paleturquoise", "powderblue", "lightskyblue", "skyblue", "lightsteelblue"]
snowflake_color = None

# Parameter ranges and values
layer_ranges = {
    "hex_size": (35.0, 45.0),
    "arm_length": (40.0, 70.0),
    "facet_length": (15.0, 35.0),
    "tip_length": (15.0, 20.0)
}
layer_values = {}

# Global state
click_x = None
click_y = None
center_point = None
animations = []

# Stage labels
stage_labels = [
    "Ice crystals condense around a tiny particle",
    "Condensing water forms a prism with facets",
    "Branching begins",
    "Facets form on branches",
    "And so on... (Ref: https://scijinks.gov/snowflakes/)"
]

# Set up the plot
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, 600)
ax.set_ylim(0, 600)
ax.set_aspect('equal')
ax.invert_yaxis()
ax.axis('off')
ax.set_title("Click to define snowflake center")

# Drawing stages
def draw_stage_1(cx, cy):
    dot = patches.Circle((cx, cy), radius=2.5, color=snowflake_color)
    ax.add_patch(dot)

def draw_stage_2(cx, cy, hex_size):
    hexagon = [(cx + hex_size * np.cos(np.pi / 3 * i),
                cy + hex_size * np.sin(np.pi / 3 * i)) for i in range(6)]
    hex_patch = patches.Polygon(hexagon, closed=True, fill=False, edgecolor=snowflake_color, linewidth=2)
    ax.add_patch(hex_patch)

def draw_stage_3(cx, cy, arm_length):
    for i in range(6):
        angle = np.pi / 3 * i
        x_end = cx + arm_length * np.cos(angle)
        y_end = cy + arm_length * np.sin(angle)
        ax.plot([cx, x_end], [cy, y_end], color=snowflake_color, linewidth=1.5)

def draw_stage_4(cx, cy, arm_length, facet_length):
    for i in range(6):
        angle = np.pi / 3 * i
        base_x = cx + arm_length * np.cos(angle)
        base_y = cy + arm_length * np.sin(angle)
        for offset in [-np.pi / 12, np.pi / 12]:
            sub_angle = angle + offset
            x_tip = base_x + facet_length * np.cos(sub_angle)
            y_tip = base_y + facet_length * np.sin(sub_angle)
            ax.plot([base_x, x_tip], [base_y, y_tip], color=snowflake_color, linewidth=1.5)

def draw_stage_5(cx, cy, arm_length, facet_length, tip_length):
    for i in range(6):
        angle = np.pi / 3 * i
        base_x = cx + arm_length * np.cos(angle)
        base_y = cy + arm_length * np.sin(angle)
        for offset in [-np.pi / 12, np.pi / 12]:
            sub_angle = angle + offset
            mid_x = base_x + facet_length * np.cos(sub_angle)
            mid_y = base_y + facet_length * np.sin(sub_angle)
            for tip_offset in [-np.pi / 24, np.pi / 24]:
                tip_angle = sub_angle + tip_offset
                x_tip = mid_x + tip_length * np.cos(tip_angle)
                y_tip = mid_y + tip_length * np.sin(tip_angle)
                ax.plot([mid_x, x_tip], [mid_y, y_tip], color=snowflake_color, linewidth=1)

def init():
    ax.clear()
    ax.set_xlim(0, 600)
    ax.set_ylim(0, 600)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.axis('off')
    return []

def update(frame):
    init()
    cx, cy = center_point
    if frame >= 0:
        draw_stage_1(cx, cy)
    if frame >= 1:
        draw_stage_2(cx, cy, layer_values["hex_size"])
    if frame >= 2:
        draw_stage_3(cx, cy, layer_values["arm_length"])
    if frame >= 3:
        draw_stage_4(cx, cy, layer_values["arm_length"], layer_values["facet_length"])
    if frame >= 4:
        draw_stage_5(cx, cy, layer_values["arm_length"], layer_values["facet_length"], layer_values["tip_length"])
    
    if 0 <= frame <= 4:
        ax.text(300, 580, stage_labels[frame], fontsize=10,
                color='grey', ha='center',
                bbox=dict(facecolor='white', edgecolor='lightgrey', boxstyle='round'))
    return []

def generate_and_draw(color):
    global center_point, animations, snowflake_color
    center_point = (click_x, click_y)
    snowflake_color = color
    ani = animation.FuncAnimation(
        fig, update, frames=5, init_func=init,
        interval=1200, repeat=False
    )
    animations.append(ani)
    fig.canvas.draw()

def launch_slider_window():
    win = tk.Toplevel()
    win.title("Snowflake Parameters")

    selected_color = tk.StringVar(win)

    tk.Label(win, text="Hex Size").pack()
    hex_slider = tk.Scale(win, from_=layer_ranges["hex_size"][0], to=layer_ranges["hex_size"][1],
                          resolution=0.5, orient=tk.HORIZONTAL)
    hex_slider.set(40)
    hex_slider.pack()

    tk.Label(win, text="Arm Length").pack()
    arm_slider = tk.Scale(win, from_=layer_ranges["arm_length"][0], to=layer_ranges["arm_length"][1],
                          resolution=1, orient=tk.HORIZONTAL)
    arm_slider.set(40)
    arm_slider.pack()

    tk.Label(win, text="Facet Length").pack()
    facet_slider = tk.Scale(win, from_=layer_ranges["facet_length"][0], to=layer_ranges["facet_length"][1],
                            resolution=0.5, orient=tk.HORIZONTAL)
    facet_slider.set(20)
    facet_slider.pack()

    tk.Label(win, text="Tip Length").pack()
    tip_slider = tk.Scale(win, from_=layer_ranges["tip_length"][0], to=layer_ranges["tip_length"][1],
                          resolution=0.5, orient=tk.HORIZONTAL)
    tip_slider.set(17.5)
    tip_slider.pack()

    # Color selection section
    tk.Label(win, text="Choose Snowflake Color").pack()

    def update_swatch():
        pass  # No preview swatch needed


    for color in color_palette:
        tk.Radiobutton(
            win,
            text=color,
            variable=selected_color,
            value=color,
            bg=color,
            fg="white",
            activebackground=color,
            selectcolor=color,         
            indicatoron=0,
            width=20,
            highlightthickness=0,      
            command=update_swatch
        ).pack(pady=1)



    selected_color.set(color_palette[0])
    update_swatch()


    def confirm():
        layer_values["hex_size"] = float(hex_slider.get())
        layer_values["arm_length"] = float(arm_slider.get())
        layer_values["facet_length"] = float(facet_slider.get())
        layer_values["tip_length"] = float(tip_slider.get())
        color = selected_color.get()
        win.destroy()
        generate_and_draw(color)

    tk.Button(win, text="Confirm", command=confirm).pack(pady=10)

def onclick(event):
    global click_x, click_y
    if event.inaxes != ax:
        return
    click_x, click_y = event.xdata, event.ydata
    launch_slider_window()

fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
