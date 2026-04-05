# Voice AI Setup Notes

This setup is based on your Python script using speech recognition, OpenAI, and audio output.

---

## 1) Open Terminal

Open:
- Command Prompt / PowerShell (Windows)
- Terminal (Mac/Linux)

---

## 2) Activate Virtual Environment (Windows)

```powershell
.venv\Scripts\activate
```

### Explanation
Activates your project’s Python environment so packages install locally.

---

## 3) Upgrade pip

```powershell
python -m pip install --upgrade pip
```

### Explanation
Updates the package installer to avoid errors.

---

## 4) Install Required Libraries

```powershell
pip install openai
pip install requests
pip install pydantic
pip install python-dotenv
pip install SpeechRecognition
```

### Explanation
- `openai` → AI + TTS
- `requests` → API calls (weather)
- `pydantic` → structured output
- `dotenv` → load API key
- `SpeechRecognition` → speech → text

---

## 5) Install Audio Support (Important)

### Windows

```powershell
pip install pyaudio
```

### Mac

```bash
brew install portaudio
pip install pyaudio
```

### Explanation
Required for microphone access.

---

## 6) Install SpeechRecognition Audio Extras

```powershell
pip install SpeechRecognition[audio]
```

### Explanation
Adds extra audio dependencies.

---

## 7) Create `.env` File

Create a file:

```
.env
```

Add:

```
OPENAI_API_KEY=your_api_key_here
```

### Explanation
Stores your API key securely.

---

## 8) Save Your Python File

Example:

```bash
main.py
```

---

## 9) Run the Project

```powershell
python main.py
```

### Explanation
Starts:
- Microphone listening
- Speech → text
- AI processing
- Text → speech response

---

## 10) Flow of Program

1. Speak into mic
2. Speech → text
3. Sent to AI
4. AI processes (PLAN / TOOL / OUTPUT)
5. Response spoken back

---

## Notes

- Allow microphone permissions
- Keep API key private
- Fix PyAudio errors if needed (common on Windows)
- Internet required

---

### other 
 - file like 
 **script.js , index.html, style.css** is created when you are giving the prompt in cursor.py for building the todo app 