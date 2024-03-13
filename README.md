<h1 align="center">Multimodal Gamer</h1>

<p align="center">
  <strong>A framework to enable multimodal models to play games on a computer.</strong>
</p>
<p align="center">
  Using the same inputs and outputs as a human operator, the model plays a game!
</p>
<div align="center">
  <img src="https://github.com/joshbickett/multimodal-gamer/assets/42594239/f9fd7238-2d4c-46a0-94a4-484afb214375" width="300"  style="margin: 10px;"/>
</div>

## Key Features
- **Compatibility**: Designed for various multimodal models and games
- **Integration**: Currently integrated with **GPT-4**
- **Supported Games**:
  - Super Mario 64: https://www.smbgames.be/super-mario-64.php
  - Poker: https://www.247freepoker.com/
  - Coming soon: Chess.com

## Click below to see MultiModal Gamer play Super Mario 64 on YouTube

[![YouTube video player](https://img.youtube.com/vi/9Znt4dMAB7U/0.jpg)](https://www.youtube.com/watch?v=9Znt4dMAB7U)

## Quick install

Create venv
```
python3 -m venv env
```
Activate it (Mac)
```
source env/bin/activate
```
Install requirements
```
pip install -r requirements.txt
```
Add OpenAI Key
```
export OPENAI_API_KEY=yourkeyhere
```
Run it
```
python main.py
```
