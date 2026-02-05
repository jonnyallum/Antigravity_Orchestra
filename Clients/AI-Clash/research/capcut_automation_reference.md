# 🛠️ CAPCUT AUTOMATION TECHNICAL REFERENCE
**Goal:** Programmatic manipulation of CapCut Pro for AgOS 3.0.

## 1. The Manipulation Path
CapCut project files (`.json`) are stored in the local `AppData` directory.
- **Path template**: `%LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft\[DraftName]`
- **Structure**: The `draft_content.json` file contains every track, clip, effect, and text overlay.

## 2. The Automation Toolset
We will use an open-source Python wrapper for the CapCut Draft format.
- **Tool**: `pyCapCut`
- **Capabilities**:
    - **Add Clips**: Insert Leo and Victor's generated video tracks.
    - **Text-to-Captions**: Programmatically create the "Leo: [Script text]" and "Victor: [Script text]" overlays.
    - **Music Layering**: Auto-add trending audio backgrounds.
    - **Draft Export**: Trigger the CapCut UI to open and export the final project (requires headless automation via `pyautogui` or specific draft-save hooks).

## 3. The Agent Workflow
1.  **@Echo** writes the script.
2.  **@Priya** generates the characters and backgrounds.
3.  **@Autoflow** runs the `draft_generator.py` script (to be created tomorrow) which builds the CapCut project.
4.  **You (User)**: Open CapCut, see a perfectly assembled "AI-Clash" draft, and hit export.

## 4. Why Use CapCut Pro?
- **Pro Effects**: Access to high-quality transitions and trending visual filters.
- **Performance**: Faster rendering than local FFmpeg for complex vertical video effects.
- **Quality Control**: Allows you to perform a 10-second "sanity check" before anything goes live.
