# 🚀 Assistant Sh1v `v0.2.1 Beta`
A personal desktop assistant I'm building to learn software development while making something I actually want to use. My focus has shifted from simple prototyping to building a robust, crash-proof architecture capable of handling complex tasks without UI freezes or memory instability.
---
## 🛠️ About The Project
This project is built using my own work mixed with some AI-assisted tools.
### UI & Frontend
Designed in Canva and implemented using **PySide6**. The UI is built to be responsive and decoupled from the engine to ensure a smooth user experience.
### Backend & App Logic
The engine, action routing, and feature integration are maintained by me. I am currently hardening the architecture to prevent memory corruption (Segmentation Faults) and ensuring thread safety using `QThread` and signal/slot communication.
---
## 📈 Current Features
### ✅ Implemented
- **Dynamic command parsing:** Extracts intent from natural language.
- **Resilient execution:** Custom `@log_and_guard` decorator to catch errors without crashing the entire app.
- **Modular architecture:** Clean separation between UI, Engine, and Actions.
- **Asynchronous Processing:** Full implementation of `QThread` to prevent UI freezing during network requests.
- **Remote Device Control:** Cross-device command routing (currently under active refinement).
- **Stable Logging:** Custom, non-blocking file-based logging to replace volatile system-wide configurations.
---
## 🔄 What I'm Working On Now
- **Hardened Execution:** Finalizing error handling for remote device communication (Timeouts & Retries).
- **Workflow Optimization:** Transitioning to a hybrid development environment (External browser-based IDEs with local command-line execution) to bypass mobile storage constraints.
- **Stability:** Eliminating race conditions and resource contention in the background worker threads.
---
## 🎯 Long-Term Goals
- [ ] Voice interaction
- [ ] Local AI integration (Ollama / Mistral)
- [ ] ESP32 hardware control
- [ ] Email and messaging automation
- [ ] Context-aware conversations
- [ ] Plugin-based command system
---
## 📋 Project Info

| Field | Details |
| :--- | :--- |
| Version | `v0.2.1 Beta` |
| Language | Python |
| Framework | PySide6 |
| Dev Environment | Pydroid 3  |
| Status | 🟢 Hardening Architecture |

## Latest Update 
- In files `action.py`, `engine.py`and `ui.py`
- ## Brand New UI
  - Updated UI with dark mode and light mode options.
  - settings have a window where you can change your username too
  - focus mode in settings where you can talk with your Local AI models in future
- ## Brand new type of Engine
  - Added a NLP (Natural Language Processing) for better output and response
  - API based calls will be added in few days (Groq).
  - <img width="1340" height="800" alt="1000026381" src="https://github.com/user-attachments/assets/628775a6-a8fd-45c5-b030-303baf20d882" />

---
> This project has evolved from a learning experiment into a study of robust software architecture. By prioritizing stability and clean design over quick-and-dirty features, I am building a system that is not only functional but maintainable and professional.
