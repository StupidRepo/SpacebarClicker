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
Go to the [releases page][rel] and download the latest release that corresponds to your OS. Extract the zip file and run the executable file.

Alternatively, you could download the unstable builds which are made from the latest commit for:
- [macOS][mac]
- [Linux][lin]
and
- [Windows][win]

Executable file is:
- `SpacebarClicker.app` on macOS
- `SpacebarClicker` (the file without the file extentsion) on Linux
- `SpacebarClicker.exe` on Windows.
## Building
### macOS + Windows + Linux
Download the [source code](https://github.com/StupidRepo/SpacebarClicker/archive/refs/heads/main.zip), extract it, and run:
- `python3 -m pip install -r requirements.txt` if you're on any OS.
After that, run:
- `python3 build.py` if you're on macOS or GNU/Linux.
- `python3 buildWin.py` if you're on Windows.
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
[mac]: https://nightly.link/StupidRepo/SpacebarClicker/workflows/main/main/SpacebarClicker-macOS.zip
[win]: https://nightly.link/StupidRepo/SpacebarClicker/workflows/main/main/SpacebarClicker-Windows.zip
[lin]: https://nightly.link/StupidRepo/SpacebarClicker/workflows/main/main/SpacebarClicker-Linux.zip
[rel]: https://github.com/StupidRepo/SpacebarClicker/releases/latest
[bb-sr]: https://github.com/StupidRepo/