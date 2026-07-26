import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_toolkits.mplot3d import Axes3D

BG_COLOR = '#1a1a2e'
ENTRY_BG = '#2d2d44'
TEXT_COLOR = 'white'
ACCENT_COLOR = '#e94560'
PLANET_RADIUS_DEFAULT = 0.5      
ATMOSPHERE_RADIUS_MULT = 1.3     

#
def draw_sphere(ax, center, radius, color='royalblue', alpha=0.95, resolution=50):
    """Draw a solid planet."""
    u, v = np.mgrid[0:2*np.pi:resolution*1j, 0:np.pi:resolution*1j]
    x = center[0] + radius * np.cos(u) * np.sin(v)
    y = center[1] + radius * np.sin(u) * np.sin(v)
    z = center[2] + radius * np.cos(v)
    ax.plot_surface(x, y, z, color=color, alpha=alpha, linewidth=0, shade=True)

def draw_atmosphere(ax, center, radius, color='lightskyblue', alpha=0.15, resolution=30):
    """Draw a translucent atmosphere shell slightly larger than the planet."""
    u, v = np.mgrid[0:2*np.pi:resolution*1j, 0:np.pi:resolution*1j]
    r = radius * ATMOSPHERE_RADIUS_MULT
    x = center[0] + r * np.cos(u) * np.sin(v)
    y = center[1] + r * np.sin(u) * np.sin(v)
    z = center[2] + r * np.cos(v)
    ax.plot_surface(x, y, z, color=color, alpha=alpha, linewidth=0, shade=False)

def plot_orbit_3d(ax, a, e, inclination=0, omega=0, Omega=0, color='white', ls='-', lw=2, n_pts=300):
    t = np.linspace(0, 2*np.pi, n_pts)
    r = a * (1 - e**2) / (1 + e * np.cos(t))
    x_peri = r * np.cos(t)
    y_peri = r * np.sin(t)
    z_peri = np.zeros_like(x_peri)
    # 3-1-3 rotation
    x1 = x_peri * np.cos(omega) - y_peri * np.sin(omega)
    y1 = x_peri * np.sin(omega) + y_peri * np.cos(omega)
    z1 = z_peri
    x2 = x1
    y2 = y1 * np.cos(inclination) - z1 * np.sin(inclination)
    z2 = y1 * np.sin(inclination) + z1 * np.cos(inclination)
    x_f = x2 * np.cos(Omega) - y2 * np.sin(Omega)
    y_f = x2 * np.sin(Omega) + y2 * np.cos(Omega)
    z_f = z2
    ax.plot(x_f, y_f, z_f, color=color, linestyle=ls, linewidth=lw)

def plot_circle_3d(ax, radius, inclination=0, omega=0, Omega=0, color='white', ls='--', lw=1.5):
    plot_orbit_3d(ax, radius, 0, inclination, omega, Omega, color, ls, lw)


