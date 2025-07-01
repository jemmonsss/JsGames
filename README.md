# 🎮 JsGames

**JsGames** is a modular collection of classic arcade-style games made with **Python** and **Pygame**. It includes a built-in launcher (`menu.py`) and supports running each game standalone or from your own custom menu system.

You can also download the **pre-installed executable** for Windows from the latest release here:  
👉 [Download EXE Release](https://github.com/jemmonsss/JsGames/releases/tag/exe)

---

## 📦 Included Games

### 🧱 Breakout
Break bricks using a paddle and ball. Collect powerups like:
- Extra life
- Sticky paddle
- Bigger paddle
- Slow motion

**Controls**:
- `←` / `→` — Move  
- `SPACE` — Launch ball  
- `P` — Pause  
- `ESC` — Return to menu  

📁 Sounds: place `.wav` files in `./breakout/`

---

### 🏓 Pong
Play against AI or a friend. Includes difficulty selection and win condition.

**Controls**:
- Player 1: `W/S`  
- Player 2: `↑/↓`  
- `P` — Pause  
- `ESC` — Return to menu  

📁 Sounds: place `.wav` files in `./pong/`

---

### 🐍 Snake
Modern Snake with two modes: **Classic** (walls = death) and **No Walls** (wrap around).

**Controls**:
- `Arrow Keys` — Move  
- `P` — Pause  
- `ESC` — Return to menu  

📁 Sounds: place `.wav` files in `./snake/`

---

### 🔢 2048 (Tile Fusion Edition)
Slide tiles to combine numbers and reach 2048. Clean visuals and scoring included.

**Controls**:
- `Arrow Keys` — Move tiles  
- `ESC` — Quit  

---

## 📂 Modular Menu Support

The games are fully modular and can be imported into **any menu system** using their `launch()` function:

```python
import snake
import pong
import tfe
import breakout

snake.launch()     # Start Snake
pong.launch()      # Start Pong
tfe.launch()       # Start 2048
breakout.launch()  # Start Breakout
```
### Option 2: Run with Python

Make sure Python and Pygame are installed:

```bash
pip install pygame


python menu.py        # Game launcher
python breakout.py    # Play Breakout
python pong.py        # Play Pong
python snake.py       # Play Snake
python tfe.py         # Play 2048
