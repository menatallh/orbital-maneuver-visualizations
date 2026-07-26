
# 🚀 Orbital Maneuver 3D Visualizer

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.5%2B-orange)](https://matplotlib.org/)

An interactive 3D visualization tool for classical and advanced orbital maneuvers.  
Built with `tkinter` and `matplotlib`, it features a **dark space theme**, **rotatable starfield**, and **customizable orbit parameters**.  

Perfect for students, educators, and spaceflight enthusiasts who want to explore astrodynamics intuitively.

---

## ✨ Features

- **13 maneuver types** – from Kepler’s laws to bi‑elliptic transfers, plane changes, phasing, and collision avoidance.
- **True 3D rendering** – elliptical orbits drawn with correct Keplerian elements (inclination, argument of periapsis, etc.).
- **Live parameter editing** – adjust semi‑major axis, eccentricity, orbit radii, inclination changes on the fly.
- **Dynamic rotation** – the camera can orbit the central body automatically for a cinematic view.
- **Star background** – hundreds of randomly placed stars on a black canvas.
- **Color‑coded orbits and burns** – clear visual distinction between initial, transfer, and final trajectories.

---

## 🖥️ Screenshots

*(Replace these with actual screenshots after running the app.)*

![Hohmann transfer](images/hohmann_screenshot.png)  
![Plane change](images/plane_change_screenshot.png)  
![Bi-elliptic transfer](images/bielliptic_screenshot.png)

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/orbital-maneuver-3d-visualizer.git
   cd orbital-maneuver-3d-visualizer
   ```

2. **Install dependencies** (Python 3.8+ recommended)
   ```bash
   pip install -r requirements.txt
   ```
   `requirements.txt` only contains:
   ```
   numpy>=1.20
   matplotlib>=3.5
   ```

3. **Run the application**
   ```bash
   python orbital_visualizer_gui.py
   ```

---

## 🎮 How to Use

1. Select a maneuver from the dropdown list (e.g., *Hohmann Transfer*).
2. Optional: modify the parameters in the input fields.
3. Click **Plot** to see the maneuver in the 3D window.
4. Use your mouse to zoom, pan, and rotate the view.
5. Press **Start Rotation** to let the camera automatically orbit the scene.

---

## 🧩 Included Maneuvers

| Category | Maneuver |
|----------|----------|
| Kepler’s laws | Kepler’s First Law |
| Apsidal burns | Raise / Lower Periapsis, Raise / Lower Apoapsis |
| Plane changes | Plane Change, Plane Change Δv Triangle |
| Entry / descent | Deorbit |
| Transfers | Hohmann Transfer, Bi‑elliptic Transfer |
| Advanced | Eccentricity Vector, Phasing Maneuver, Collision Avoidance |

---

## ⚙️ Code Structure

- `orbital_visualizer_gui.py` – main application: GUI, 3D drawing, and all maneuver logic.
- `ManeuverPlotter` class – static methods for each maneuver.
- `OrbitalVisualizer3D` class – Tkinter window management, rotation, and parameter handling.

The code is self‑contained and heavily commented. Adding a new maneuver is as simple as:
- Adding a new method to `ManeuverPlotter`.
- Listing it in `MANEUVER_PARAMS` with the required parameter fields.
- Adding a mapping in `snake_case()`.

---

## 🛠️ Customization

All orbit parameters are exposed through the GUI, but you can also tweak:
- **Planet size and color** inside `draw_sphere()` calls.
- **Star density / radius** in `add_stars()`.
- **Rotation speed** in the `rotate_view()` method.

---

## 📚 Educational Value

This tool supports:
- University courses on orbital mechanics / spacecraft dynamics.
- Self‑study with classic textbooks (Bate, Mueller & White; Vallado).
- KSP / Orbiter mission planning – understanding the geometry behind in‑game maneuvers.

---

## 🤝 Contributing

Pull requests are welcome! If you’d like to add a new maneuver (e.g., gravity assist, low‑thrust spiral, Lambert solver), please:

1. Fork the repo  
2. Create a feature branch  
3. Submit a PR with a clear description  

Make sure your code includes the necessary parameter fields and maintains the dark theme.

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## ⭐ Acknowledgements

Inspired by the beauty of orbital mechanics and the open‑source tools NumPy & Matplotlib.

---

*If you find this useful, a star ⭐ is always appreciated!*


https://github.com/user-attachments/assets/4a630264-b3d7-45be-b30b-90b0bd6e0a8f