class ManeuverPlotter:
    @staticmethod
    def kepler_first_law(ax, a=3.0, e=0.6, **kwargs):
        ax.set_title("Kepler's First Law", color=TEXT_COLOR, fontsize=12)
        draw_atmosphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT)
        draw_sphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT, color='royalblue')
        plot_orbit_3d(ax, a, e, color='cyan', lw=2)
        ax.scatter([0],[0],[0], color='white', s=50)
        peri_x = a*(1-e)
        apo_x = -a*(1+e)
        ax.scatter([peri_x, apo_x], [0,0], [0,0], color='yellow', s=40)
        ax.text(peri_x, 0.4, 0, 'Peri', color='yellow', fontsize=8)
        ax.text(apo_x, 0.4, 0, 'Apo', color='yellow', fontsize=8)

    @staticmethod
    def raise_periapsis(ax, a0=2.0, e0=0.5, a_final=None, e_final=None, **kwargs):
        if a_final is None or e_final is None:
            peri_initial = a0*(1-e0)
            apo = -a0*(1+e0)
            peri_raised = peri_initial + 1.0
            a_final = (peri_raised + abs(apo))/2
            e_final = (abs(apo) - peri_raised) / (abs(apo) + peri_raised)
        ax.set_title("Raise Periapsis", color=TEXT_COLOR, fontsize=12)
        draw_atmosphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT)
        draw_sphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT, color='royalblue')
        plot_orbit_3d(ax, a0, e0, color='grey', ls='--', lw=1.5)
        plot_orbit_3d(ax, a_final, e_final, color='lime', lw=2)
        apo_x = -a0*(1+e0)
        ax.scatter([apo_x],[0],[0], color='red', s=60, marker='*')
        ax.quiver(apo_x, 0, 0, 0, 0.8, 0, color='red', arrow_length_ratio=0.2, linewidth=2)
        ax.text(apo_x, 0.8, 0, 'Burn\nprograde', color='red', fontsize=8)

    @staticmethod
    def lower_periapsis(ax, a0=2.5, e0=0.2, a_final=None, e_final=None, **kwargs):
        if a_final is None or e_final is None:
            peri_initial = a0*(1-e0)
            apo = -a0*(1+e0)
            peri_lowered = peri_initial - 1.0
            a_final = (peri_lowered + abs(apo))/2
            e_final = (abs(apo) - peri_lowered) / (abs(apo) + peri_lowered)
        ax.set_title("Lower Periapsis", color=TEXT_COLOR, fontsize=12)
        draw_atmosphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT)
        draw_sphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT, color='royalblue')
        plot_orbit_3d(ax, a0, e0, color='grey', ls='--', lw=1.5)
        plot_orbit_3d(ax, a_final, e_final, color='red', lw=2)
        apo_x = -a0*(1+e0)
        ax.scatter([apo_x],[0],[0], color='red', s=60, marker='*')
        ax.quiver(apo_x, 0, 0, 0, -0.8, 0, color='red', arrow_length_ratio=0.2, linewidth=2)
        ax.text(apo_x, -0.8, 0, 'Burn\nretrograde', color='red', fontsize=8)

    @staticmethod
    def raise_apoapsis(ax, a0=2.5, e0=0.2, a_final=None, e_final=None, **kwargs):
        if a_final is None or e_final is None:
            peri = a0*(1-e0)
            apo_initial = -a0*(1+e0)
            apo_raised = apo_initial - 2.0
            a_final = (peri + abs(apo_raised))/2
            e_final = (abs(apo_raised) - peri) / (abs(apo_raised) + peri)
        ax.set_title("Raise Apoapsis", color=TEXT_COLOR, fontsize=12)
        draw_atmosphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT)
        draw_sphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT, color='royalblue')
        plot_orbit_3d(ax, a0, e0, color='grey', ls='--', lw=1.5)
        plot_orbit_3d(ax, a_final, e_final, color='deepskyblue', lw=2)
        peri_x = a0*(1-e0)
        ax.scatter([peri_x],[0],[0], color='red', s=60, marker='*')
        ax.quiver(peri_x, 0, 0, 0, 0.8, 0, color='red', arrow_length_ratio=0.2)
        ax.text(peri_x, 0.8, 0, 'Burn\nprograde', color='red', fontsize=8)

    @staticmethod
    def lower_apoapsis(ax, a0=3.5, e0=0.4286, a_final=None, e_final=None, **kwargs):
        if a_final is None or e_final is None:
            peri = a0*(1-e0)
            apo_initial = -a0*(1+e0)
            apo_lowered = apo_initial + 2.0
            a_final = (peri + abs(apo_lowered))/2
            e_final = (abs(apo_lowered) - peri) / (abs(apo_lowered) + peri)
        ax.set_title("Lower Apoapsis", color=TEXT_COLOR, fontsize=12)
        draw_atmosphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT)
        draw_sphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT, color='royalblue')
        plot_orbit_3d(ax, a0, e0, color='grey', ls='--', lw=1.5)
        plot_orbit_3d(ax, a_final, e_final, color='orange', lw=2)
        peri_x = a0*(1-e0)
        ax.scatter([peri_x],[0],[0], color='red', s=60, marker='*')
        ax.quiver(peri_x, 0, 0, 0, -0.8, 0, color='red', arrow_length_ratio=0.2)
        ax.text(peri_x, -0.8, 0, 'Burn\nretrograde', color='red', fontsize=8)

    @staticmethod
    def plane_change(ax, r=3.0, delta_i=30, **kwargs):
        ax.set_title(f"Plane Change (Δi={delta_i}°)", color=TEXT_COLOR, fontsize=12)
        draw_atmosphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT)
        draw_sphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT, color='royalblue')
        plot_circle_3d(ax, r, color='grey', ls='--')
        plot_circle_3d(ax, r, inclination=np.deg2rad(delta_i), color='gold')
        ax.scatter([r],[0],[0], color='red', s=60, marker='*')
        ax.quiver(r, 0, 0, 0, 0, 0.8, color='red', arrow_length_ratio=0.2)
        ax.text(r, 0, 1.0, 'Burn normal', color='red', fontsize=8)

    @staticmethod
    def deorbit(ax, r_initial=1.5, planet_radius=0.5, **kwargs):
        ax.set_title("Deorbit", color=TEXT_COLOR, fontsize=12)
        draw_atmosphere(ax, (0,0,0), planet_radius)
        draw_sphere(ax, (0,0,0), planet_radius, color='chocolate', alpha=0.9)
        u = np.linspace(0, 2*np.pi, 100)
        ax.plot(np.cos(u), np.sin(u), 0, color='brown', ls='--')
        plot_circle_3d(ax, r_initial, color='white', ls='--')
        ax.scatter([-r_initial],[0],[0], color='red', s=60, marker='*')
        ax.quiver(-r_initial, 0, 0, 0, -1.2, 0, color='red', arrow_length_ratio=0.2)
        a_de = (planet_radius + r_initial)/2
        e_de = (r_initial - planet_radius) / (r_initial + planet_radius)
        plot_orbit_3d(ax, a_de, e_de, color='red', lw=2)

    @staticmethod
    def hohmann_transfer(ax, r1=1.0, r2=3.0, **kwargs):
        ax.set_title("Hohmann Transfer", color=TEXT_COLOR, fontsize=12)
        draw_atmosphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT)
        draw_sphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT, color='royalblue')
        plot_circle_3d(ax, r1, color='grey', ls='--')
        plot_circle_3d(ax, r2, color='lightgreen', ls='--')
        a_tr = (r1 + r2)/2
        e_tr = (r2 - r1)/(r2 + r1)
        plot_orbit_3d(ax, a_tr, e_tr, color='darkorange', lw=2)
        ax.scatter([r1, -r2],[0,0],[0,0], color='red', s=60, marker='*')
        ax.quiver(r1, 0, 0, 0, 0.8, 0, color='red', arrow_length_ratio=0.2)
        ax.quiver(-r2, 0, 0, 0, -0.8, 0, color='red', arrow_length_ratio=0.2)
        ax.text(r1, 0.7, 0, '1', color='red'); ax.text(-r2, -0.7, 0, '2', color='red')

    @staticmethod
    def bielliptic_transfer(ax, r1=1.0, r2=5.0, r_big=20.0, **kwargs):
        ax.set_title("Bi‑elliptic Transfer", color=TEXT_COLOR, fontsize=12)
        draw_atmosphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT)
        draw_sphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT, color='royalblue')
        plot_circle_3d(ax, r1, color='grey', ls='--')
        plot_circle_3d(ax, r2, color='lightgreen', ls='--')
        a1 = (r1 + r_big)/2; e1 = (r_big - r1)/(r_big + r1)
        a2 = (r2 + r_big)/2; e2 = (r_big - r2)/(r_big + r2)
        plot_orbit_3d(ax, a1, e1, color='blue', ls=':', lw=1.5)
        plot_orbit_3d(ax, a2, e2, color='magenta', ls='-.', lw=1.5)
        ax.scatter([r1, -r_big, r2],[0,0,0],[0,0,0], color='red', s=60, marker='*')
        ax.quiver(r1,0,0, 0,0.8,0, color='red', arrow_length_ratio=0.2)
        ax.quiver(-r_big,0,0, 0,0.8,0, color='red', arrow_length_ratio=0.2)
        ax.quiver(r2,0,0, 0,-0.8,0, color='red', arrow_length_ratio=0.2)
        ax.text(r1,0.7,0, '1', color='red'); ax.text(-r_big,0.7,0, '2', color='red'); ax.text(r2,-0.7,0, '3', color='red')

    @staticmethod
    def plane_change_dv_triangle(ax, v=1.5, delta_i=40, **kwargs):
        ax.set_title("Plane Change Δv Triangle", color=TEXT_COLOR, fontsize=12)
        delta_i_rad = np.deg2rad(delta_i)
        v1 = np.array([v, 0, 0])
        v2 = np.array([v*np.cos(delta_i_rad), v*np.sin(delta_i_rad), 0])
        dv = v2 - v1
        ax.quiver(0,0,0, *v1, color='cyan', arrow_length_ratio=0.1, linewidth=2)
        ax.quiver(0,0,0, *v2, color='lime', arrow_length_ratio=0.1, linewidth=2)
        ax.quiver(*v1, *dv, color='red', arrow_length_ratio=0.1, linewidth=2)
        ax.text(v/2, -0.2, 0, r'$\vec{v}_1$', color='cyan'); ax.text(v*np.cos(delta_i_rad)/2, v*np.sin(delta_i_rad)/2, 0, r'$\vec{v}_2$', color='lime')
        ax.set_xlim(-0.5,2.5); ax.set_ylim(-0.5,2); ax.set_zlim(-0.5,0.5)

    @staticmethod
    def eccentricity_vector(ax, a=2.5, e=0.6, **kwargs):
        ax.set_title("Eccentricity Vector", color=TEXT_COLOR, fontsize=12)
        draw_atmosphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT)
        draw_sphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT, color='royalblue')
        plot_orbit_3d(ax, a, e, color='white', lw=2)
        peri_x = a*(1-e)
        ax.quiver(0,0,0, peri_x, 0, 0, color='red', arrow_length_ratio=0.1, linewidth=2)
        ax.text(peri_x/2, 0.3, 0, r'$\vec{e}$', color='red', fontsize=12)
        apo_x = -a*(1+e)
        ax.quiver(apo_x, 0, 0, 0, 0.5, 0, color='green', arrow_length_ratio=0.2)
        ax.text(apo_x, 0.5, 0, 'Prograde\nat apo', color='green', fontsize=8)
        ax.quiver(peri_x, 0, 0, 0, 0, 0.5, color='yellow', arrow_length_ratio=0.2)
        ax.text(peri_x, 0, 0.7, 'Radial\nat peri', color='yellow', fontsize=8)

    @staticmethod
    def phasing(ax, r_target=3.0, r_phase=2.0, **kwargs):
        ax.set_title("Phasing Maneuver", color=TEXT_COLOR, fontsize=12)
        draw_atmosphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT)
        draw_sphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT, color='royalblue')
        plot_circle_3d(ax, r_target, color='grey', ls='--')
        plot_circle_3d(ax, r_phase, color='darkorange', lw=2)
        ax.scatter([r_target*np.cos(np.deg2rad(90))], [r_target*np.sin(np.deg2rad(90))], [0], color='white', s=50)
        ax.scatter([r_phase*np.cos(np.deg2rad(150))], [r_phase*np.sin(np.deg2rad(150))], [0], color='red', s=50)
        ax.text(r_target*np.cos(np.deg2rad(90)), r_target*np.sin(np.deg2rad(90))+0.5, 0, 'Target', color='white', fontsize=8)
        ax.text(r_phase*np.cos(np.deg2rad(150)), r_phase*np.sin(np.deg2rad(150))+0.5, 0, 'Chaser', color='red', fontsize=8)
        ax.quiver(2.5,0,0, 0,2.5,0, color='cyan', arrow_length_ratio=0.1)
        ax.text(2.8,1.4,0, r'$\Delta\theta$', color='cyan', fontsize=10)

    @staticmethod
    def collision_avoidance(ax, **kwargs):
        ax.set_title("Collision Avoidance", color=TEXT_COLOR, fontsize=12)
        draw_atmosphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT)
        draw_sphere(ax, (0,0,0), PLANET_RADIUS_DEFAULT, color='royalblue')
        plot_circle_3d(ax, 4.0, color='blue', ls='--')
        plot_orbit_3d(ax, 4.0, 0.2, inclination=np.deg2rad(10), color='red')
        ax.scatter([3.6, 3.6], [1.3, -1.3], [0,0], color='yellow', s=40)
        plot_orbit_3d(ax, 4.0, 0.3, inclination=np.deg2rad(5), color='lime', lw=2)
        ax.text(3.8, 1.8, 0, 'Collision\npoints', color='yellow', fontsize=8)

