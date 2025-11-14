# Space Shooter Game

Space Shooter is a 2D arcade game where players control a spaceship and battle through 5 challenging levels with unique enemy attack patterns.

## Game Features

- **5 Challenging Levels**: Each with unique enemy attack patterns
  - Level 1: 8-directional shooting
  - Level 2: Faster 12-directional shots
  - Level 3: Spiral firing pattern
  - Level 4: Aimed shots with spread
  - Level 5: Combination of circular and targeted fire
- **Upgrade System**: Earn points to enhance damage, health, speed, armor, and attack speed
- **Single Player Mode**: Play alone against waves of enemies
- **Animated Parallax Background**
- **Explosion Effects**: Using `boom.png` and `boom2.png`
- **Sound Effects**: For shooting, explosions, and menu navigation

## Files

- `space_shooter_russian.py`: Main game logic (offline version)
- `space_shooter_offline.py`: Simplified standalone version
- Various `.png` and `.wav` assets for visuals and audio

## How to Play

- **Controls**: Arrow keys to move, SPACE to shoot, B for shop, ESC for menu
- **Objective**: Destroy enemy ships and survive as long as possible
- **Scoring**: Earn points for each enemy destroyed
- **Leveling**: Gain XP by destroying enemies and level up for bonuses

## System Requirements

- Python 3.7+
- Pygame library

## Installing Dependencies

The game requires a specific Python interpreter located at `D:\Panda3D-1.10.15-x64\python\python.exe`. To install Pygame:

```bash
D:\Panda3D-1.10.15-x64\python\python.exe -m pip install pygame
```

Alternatively, you can run the provided `install_dependencies.bat` script which will automatically use the correct Python interpreter.

## Running the Game

### Main Version (Offline)
Double-click `run_all.bat` or run from command line:
```bash
run_all.bat
```

### Standalone Version
Double-click `run_standalone.bat` or run from command line:
```bash
run_standalone.bat
```

### Web Deployment
Double-click `run_web_standalone.bat` or run from command line:
```bash
run_web_standalone.bat
```

## Web Deployment

For web deployment instructions, see `README_WEB_DEPLOY.md`

## Support

For issues or questions, please contact the developer.