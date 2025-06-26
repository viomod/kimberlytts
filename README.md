# Kimberly TTVC
A Text To Voice Chat for Kimberly TTS, Defaults to a VB Audio Cable, If you do not have VB download it [here](https://vb-audio.com/Cable/).

## Requirements

You will need to download FFmpeg using this command.

```bash
  winget install "FFmpeg (Essentials Build)" 
```

Then download the requirements like this.

```bash
  pip install tk requests sounddevice numpy pydub
```

## Built It Yourself

Simply download the source code and run this to compile it to an EXE.

```python
  pyinstaller --onefile --noconsole --icon=mic.ico app.py 
```

For debug purposes feel free to remove "--noconsole".

If you d not have pyinstaller run this.

```python
  pip install pyinstaller
```
