# Archlinux Configuration


## Window Manager/ Desktop Environment

### Xorg

- KDE cannot set different scaling for multiple displays, which is essential when multiple displays differ in terms of DPI.
- GNOME supports that but needs patches to enable fractional scaling.
- In i3 the different-scaling issue can be resolved using `xrandr`.

### Wayland

Multiple displays is better supported. I tried Sway and it's powerful and easy to use.

However at the time of writing, Fcitx5 under Wayland is hardly usable and xwayland in HiDPI is blurry.
