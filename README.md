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
- **Compatibility**: Designed to be compatible with various multimodal models and games
- **Models**: Currently integrated with **GPT-4**
- **Supported Games**:
  - Super Mario 64: https://www.smbgames.be/super-mario-64.php
  - Poker: https://www.247freepoker.com/
  - Chess: https://www.chess.com/
    - Requires Chess.com Keyboard: https://chromewebstore.google.com/detail/chesscom-keyboard/bghaancnengidpcefpkbbppinjmfnlhh

## Demo of Multimodal Gamer playing on Chess.com

https://github.com/joshbickett/multimodal-gamer/assets/42594239/2d557fc9-3d93-4bc7-9636-376861418298

## Quick install

1. Create a virtual environment:
    ```bash
    python3 -m venv env
    ```
2. Activate the virtual environment (Mac/Linux):
    ```bash
    source env/bin/activate
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Add your OpenAI API key:
    ```bash
    export OPENAI_API_KEY=yourkeyhere
    ```


## Running the Game

To run a specific game, use the `-game` flag followed by the name of the game. For example, to play chess:

```bash
python main.py --game chess
```

