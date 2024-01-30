# Design Pediatric CT (Flet App) <a href="https://github.com/Lightbridge-KS/PedDesign-flet"><img src="assets/icon.png" align="right" height="138" /></a>

> **Cross-platform app for design pediatric CT protocol.**

**Build using [Flet](https://flet.dev/)**, a cross-platform UI framework in Python.

## Build from Source

### Installation

1. Install [flet](https://flet.dev/docs/guides/python/getting-started) and [pyperclip](https://pypi.org/project/pyperclip/) with:

```shell
pip install -r requirements.txt
```

2. [Install Flutter](https://docs.flutter.dev/get-started/install)


### Build app

```shell
cd to/directory
# Build
flet build <target_platform>
```

`<target_platform>` could be one of the following: `apk`, `aab`, `ipa`, `web`, `macos`, `windows`, `linux`.
