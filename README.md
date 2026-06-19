# 🚀 Assistant Sh1v `v0.2.1 Beta` [PAUSED]
> **PROJECT STATUS: ARCHIVED**
> *Development on this mobile (Pydroid 3) version is currently paused due to hardware resource constraints. All architecture, logic, and UI design are stable and ready to be ported to a desktop environment (Laptop) in the next phase.*
---
## 🛠️ About The Project
This project is an evolving personal assistant built to master software architecture, concurrency, and modular design. My focus has shifted from prototyping to a **robust, crash-proof architecture** designed to handle complex tasks without UI freezes or memory instability.
### UI & Frontend
- Built with **PySide6**. 
- Designed for responsiveness, featuring a sophisticated dark/light mode dashboard.
- Decoupled from the engine to ensure a smooth, non-blocking user experience.
### Backend & App Logic
- Logic, engine parsing, and action routing are maintained as modular components.
- Hardened architecture utilizing `QThread` and signal/slot communication to prevent segmentation faults and race conditions.
---
## 📈 Current Features (Mobile-Stable Version)
### ✅ Implemented
- **Dynamic NLP command parsing:** Extracts intent from natural language.
- **Resilient execution:** Custom `@log_and_guard` decorator to catch runtime errors.
- **Asynchronous Processing:** Full implementation of `QThread` to prevent UI freezing during network/API calls.
- **Advanced Dashboard:** Real-time system monitor (CPU/RAM), integrated weather, and interactive logs.
- **Settings & Personalization:** Modular settings allowing for username customization and future-ready AI configuration.
---
## 🔄 Roadmap: Laptop Porting Strategy
*When transitioning to a desktop environment, the following steps will be executed:*
1. **Environment Migration:** Setup a full development environment (VS Code/PyCharm) with proper virtual environments (`venv`).
2. **Hybrid Engine Integration:** Implement the 3-mode routing system (**Offline/Hybrid/Online**) leveraging the Groq API for intelligent fallback.
3. **Database Decoupling:** Migrate user settings and project history from local variables to a persistent database (SQLite/Django integration).
4. **Hardware Expansion:** Implement local LLM support (e.g., Ollama/Mistral) and ESP32 hardware control.
---
## 🎯 Long-Term Goals
- [ ] Voice interaction
- [ ] Full local AI integration (Ollama / Mistral)
- [ ] ESP32 hardware control
- [ ] Email and messaging automation
- [ ] Context-aware conversation memory
- [ ] Plugin-based command system
---
## 📋 Project Info

| Field | Details |
| :--- | :--- |
| Version | `v0.2.1 Beta` |
| Language | Python |
| Framework | PySide6 |
| Dev Environment | Pydroid 3 (Paused) |
| **Status** | ⏸️ **Archived - Awaiting Laptop Port** |

---
> This project has evolved from a learning experiment into a study of robust software architecture. By prioritizing stability and clean design over "quick-and-dirty" features, I am building a system that is functional, maintainable, and professional.
