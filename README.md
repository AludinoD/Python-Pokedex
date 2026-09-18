# Python-Pokedex
A Pokedex themed Application with PokeAPI made in Python and Tkinter for GUI.
---
Inspired by the Kanto Region Pokedex from Pokémon: Indigo League, I decided to recreate it using Figma as a design for the Application. I also used PokeAPI  to display necessary information about the Pokémon. 
## Features 
This app includes multiple features that mimic how a Pokédex works in the show:
* **Browse and Search:** Look up Pokémon easily by either their **index number** or their **name**.
* **Navigation:** Cycle seamlessly between the **next and previous** Pokémon.
* **Detailed Stats:** View comprehensive **Pokémon stats**, **nature type**, and **evolution lines**.
* **Variant Toggling:** Instantly switch between the **normal** and **shiny** variants of each Pokémon.
* **Favorites System:** Add Pokémon to your **favorites** list and remove them whenever you like.
* **Comparison Tool:** Compare **two Pokémon side by side** to analyze their traits.

---

## Project Structure
```text
├── Pokedex.py             # Main application source script
├── BgMusic.mp3            # Background audio track
├── Compare.png            # Background asset for comparing Pokémon stats/features
├── Pokeball.ico           # Application window icon
└── PokeDex.png            # Main background asset
```

## How To Run?

### Prerequisites

Make sure you have **Python 3.x** installed on your system.

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Set up a virtual environment (Recommended):**
   ```bash
   python -m venv .venv
   
   # On Windows:
   .venv\Scripts\activate
   
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Run the application:**
   ```bash
   python Pokedex.py
   ```

---

## Assets Note
All media files (`BgMusic.mp3`, `.png` assets, and `.ico` files) are placed in the root directory so the main script can load them dynamically during runtime.

---
