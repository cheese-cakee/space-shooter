# 🚀 Space Shooter Game

A modern, web-based space shooter game built with Python and Pygame, featuring smooth gameplay, animated explosions, and a complete menu system. Play directly in your browser!


<img width="1594" height="931" alt="{A5ED6D04-CA41-4F7F-8A23-3F6425FF14FC}" src="https://github.com/user-attachments/assets/de36581a-895f-45ac-83ba-d105539d7bd1" />


## 🎮 [Play Now on Vercel](https://space-shooter-five-liart.vercel.app/)

## ✨ Features

### 🎯 Gameplay
- **Smooth Player Movement** - Responsive arrow key controls with boundary collision
- **Laser Shooting System** - Space key firing with cooldown mechanics  
- **Dynamic Meteor Spawning** - Randomly generated meteors with varying speeds and rotation
- **Collision Detection** - Pixel-perfect collision using pygame masks
- **Animated Explosions** - 21-frame explosion animations for immersive feedback
- **Real-time Scoring** - Time-based scoring system with live updates

### 🎨 User Interface
- **Professional Main Menu** - Clean UI with game title and navigation
- **Game Over Screen** - Score display with restart/menu options
- **Leaderboard System** - Top 10 high scores with JSON persistence
- **Responsive Design** - Works on desktop and mobile browsers
- **Custom Typography** - Oxanium font for futuristic aesthetic

### 🔊 Audio & Visual Effects
- **Spatial Audio** - Laser firing and explosion sound effects
- **Background Music** - Ambient space music during gameplay
- **Rotating Sprites** - Dynamic meteor rotation for realism
- **Particle System** - Animated star background
- **Smooth Animations** - Delta-time based movement for consistent frame rates

### 🌐 Web Deployment
- **Browser Compatible** - Runs natively in web browsers using WebAssembly
- **Cross-Platform** - Works on Windows, Mac, Linux

## 🛠️ Technology Stack

- **Python 3.11+** - Core game logic
- **Pygame** - Game engine and graphics
- **Pygbag** - Web deployment via WebAssembly
- **JSON** - Data persistence for leaderboards
- **HTML5 Canvas** - Web rendering
- **Vercel** - Web hosting and deployment

## 🎮 Controls

| Key | Action |
|-----|--------|
| ↑↓←→ | Move spaceship |
| Space | Fire laser |
| ESC | Return to menu |
| Mouse | Navigate menus |

## 🚀 Quick Start

### Play Online
Simply visit the [live demo](https://space-shooter-five-liart.vercel.app/) - no installation required!

### Run Locally
```bash
# Clone the repository
git clone https://github.com/yourusername/spaceshooter.git
cd spaceshooter

# Install dependencies
pip install pygame

# Run the game
python main.py
```

### Web Development
```bash
# Install pygbag for web deployment
pip install pygbag

# Build for web
pygbag .

# Access at http://localhost:8000
```

## 📁 Project Structure

```
spaceshooter/
├── main.py                 # Main game file with async web support
├── images/                 # Game assets
│   ├── player.png         # Spaceship sprite
│   ├── meteor.png         # Meteor sprite  
│   ├── laser.png          # Laser projectile
│   ├── star.png           # Background stars
│   ├── Oxanium-Bold.ttf   # Custom font
│   └── explosion/         # 21-frame explosion animation
│       ├── 0.png
│       └── ...
├── audio/                 # Sound effects and music
│   ├── laser.wav          # Laser firing sound
│   ├── explosion.wav      # Explosion sound effect
│   └── game_music.wav     # Background music
├── leaderboard.json       # High score persistence
└── README.md             # This file
```

## 🎯 Game Mechanics

### Scoring System
- **Time Survival**: Score increases based on survival time
- **Formula**: `(current_time - start_time) // 100`
- **Leaderboard**: Top 10 scores saved locally

### Difficulty Progression
- **Meteor Spawn Rate**: Every 500ms consistently
- **Varied Meteor Speed**: 400-500 pixels per second
- **Random Trajectories**: Slight horizontal movement variation
- **Rotation Effects**: Each meteor rotates at different speeds

### Physics Engine
- **Delta Time Movement**: Smooth 60 FPS gameplay
- **Boundary Collision**: Player stays within screen bounds
- **Mask-based Detection**: Pixel-perfect collision detection
- **Vector Mathematics**: Normalized movement for diagonal consistency

### Asset Guidelines
- **Images**: PNG format with alpha transparency
- **Audio**: WAV format, 44.1kHz recommended  
- **Fonts**: TTF format for cross-platform compatibility

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📈 Future Enhancements

- [ ] Power-ups and weapon upgrades
- [ ] Multiple enemy types
- [ ] Parallax scrolling backgrounds  
- [ ] Achievement system
- [ ] Multiplayer support
- [ ] Progressive Web App (PWA) features

***

⭐ **Star this repository if you enjoyed the game!**
