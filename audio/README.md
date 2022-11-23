## CUE Splitting

Install `shntool`:

```sh
sudo apt install shntool
```

Split into `flac` with formatted filenames (`%p` for performer, `%a` for album, `%t` for title, and `%n` for track number) [^archwiki]:

```sh
shnsplit -t "%n-%t" -f index.cue -o flac index.ape
```

[^archwiki]: CUE Splitting - ArchWiki, https://wiki.archlinux.org/title/CUE_Splitting

### Codec

#### flac

```
sudo apt install flac
```

#### ape

[Monkeys's Audio](https://monkeysaudio.com) is a codec for ape. A prebuilt Ubuntu package `mac` at [PPA](https://launchpad.net/~flacon/+archive/ubuntu/ppa) `flacon` is available [^ppa].

[^ppa]: audio - Why can I not split a .ape file? - Unix & Linux Stack Exchange, https://unix.stackexchange.com/a/227252

However this only has amd64 builds. Thus for arm64 we need to build manually:

- Download source code at https://monkeysaudio.com/developers.html
- `Makefile` is at `Source/Projects/NonWindows/`
- `make`
- `sudo make install`
- `sudo ln -s /usr/local/lib/libMAC.so.8 /usr/lib/libMAC.so.8`
    - The program seems to be unable find the lib unless at `/usr/lib/`.
