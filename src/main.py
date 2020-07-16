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

        # Load default particles
        p1 = models.Particle(100, 300, 1e-9)
        p2 = models.Particle(700, 300, -1e-9)
        self.system = models.System([p1, p2], 200)

        # Instantiate widgets
        self.canvas = Canvas(self, width=self.config_width, height=self.config_height, bg="black", bd=0, highlightthickness=0)
        self.info_frame = InfoFrame(self.system,
            (self.direction_only, self.field_displayed, self.scale_displayed),
            self, bd=0, highlightthickness=0)

        # Default check settings
        self.direction_only.set(0)
        self.field_displayed.set(1)
        self.scale_displayed.set(0)

        # Display system fields
        self.display_field(self.system)

        # Initial display of particles
        self.display_particles(self.system)

        # Selected particle
        self.selected_particle = None

        # Set widget bindings
        # Binded canvas mouse motion to information update
        self.canvas.bind("<Motion>", self.info_frame.update)
        # Binded particles to click and movement update
        for particle in self.system.get_particles():
            self.canvas.tag_bind(particle.id, "<Button-1>", self.select_particle)
        # Unselect movement select particle
        self.canvas.bind("<ButtonRelease-1>", self.unselect_particle)

        # Pack widgets into window grid
        self.canvas.grid(row=0, column=0)
        self.info_frame.grid(row=0, column=1)

        # Update window
        self.update()

        # Run loop
        self.after(0, self.loop)

        # Run window mainloop
        self.mainloop()

    def select_particle(self, event):
        # Select particle that is clicked
        particle = self.canvas.find_withtag(CURRENT)[0]
        self.selected_particle = particle

    def unselect_particle(self, event):
        # Unselect particle if is selected
        if self.selected_particle is not None:
            self.selected_particle = None

    def loop(self):
        # Move selected particle
        if self.selected_particle is not None:
            # Get selected particle coords
            selected_particle_coords = self.canvas.coords(self.selected_particle)

            # Get relative mouse position
            mousex = self.winfo_pointerx() - self.winfo_rootx() - self.particle_rad
            mousey = self.winfo_pointery() - self.winfo_rooty() - self.particle_rad

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
            if particle.charge > 0:
                color = "red"
            else:
                color = "blue"

            # Display particle
            p = particle.id = self.canvas.create_oval(particle.x - self.particle_rad, particle.y - self.particle_rad,
                particle.x + self.particle_rad, particle.y + self.particle_rad,
                outline=color, fill=color)
            self.canvas.addtag_withtag("particle", p)


# InfoFrame class
class InfoFrame(Frame):
    def __init__(self, field, intvars, *args, **kwargs):
        # Initialize the frame
        super().__init__(*args, **kwargs)

        # Instantiate StringVars
        self.x_label_var = StringVar()
        self.y_label_var = StringVar()
        self.field_label_var = StringVar()

        # Instantiate labels
        # Pair textvariables to StringVars
        self.x_label = Label(self, textvariable=self.x_label_var, width=15)
        self.y_label = Label(self, textvariable=self.y_label_var, width=15)
        self.field_label = Label(self, textvariable=self.field_label_var, width=30)

        # Instantiate checks
        # Pair checks with intvars
        self.direction_check = Checkbutton(self, text="Direction Only", variable=intvars[0])
        self.field_check = Checkbutton(self, text="Display Field", variable=intvars[1])
        self.scale_check = Checkbutton(self, text="Display Scale", variable=intvars[2])

        # Pack widgets into frame grid
        self.x_label.grid(row=0, column=0)
        self.y_label.grid(row=0, column=1)
        self.field_label.grid(row=1, column=0, columnspan=2)
        self.direction_check.grid(row=2, column=0, columnspan=2)
        self.field_check.grid(row=3, column=0, columnspan=2)
        self.scale_check.grid(row=4, column=0, columnspan=2)

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


# Main program
if __name__ == "__main__":
    # Run window
    Window()
