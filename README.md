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
## Installing
### macOS + Windows + Linux
Latest stable build:
- [macOS][macs]
- [Windows][wins]
- [Linux][lins]
- [All][alls]

Latest unstable builds:
- [macOS][macu]
- [Windows][winu]
- [Linux][linu]
- [All][allu]

(Unstable build may reset your save file!)

The executable is `SpacebarClicker.app` for macOS, `SpacebarClicker` (the file without the file extentsion) for Linux or `SpacebarClicker.exe` for Windows.
## Building
### macOS + Windows + Linux
Download the [source code](https://github.com/StupidRepo/SpacebarClicker/archive/refs/heads/main.zip), extract it, and run:
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

[source]: https://github.com/StupidRepo/SpacebarClicker/archive/refs/heads/main.zip

[macu]: https://nightly.link/StupidRepo/SpacebarClicker/workflows/main/main/macOS.zip
[macs]: https://github.com/StupidRepo/SpacebarClicker/releases/latest/download/macOS.zip

[winu]: https://nightly.link/StupidRepo/SpacebarClicker/workflows/main/main/Windows.zip
[wins]: https://github.com/StupidRepo/SpacebarClicker/releases/latest/download/Windows.zip

[linu]: https://nightly.link/StupidRepo/SpacebarClicker/workflows/main/main/Linux.zip
[lins]: https://github.com/StupidRepo/SpacebarClicker/releases/latest/download/Linux.zip

[allu]: https://nightly.link/StupidRepo/SpacebarClicker/workflows/main/main
[alls]: https://github.com/StupidRepo/SpacebarClicker/releases/latest

[bb-sr]: https://github.com/StupidRepo/