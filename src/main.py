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

        # Load default particles
        p1 = models.Particle(100, 300)
        p2 = models.Particle(700, 300, -1)
        system = models.System([p1, p2])

        # Instantiate widgets
        self.canvas = Canvas(self, width=800, height=600, bg="black", bd=0, highlightthickness=0)
        self.info_frame = InfoFrame(system, self, bd=0, highlightthickness=0)

        # Set widget bindings
        # Binded canvas mouse motion to information update
        self.canvas.bind("<Motion>", self.info_frame.update)

        # Pack widgets into window grid
        self.canvas.grid(row=0, column=0)
        self.info_frame.grid(row=0, column=1)

        # Update window
        self.update()

        # Display system
        self.display(system)

        # Run window mainloop
        self.mainloop()

    def display(self, system):
        # Display the system
        # Separation factor for field arrows
        arrow_sep = 50
        # Radius of particle
        particle_rad = 10

        # Display field arrows
        for x in range(self.canvas.winfo_width() // arrow_sep):
            for y in range(self.canvas.winfo_height() // arrow_sep):
                # Get field vector at arrow position
                f = system.get_field(x * arrow_sep, y * arrow_sep)

                # Ignore arrow if position is at a particle
                if not f:
                    continue

                # Resize arrows by a factor
                resize_factor = 10000
                f[0] /= resize_factor
                f[1] /= resize_factor

                # Display arrow position
                self.canvas.create_oval(x * arrow_sep - 2, y * arrow_sep - 2,
                    x * arrow_sep + 2, y * arrow_sep + 2,
                    outline="white", fill="white")

                # Display arrow vector
                self.canvas.create_line(x * arrow_sep, y * arrow_sep,
                    x * arrow_sep + f[0], y * arrow_sep + f[1],
                    fill="white")

        # Display particles
        for particle in system.get_particles():
            # Indicate sign of charge with color
            if particle.charge > 0:
                color = "red"
            else:
                color = "blue"

            # Display particle
            self.canvas.create_oval(particle.x - particle_rad, particle.y - particle_rad,
                particle.x + particle_rad, particle.y + particle_rad,
                outline=color, fill=color)


# InfoFrame class
class InfoFrame(Frame):
    def __init__(self, field, *args, **kwargs):
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

        # Pack widgets into frame grid
        self.x_label.grid(row=0, column=0)
        self.y_label.grid(row=0, column=1)
        self.field_label.grid(row=1, column=0, columnspan=2)

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
