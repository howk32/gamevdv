# Space Shooter - Web Deployment

This is a standalone version of the Space Shooter game that can be deployed to the web without any online multiplayer functionality.

## Files Included

- `space_shooter_offline.py` - Standalone Python version of the game (no online required)
- `index.html` - Main web page for the game
- `run_standalone.bat` - Batch file to run the standalone Python version
- `run_web_standalone.bat` - Batch file to run a simple web server
- `web_server_standalone.py` - Simple web server for hosting the game

## How to Deploy to the Web

### Option 1: GitHub Pages
1. Create a GitHub repository
2. Upload all files to the repository
3. Enable GitHub Pages in the repository settings
4. Your game will be available at `https://username.github.io/repository-name/`

### Option 2: Any Static Web Hosting
1. Upload all files to your web hosting service
2. Make sure `index.html` is served as the main page
3. The game will be accessible through your domain

### Option 3: Local Testing
1. Run `run_web_standalone.bat`
2. Open your browser and go to `http://localhost:8000`

## How to Play

- **Controls**: Arrow keys to move, SPACE to shoot, ESC for menu
- **Objective**: Destroy enemy ships and survive as long as possible
- **Scoring**: Earn points for each enemy destroyed

## System Requirements

- Python 3.7+ (for running the standalone version)
- Web browser (for playing in the browser)

## Installing Dependencies

For the standalone Python version:
```bash
pip install pygame
```

## Running the Standalone Version

Double-click `run_standalone.bat` or run from command line:
```bash
python space_shooter_offline.py
```

## Running the Web Server (for local testing)

Double-click `run_web_standalone.bat` or run from command line:
```bash
python web_server_standalone.py
```

Then open your browser and go to `http://localhost:8000`

## Features

- Classic space shooter gameplay
- 5 challenging levels
- Simple upgrade system
- Animated backgrounds
- Sound effects
- No online requirements
- Easy deployment to any web hosting service

## Support

For issues or questions, please contact the developer.