# ----------------------------------------------------------------------
# Parameter definitions
# ----------------------------------------------------------------------
MANEUVER_PARAMS = {
    "Kepler's First Law": [
        ('a (semi-major axis)', '3.0'),
        ('e (eccentricity)', '0.6')
    ],
    "Raise Periapsis": [
        ('initial a', '2.0'),
        ('initial e', '0.5'),
        ('final a (optional)', ''),
        ('final e (optional)', '')
    ],
    "Lower Periapsis": [
        ('initial a', '2.5'),
        ('initial e', '0.2'),
        ('final a (optional)', ''),
        ('final e (optional)', '')
    ],
    "Raise Apoapsis": [
        ('initial a', '2.5'),
        ('initial e', '0.2'),
        ('final a (optional)', ''),
        ('final e (optional)', '')
    ],
    "Lower Apoapsis": [
        ('initial a', '3.5'),
        ('initial e', '0.4286'),
        ('final a (optional)', ''),
        ('final e (optional)', '')
    ],
    "Plane Change": [
        ('Orbit radius r', '3.0'),
        ('Inclination change (deg)', '30')
    ],
    "Deorbit": [
        ('Initial orbit radius', '1.5'),
        ('Planet radius', '0.5')
    ],
    "Hohmann Transfer": [
        ('Initial orbit radius r1', '1.5'),
        ('Target orbit radius r2', '3.5')
    ],
    "Bi-elliptic Transfer": [
        ('Initial radius r1', '1.5'),
        ('Target radius r2', '5.0'),
        ('Intermediate apoapsis r_big', '20.0')
    ],
    "Plane Change Δv Triangle": [
        ('Speed v', '1.5'),
        ('Angle Δi (deg)', '40')
    ],
    "Eccentricity Vector": [
        ('Semi-major axis a', '2.5'),
        ('Eccentricity e', '0.6')
    ],
    "Phasing Maneuver": [
        ('Target orbit radius', '3.5'),
        ('Phasing orbit radius', '2.5')
    ],
    "Collision Avoidance": []
}


