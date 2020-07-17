from tkinter import *
import models
import math


# Window class
class Window(Tk):
    def __init__(self, *args, **kwargs):
        # Initialize the window
        super().__init__(*args, **kwargs)

        # Set window settings
        self.title("Charges and Fields")
        self.resizable(0, 0)

        # Set window display settings
        # Radius of particle
        self.particle_rad = 10
        # Config sizing
        self.config_width = 800
        self.config_height = 600
        # Config arrow display type
        self.direction_only = IntVar()
        self.field_displayed = IntVar()
        self.scale_displayed = IntVar()
        self.grid_displayed = IntVar()

        # Load default particles
        p1 = models.Particle(100, 300, 1e-9)
        p2 = models.Particle(700, 300, -1e-9)
        self.system = models.System([p1, p2], 200)

        # Instantiate widgets
        self.canvas = Canvas(self, width=self.config_width, height=self.config_height, bg="black", bd=0, highlightthickness=0)
        self.info_frame = InfoFrame(self.system,
            (self.direction_only, self.field_displayed, self.scale_displayed, self.grid_displayed),
            (self.add_pos_particle, self.add_neg_particle, self.delete_mode, self.add_sensor),
            self, bd=0, highlightthickness=0)

        # Default check settings
        self.direction_only.set(0)
        self.field_displayed.set(1)
        self.scale_displayed.set(0)
        self.grid_displayed.set(0)

        # Display system fields
        self.display_field(self.system)

        # Initial display of particles
        self.display_particles(self.system)

        # Selected particle
        self.selected_particle = None

        # Cursor modes
        self.click_mode = None
        self.length_mode_bool = False

        # Select length coords
        self.length_start = (0, 0)

        # Set widget bindings
        # Binded canvas mouse motion to information update
        self.canvas.bind("<Motion>", self.info_frame.update)
        # Binded particles to click and movement update
        self.particle_bind()
        # Unselect movement select particle
        self.canvas.bind("<ButtonRelease-1>", self.unselect_particle)
        # Binded canvas click to measuretape
        self.canvas.bind("<Button-1>", self.length_mode)

        # Pack widgets into window grid
        self.canvas.grid(row=0, column=0)
        self.info_frame.grid(row=0, column=1)

        # Update window
        self.update()

        # Run loop
        self.after(0, self.loop)

        # Run window mainloop
        self.mainloop()

    def length_mode(self, event):
        self.length_mode_bool = True
        self.length_start = (event.x, event.y)

    def add_sensor(self):
        s = models.Particle(300, 300, 0)
        self.system.add_particle(s)
        self.refresh_particles()
        self.click_mode = None

    def delete_mode(self):
        self.click_mode = "delete"

    def particle_bind(self):
        # Binded particles to click and movement update
        for particle in self.system.get_particles():
            self.canvas.tag_bind(particle.id, "<Button-1>", self.select_particle)

    def refresh_particles(self):
        self.canvas.delete("particle")
        self.display_particles(self.system)
        self.particle_bind()

    def add_pos_particle(self):
        p = models.Particle(300, 300, 1e-9)
        self.system.add_particle(p)
        self.refresh_particles()
        self.click_mode = None

    def add_neg_particle(self):
        p = models.Particle(300, 300, -1e-9)
        self.system.add_particle(p)
        self.refresh_particles()
        self.click_mode = None

    def select_particle(self, event):
        particle = self.canvas.find_withtag(CURRENT)[0]

        if self.click_mode is None:
            # Select particle that is clicked
            self.selected_particle = particle
        elif self.click_mode == "delete":
            self.system.remove_particle(particle)
            self.refresh_particles()
            self.click_mode = None

    def unselect_particle(self, event):
        # Unselect particle if is selected
        if self.selected_particle is not None:
            self.selected_particle = None

        self.length_mode_bool = False

        # Reset mode
        self.click_mode = None

    def loop(self):
        # Get mouse pos
        mousex = self.winfo_pointerx() - self.winfo_rootx() - self.particle_rad
        mousey = self.winfo_pointery() - self.winfo_rooty() - self.particle_rad

        # Move selected particle
        if self.selected_particle is not None:
            # Get selected particle coords
            selected_particle_coords = self.canvas.coords(self.selected_particle)

            # Get relative mouse position

            # Move particle to mouse
            self.canvas.move(self.selected_particle, mousex - selected_particle_coords[0], mousey - selected_particle_coords[1])

        # Update particle coords
        for particle in self.system.get_particles():
            particle.x = self.canvas.coords(particle.id)[0] + self.particle_rad
            particle.y = self.canvas.coords(particle.id)[1] + self.particle_rad

        # Update field
        self.canvas.delete("field")
        if self.field_displayed.get():
            self.display_field(self.system)

        # Display grid
        if self.grid_displayed.get():
            grid_sep = 25
            for column in range(self.config_width // grid_sep):
                self.canvas.create_line(column * grid_sep, 0, column * grid_sep, self.config_height, fill="#9e9e9e", tags="gridline")

            for row in range(self.config_height // grid_sep):
                self.canvas.create_line(0, row * grid_sep, self.config_width, row * grid_sep, fill="#9e9e9e", tags="gridline")
        else:
            self.canvas.delete("gridline")

        # Display sensor arrow
        self.canvas.delete("sensorline")
        for particle in self.system.get_particles():
            if particle.charge == 0:
                f = self.system.get_field(particle.x, particle.y)
                if f:
                    f[0] /= 1000
                    f[1] /= 1000
                    self.canvas.create_line(particle.x, particle.y, particle.x + f[0], particle.y + f[1], fill="#0f0", tags="sensorline")

        # Display length line
        self.canvas.delete("lengthline")
        if self.length_mode_bool and self.selected_particle is None:
            self.canvas.create_line(self.length_start[0], self.length_start[1], mousex, mousey, fill="#00d0ff", tags="lengthline")
            self.canvas.create_text((self.length_start[0] + mousex) / 2, (self.length_start[1] + mousey) / 2,
                text=f"{round(self.system.distance(self.length_start, (mousex, mousey)) / self.system.conversion, 3)} meters",
                fill="#00d0ff", tags="lengthline")

        # Raise particles
        self.canvas.tag_raise("particle")

        if self.scale_displayed.get():
            # Display scale
            self.canvas.create_rectangle(20, 20, 20 + self.system.conversion, 50, outline="green", fill="green", tags="scale")
            self.canvas.create_text((40 + self.system.conversion) / 2, 35, text="1 Meter", tags="scale")
        else:
            self.canvas.delete("scale")

        # Repeat loop
        self.after(10, self.loop)

    def display_field(self, system):
        # Display the system
        # Separation factor for field arrows
        arrow_sep = 50

        # Display field arrows
        for x in range(self.config_width // arrow_sep):
            for y in range(self.config_height // arrow_sep):
                # Get field vector at arrow position
                f = system.get_field(x * arrow_sep, y * arrow_sep)

                # Ignore arrow if position is at a particle
                if not f:
                    continue

                if self.direction_only.get():
                    # Disregard magnitude of arrows
                    f_dist_factor = system.distance((0, 0), f) / 30
                    f[0] /= f_dist_factor
                    f[1] /= f_dist_factor
                else:
                    # Resize arrows by a factor
                    resize_factor = 1000
                    f[0] /= resize_factor
                    f[1] /= resize_factor

                # Display arrow vector
                arrow = self.canvas.create_line(x * arrow_sep, y * arrow_sep,
                    x * arrow_sep + f[0], y * arrow_sep + f[1],
                    fill="white", arrow=LAST)
                self.canvas.addtag_withtag("field", arrow)

    def display_particles(self, system):
        # Display particles
        for particle in system.get_particles():
            # Indicate sign of charge with color
            if particle.charge < 0:
                color = "red"
            elif particle.charge > 0:
                color = "blue"
            else:
                color = "yellow"

            # Display particle
            p = particle.id = self.canvas.create_oval(particle.x - self.particle_rad, particle.y - self.particle_rad,
                particle.x + self.particle_rad, particle.y + self.particle_rad,
                outline=color, fill=color)
            self.canvas.addtag_withtag("particle", p)


# InfoFrame class
class InfoFrame(Frame):
    def __init__(self, field, intvars, cmds, *args, **kwargs):
        # Initialize the frame
        super().__init__(*args, **kwargs)

        # Instantiate StringVars
        self.x_label_var = StringVar()
        self.y_label_var = StringVar()
        self.field_label_var = StringVar()
        self.voltage_label_var = StringVar()

        # Instantiate labels
        # Pair textvariables to StringVars
        self.x_label = Label(self, textvariable=self.x_label_var, width=15)
        self.y_label = Label(self, textvariable=self.y_label_var, width=15)
        self.field_label = Label(self, textvariable=self.field_label_var, width=30)
        self.voltage_label = Label(self, textvariable=self.voltage_label_var, width=30)

        # Instantiate checks
        # Pair checks with intvars
        self.direction_check = Checkbutton(self, text="Direction Only", variable=intvars[0])
        self.field_check = Checkbutton(self, text="Display Field", variable=intvars[1])
        self.scale_check = Checkbutton(self, text="Display Scale", variable=intvars[2])
        self.grid_check = Checkbutton(self, text="Display Grid", variable=intvars[3])

        # Instantiate buttons
        # Pair event handlers with buttons
        self.create_pro = Button(self, text="Add - Charge", command=cmds[0])
        self.create_ele = Button(self, text="Add + Charge", command=cmds[1])
        self.delete_par = Button(self, text="Delete", command=cmds[2])
        self.create_sen = Button(self, text="Add Sensor", command=cmds[3])

        # Pack widgets into frame grid
        self.x_label.grid(row=0, column=0)
        self.y_label.grid(row=0, column=1)
        self.field_label.grid(row=1, column=0, columnspan=2)
        self.voltage_label.grid(row=2, column=0, columnspan=2)
        self.direction_check.grid(row=3, column=0, columnspan=2)
        self.field_check.grid(row=4, column=0, columnspan=2)
        self.scale_check.grid(row=5, column=0, columnspan=2)
        self.grid_check.grid(row=6, column=0, columnspan=2)
        self.create_pro.grid(row=7, column=0, columnspan=2)
        self.create_ele.grid(row=8, column=0, columnspan=2)
        self.delete_par.grid(row=9, column=0, columnspan=2)
        self.create_sen.grid(row=10, column=0, columnspan=2)

        # Instantiate field to read
        self.field = field

    def update(self, mov):
        # Update mouse information of frame
        self.x_label_var.set(f"X: {mov.x}")
        self.y_label_var.set(f"Y: {mov.y}")

        # Get field at mouse position
        f = self.field.get_field(mov.x, mov.y)

        # Return field if mouse not at particle position
        if f:
            f = self.field.distance((0, 0), f)
            f = round(f)
        else:
            f = "NaN"

        # Update field information at mouse
        self.field_label_var.set(f"Field: {f}")

        # Return voltage at mouse position
        v = self.field.get_voltage(mov.x, mov.y)
        v = round(v)

        # Update voltage information at mouse
        self.voltage_label_var.set(f"V: {v}")


# Main program
if __name__ == "__main__":
    # Run window
    Window()
