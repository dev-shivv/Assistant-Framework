# 🚀 Assistant Sh1v `v0.2 Beta`

A personal desktop assistant I'm building to learn software development while making something I actually want to use.

The idea is simple — type or speak a command, the assistant gets it, sends it to the right action, and replies in a natural way. The project is still being built, but my main focus right now is making the core engine accurate, stable, and easy to add stuff to.

---

## 🛠️ About The Project

This project is built using my own work mixed with some AI-assisted tools.

### UI & Frontend

I designed the interface in Canva and converted it into PySide6 code with help from Gemini. Since I'm coding on an Android device, AI-assisted UI generation lets me focus more time on the logic and structure of the app.

### Backend & App Logic

The backend, command parsing system, action routing, and feature integration — all of that is built and maintained by me.

I'm still learning Python and PySide6, so I don't know every part of every library. But I do understand how the different pieces work together and how to keep adding features without breaking what already works.

---

## 📈 Current Features

### ✅ Implemented

- **Dynamic command parsing**
  - Pulls out the useful info from natural commands like:
    > *"play believer on youtube"* → Query: `believer`

- **Typo correction using `difflib`**
  - Helps when there's a small spelling mistake or the command doesn't match perfectly

- **Modular architecture**
  - UI, engine, and action layers are all kept separate

- **Command routing system**
  - Matches what the user types/says and runs the right action

---

## 🔄 What I'm Working On Now

- Adding `QThread` for background tasks
- Stopping the UI from freezing during network stuff
- Making the command parser more reliable
- Cleaning up the engine so it's easier to expand later

---

## 🎯 Long-Term Goals

- [ ] Voice interaction
- [ ] Local AI integration (Ollama / Mistral)
- [ ] ESP32 hardware control
- [ ] Email and messaging automation
- [ ] Scheduling and reminders
- [ ] Context-aware conversations
- [ ] Plugin-based command system

---

## 📋 Project Info

| Field | Details |
|---|---|
| Version | `v0.2 Beta` |
| Language | Python |
| Framework | PySide6 |
| Dev Environment | Android (Pydroid 3) |
| Status | 🟢 Active Development |

---

> This project started as a learning experiment and slowly became my main long-term software project. Every new feature teaches me something new about how software actually works — architecture, problem-solving, all of it.