class OrbitalVisualizer3D:
    def __init__(self, root):
        self.root = root
        self.root.title("Orbital Maneuver 3D Visualizer")
        self.root.configure(bg=BG_COLOR)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR, font=('Arial', 10))
        style.configure('TButton', background=ENTRY_BG, foreground='black', font=('Arial', 10))
        style.configure('TEntry', fieldbackground=ENTRY_BG, foreground='white')

        self.left_frame = tk.Frame(root, bg=BG_COLOR, width=280)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.right_frame = tk.Frame(root, bg=BG_COLOR)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(self.left_frame, text="Select Maneuver:").pack(pady=5)
        self.maneuver_var = tk.StringVar(value=list(MANEUVER_PARAMS.keys())[0])
        self.combo = ttk.Combobox(self.left_frame, textvariable=self.maneuver_var,
                                  values=list(MANEUVER_PARAMS.keys()), width=28)
        self.combo.pack(pady=5)
        self.combo.bind('<<ComboboxSelected>>', self.update_param_fields)

        self.param_canvas = tk.Frame(self.left_frame, bg=BG_COLOR)
        self.param_canvas.pack(fill=tk.BOTH, expand=True, pady=10)
        self.param_entries = {}

        self.plot_btn = ttk.Button(self.left_frame, text="Plot", command=self.plot)
        self.plot_btn.pack(pady=5)

        self.rot_btn = ttk.Button(self.left_frame, text="Start Rotation", command=self.toggle_rotation)
        self.rot_btn.pack(pady=5)

        self.fullscreen_btn = ttk.Button(self.left_frame, text="Fullscreen View", command=self.open_fullscreen)
        self.fullscreen_btn.pack(pady=5)

        self.fig = plt.figure(figsize=(7,6), facecolor='black')
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor('black')
        self.ax.grid(False)
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        self.ax.set_xticks([]); self.ax.set_yticks([]); self.ax.set_zticks([])
        self.add_stars()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.right_frame)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.rotating = False
        self.update_param_fields()

    def add_stars(self, n=200, radius=25):
        phi = np.random.uniform(0, 2*np.pi, n)
        theta = np.random.uniform(-np.pi/2, np.pi/2, n)
        x = radius * np.cos(theta) * np.cos(phi)
        y = radius * np.cos(theta) * np.sin(phi)
        z = radius * np.sin(theta)
        self.ax.scatter(x, y, z, c='white', s=4, alpha=0.7, linewidths=0)

    def update_param_fields(self, event=None):
        for widget in self.param_canvas.winfo_children():
            widget.destroy()
        self.param_entries.clear()
        maneuver = self.maneuver_var.get()
        if maneuver not in MANEUVER_PARAMS:
            return
        for idx, (name, default) in enumerate(MANEUVER_PARAMS[maneuver]):
            ttk.Label(self.param_canvas, text=name).grid(row=idx, column=0, sticky='w', padx=5, pady=2)
            entry = ttk.Entry(self.param_canvas, width=10)
            entry.insert(0, default)
            entry.grid(row=idx, column=1, padx=5, pady=2)
            self.param_entries[name] = entry

    def read_params(self):
        params = {}
        for name, entry in self.param_entries.items():
            val = entry.get().strip()
            if val:
                try:
                    params[name] = float(val)
                except ValueError:
                    pass
        return params

    def plot(self, fig_ax_tuple=None):
        if fig_ax_tuple:
            fig, ax = fig_ax_tuple
        else:
            ax = self.ax
            fig = self.fig
        ax.clear()
        ax.set_facecolor('black')
        ax.grid(False)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
        # Re-add stars
        phi = np.random.uniform(0, 2*np.pi, 200)
        theta = np.random.uniform(-np.pi/2, np.pi/2, 200)
        x = 25 * np.cos(theta) * np.cos(phi)
        y = 25 * np.cos(theta) * np.sin(phi)
        z = 25 * np.sin(theta)
        ax.scatter(x, y, z, c='white', s=4, alpha=0.7, linewidths=0)

        maneuver = self.maneuver_var.get()
        params = self.read_params()
        plot_func = getattr(ManeuverPlotter, self.snake_case(maneuver), None)
        if plot_func is None:
            ax.text(0,0,0,"Not implemented", color='white')
        else:
            kwargs = self.build_kwargs(maneuver, params)
            plot_func(ax, **kwargs)

        if not fig_ax_tuple:
            self.canvas.draw()

    def build_kwargs(self, maneuver, params):
        if maneuver == "Kepler's First Law":
            return {'a': params.get('a (semi-major axis)', 3.0),
                    'e': params.get('e (eccentricity)', 0.6)}
        elif maneuver == "Raise Periapsis":
            d = {'a0': params.get('initial a', 2.0), 'e0': params.get('initial e', 0.5)}
            if 'final a (optional)' in params: d['a_final'] = params['final a (optional)']
            if 'final e (optional)' in params: d['e_final'] = params['final e (optional)']
            return d
        elif maneuver == "Lower Periapsis":
            d = {'a0': params.get('initial a', 2.5), 'e0': params.get('initial e', 0.2)}
            if 'final a (optional)' in params: d['a_final'] = params['final a (optional)']
            if 'final e (optional)' in params: d['e_final'] = params['final e (optional)']
            return d
        elif maneuver == "Raise Apoapsis":
            d = {'a0': params.get('initial a', 2.5), 'e0': params.get('initial e', 0.2)}
            if 'final a (optional)' in params: d['a_final'] = params['final a (optional)']
            if 'final e (optional)' in params: d['e_final'] = params['final e (optional)']
            return d
        elif maneuver == "Lower Apoapsis":
            d = {'a0': params.get('initial a', 3.5), 'e0': params.get('initial e', 0.4286)}
            if 'final a (optional)' in params: d['a_final'] = params['final a (optional)']
            if 'final e (optional)' in params: d['e_final'] = params['final e (optional)']
            return d
        elif maneuver == "Plane Change":
            return {'r': params.get('Orbit radius r', 3.0),
                    'delta_i': params.get('Inclination change (deg)', 30)}
        elif maneuver == "Deorbit":
            return {'r_initial': params.get('Initial orbit radius', 1.5),
                    'planet_radius': params.get('Planet radius', 0.5)}
        elif maneuver == "Hohmann Transfer":
            return {'r1': params.get('Initial orbit radius r1', 1.5),
                    'r2': params.get('Target orbit radius r2', 3.5)}
        elif maneuver == "Bi-elliptic Transfer":
            return {'r1': params.get('Initial radius r1', 1.5),
                    'r2': params.get('Target radius r2', 5.0),
                    'r_big': params.get('Intermediate apoapsis r_big', 20.0)}
        elif maneuver == "Plane Change Δv Triangle":
            return {'v': params.get('Speed v', 1.5),
                    'delta_i': params.get('Angle Δi (deg)', 40)}
        elif maneuver == "Eccentricity Vector":
            return {'a': params.get('Semi-major axis a', 2.5),
                    'e': params.get('Eccentricity e', 0.6)}
        elif maneuver == "Phasing Maneuver":
            return {'r_target': params.get('Target orbit radius', 3.5),
                    'r_phase': params.get('Phasing orbit radius', 2.5)}
        elif maneuver == "Collision Avoidance":
            return {}
        return {}

    def snake_case(self, name):
        mapping = {
            "Kepler's First Law": "kepler_first_law",
            "Raise Periapsis": "raise_periapsis",
            "Lower Periapsis": "lower_periapsis",
            "Raise Apoapsis": "raise_apoapsis",
            "Lower Apoapsis": "lower_apoapsis",
            "Plane Change": "plane_change",
            "Deorbit": "deorbit",
            "Hohmann Transfer": "hohmann_transfer",
            "Bi-elliptic Transfer": "bielliptic_transfer",
            "Plane Change Δv Triangle": "plane_change_dv_triangle",
            "Eccentricity Vector": "eccentricity_vector",
            "Phasing Maneuver": "phasing",
            "Collision Avoidance": "collision_avoidance"
        }
        return mapping[name]

    def toggle_rotation(self):
        if self.rotating:
            self.rotating = False
            self.rot_btn.config(text="Start Rotation")
        else:
            self.rotating = True
            self.rot_btn.config(text="Stop Rotation")
            self.rotate_view()

    def rotate_view(self):
        if not self.rotating:
            return
        self.ax.view_init(elev=20, azim=self.ax.azim + 0.8)
        self.canvas.draw()
        self.root.after(50, self.rotate_view)

    def open_fullscreen(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Fullscreen Orbital View")
        new_window.configure(bg='black')
        new_window.attributes('-fullscreen', True)

        fig = plt.figure(figsize=(16,9), facecolor='black')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('black')
        ax.grid(False)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])

        self.plot(fig_ax_tuple=(fig, ax))

        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        close_btn = tk.Button(new_window, text="Close (Esc)", command=new_window.destroy,
                              bg='black', fg='white', font=('Arial', 14))
        close_btn.pack(pady=10)
        new_window.bind("<Escape>", lambda e: new_window.destroy())

if __name__ == "__main__":
    root = tk.Tk()
    app = OrbitalVisualizer3D(root)
    root.mainloop()
