# Spacebar Clicker
A free and fun game made in [Python][py], using the [`pygame`][pg] library.
## Description
Think of Cookie Clicker, but you have to press your space(bar) key to get 'spaces' (which are like cookies, but Spacebar Clicker's version).
## Custom In-Game Statuses
You can make your own in-game statuses by editing the `assets/core/descriptions.json` file.
Formatting goes as follows:
```
{clicks} - how many spaces you have
{cpc} - how many spaces you get per click
{chanceToClick} - the chance to get a space (hard mode only)
{version} - the current version of the game
{space} - is either 'spaces' if you have more than 1 space, or 'space' if you have 1 space
{intlimit} - the limit of an integer
{untilintlimit} - the amount of spaces until you reach the integer limit
```
An example would be:
```json
{
  "count": 420,
  "text": "You have {clicks} {space}, and this message will show at 420+ spaces!"
}
```
## Keybinds
```
Spacebar/Space/Return/Backspace - Click
M - Mute audio
C - Reset window size
F - Toggle resizeability
X - Reset save file
A - Toggle Keyism
```
## Updating
### macOS + Windows + Linux
To update the game, you will need to download the latest stable build from the [releases page][alls] (or an [unstable build](#installing)), and then run the game as normal from the new executable file.

> **Warning**: Your save file will be erased, ***HOWEVER*** it will copy your spaces and cpc to the new save file. Please do **NOT** downgrade your game, as it is not supported and you will not receive any help if you do so.
## Installing
### macOS + Windows + Linux
> **Note**: For macOS builds, you will need to open `Terminal.app` and run `chmod +x /path/to/SpacebarClicker` to make the file executable. (e.g. if the file is in your Downloads folder, you will need to run `chmod +x ~/Downloads/SpacebarClicker/SpacebarClicker`)

Latest stable build:
- [macOS][macs]
- [Windows][wins]
- [GNU/Linux][lins]
- [All][alls]

Latest unstable build:
- [macOS][macu]
- [Windows][winu]
- [GNU/Linux][linu]
- [All][allu]

> **Warning**: Updating your game will erase your save file. See [`Updating`](#updating) for more information on what happens.

### What's the 'executable file'?
The executable is `SpacebarClicker` (the file without the file extenstion) for macOS, `SpacebarClicker` (the file without the file extentsion) for GNU/Linux or `SpacebarClicker.exe` for Windows.
## Building
### macOS + Windows + Linux
`git clone` the repository, then run:
- `python3 -m pip install -r requirements.txt` if you're on any OS.
After that, run:
- `python3 buildWin.py` if you're on Windows.
- `python3 build.py` if you're on macOS or GNU/Linux.
## Contributing
I will greatly appreciate it if you contribute to the game.
You can contribute by making forking the repository, making your changes and then making a pull request.
## Credits/Contributors
- Bradlee Barnes ([StupidRepo][bb-sr])
## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for more information.

[py]: https://www.python.org/
[pg]: https://www.pygame.org/

[macu]: https://nightly.link/StupidRepo/SpacebarClicker/workflows/main/main/macOS.zip
[macs]: https://github.com/StupidRepo/SpacebarClicker/releases/latest/download/macOS.zip

[winu]: https://nightly.link/StupidRepo/SpacebarClicker/workflows/main/main/Windows.zip
[wins]: https://github.com/StupidRepo/SpacebarClicker/releases/latest/download/Windows.zip

[linu]: https://nightly.link/StupidRepo/SpacebarClicker/workflows/main/main/Linux.zip
[lins]: https://github.com/StupidRepo/SpacebarClicker/releases/latest/download/Linux.zip

[allu]: https://nightly.link/StupidRepo/SpacebarClicker/workflows/main/main
[alls]: https://github.com/StupidRepo/SpacebarClicker/releases/latest

[bb-sr]: https://github.com/StupidRepo/