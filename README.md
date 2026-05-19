# File Automation Tools

Two simple Python scripts to manage and find files on your Mac.

---

## 1. File Organizer (`file_organizer.py`)

Automatically sorts files in a folder into subfolders by type (Images, Documents, Videos, etc.).

**Usage:**

```bash
# Organize your Downloads folder (default)
python3 file_organizer.py

# Organize any other folder
python3 file_organizer.py ~/Desktop/MyFolder
```

**Folders it creates:**

| Folder | File Types |
|---|---|
| Images | .jpg, .jpeg, .png, .gif, .webp |
| Documents | .pdf, .docx, .txt, .xlsx, .html |
| Videos | .mp4, .mov, .avi, .mkv |
| Audio | .mp3, .wav, .aac, .flac |
| Archives | .zip, .tar, .gz, .rar |
| Installers | .dmg, .pkg, .exe |
| Code | .py, .js, .ts, .css, .json |
| Network | .pkt, .pcap |
| Others | anything not listed above |

---

## 2. File Finder (`find_file.py`)

Searches your entire Mac for a file by name (partial or full) and opens its location in Finder.

**Setup — create a shortcut so you can use it from anywhere:**

```bash
echo 'alias findfile="python3 ~/Desktop/P/find_file.py"' >> ~/.zshrc
source ~/.zshrc
```

**Usage:**

```bash
# Search by partial name
findfile photo

# Search by full name (spaces are supported)
findfile Biniam Tsige CV
```

It will list all matches. Then type a **number** or the **exact filename** to open it in Finder.

---

## Requirements

- macOS
- Python 3 (comes pre-installed on most Macs)
- No external libraries needed
