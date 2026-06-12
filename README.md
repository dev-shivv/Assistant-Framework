# Assistant-Framework

A Python-based personal assistant that performs web and device 
operations through natural text commands. Built from scratch 
with a modular structure — brain, actions, and UI fully separated.

## Current Features
- Search and play on YouTube
- Search on Google
- Open Claude, ChatGPT, Gemini, GitHub, Spotify
- Natural command parsing using regex engine

## Project Structure
- `actions.py` — all web and app functions
- `engine.py` — command parsing brain
- `ui.py` — for UI
- `StyleSheet.qss` for UI styling
- `app.py` — connecting point

## Vision
A fully functional desktop assistant that understands natural 
language commands and performs real device operations — opening 
apps, managing files, playing media, searching the web, and more.
Not a toy project. Built to actually use daily.

## Roadmap
- [x] Structure Understandings
- [x] Simple Logic Implementation
- [x] CLI
- [x] Command parsing engine
- [x] Web and app actions
- [x] PySide6 UI with live terminal display panel
- [o] File and app management commands
- [o] Stable v1.0 release

## Tech Stack
- Python
- `re` module — command parsing
- `webbrowser` module — web actions
- `PySide6` module — For UI FrameWork
- `os` module — For OS related operations
- `sys` module — for system
- `difflib` module — for typo handeling
- `requests` module for API call

## Status
🔨 Active Development — v0.1

## Developer
[dev-shivv](https://github.com/dev-shivv)
