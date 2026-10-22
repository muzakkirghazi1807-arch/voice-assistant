const statusText = document.getElementById("status");
const responseBox = document.getElementById("response");
const listenButton = document.getElementById("listenButton");
const commandForm = document.getElementById("commandForm");
const commandInput = document.getElementById("commandInput");

// Flask backend address
const BACKEND_URL = "http://127.0.0.1:5000";
// Choose a male-sounding English voice if the browser has one installed.
let jarvisVoice = null;
function chooseJarvisVoice() {
    const voices = window.speechSynthesis.getVoices();
    const englishVoices = voices.filter(voice => /^en[-_]/i.test(voice.lang));
    const maleName = /\b(male|david|mark|guy|ryan|ravi|prabhat|daniel|george|james|matthew|andrew|aaron|anthony)\b/i;
    const naturalMale = englishVoices.find(voice =>
        maleName.test(voice.name) && /natural|neural|online/i.test(voice.name)
    );
    const maleEnglish = englishVoices.find(voice => maleName.test(voice.name));

    jarvisVoice = naturalMale || maleEnglish || null;
    if (jarvisVoice) {
        console.log("JARVIS voice:", jarvisVoice.name);
    } else {
        console.log("No male English voice found; using the browser default voice.");
    }
}

window.speechSynthesis.addEventListener("voiceschanged", chooseJarvisVoice);
chooseJarvisVoice();

// Speak a response and display it on the website
function speak(text) {
responseBox.textContent = text;
if (!("speechSynthesis" in window)) {
    statusText.textContent =
        "Your browser does not support speech synthesis.";
    return;
}

window.speechSynthesis.cancel();

const message = new SpeechSynthesisUtterance(text);
message.lang = jarvisVoice ? jarvisVoice.lang : "en-IN";
if (jarvisVoice) {
    message.voice = jarvisVoice;
}
message.rate = 0.95;
message.pitch = 1;

message.onstart = function () {
    statusText.textContent = "JARVIS is speaking...";
};

message.onend = function () {
    statusText.textContent = "Ready.";
};

message.onerror = function (event) {
    statusText.textContent = "Speech error: " + event.error;
    console.error("JARVIS speech error:", event);
};

window.speechSynthesis.speak(message);
}

// Search Google
function openSearch(query) {
const url =
"https://www.google.com/search?q=" +
encodeURIComponent(query);
window.open(url, "_blank");
}

// Send a command to the Python backend
async function askPython(command) {
statusText.textContent = "JARVIS is thinking...";
try {
    const response = await fetch(
        `${BACKEND_URL}/command`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                command: command
            })
        }
    );

    const data = await response.json();

    if (!response.ok) {
        speak(data.response || "Sorry, something went wrong.");
        return;
    }

    speak(data.response || "I received your command.");

} catch (error) {
    console.error("Python backend error:", error);

    speak(
        "I could not connect to my Python backend. " +
        "Please make sure the JARVIS server is running."
    );
}
}

// Process commands received from typing or voice
async function handleCommand(input) {
const command = input.toLowerCase().trim();
if (command === "") {
    speak("Please enter a command.");
    return;
}

statusText.textContent = "Command received.";

// Commands handled directly by the browser
if (command.includes("open google")) {
    speak("Opening Google.");
    window.open("https://www.google.com", "_blank");
    return;
}

if (command.includes("open youtube")) {
    speak("Opening YouTube.");
    window.open("https://www.youtube.com", "_blank");
    return;
}

if (command.includes("open gmail")) {
    speak("Opening Gmail.");
    window.open("https://mail.google.com", "_blank");
    return;
}

if (
    command.startsWith("search for ") ||
    command.startsWith("search ")
) {
    const query = command.startsWith("search for ")
        ? command.substring(11).trim()
        : command.substring(7).trim();

    if (query) {
        speak("Searching Google for " + query);
        openSearch(query);
    } else {
        speak("Please tell me what you want to search for.");
    }

    return;
}

if (command.startsWith("wikipedia ")) {
    const topic = command.substring(10).trim();

    if (topic) {
        speak("Searching Wikipedia for " + topic);

        window.open(
            "https://en.wikipedia.org/wiki/Special:Search?search=" +
            encodeURIComponent(topic),
            "_blank"
        );
    } else {
        speak("Please provide a Wikipedia topic.");
    }

    return;
}

if (
    command === "exit" ||
    command === "stop jarvis"
) {
    speak("Goodbye! You can return whenever you need me.");
    return;
}

// Send other commands to Python
await askPython(command);
}

// Handle typed commands
commandForm.addEventListener("submit", function (event) {
event.preventDefault();
const command = commandInput.value.trim();

commandInput.value = "";

handleCommand(command);
});

// Voice recognition
const SpeechRecognition =
window.SpeechRecognition ||
window.webkitSpeechRecognition;

if (SpeechRecognition) {
const recognition = new SpeechRecognition();
recognition.lang = "en-IN";
recognition.continuous = false;
recognition.interimResults = false;

listenButton.addEventListener("click", function () {
    statusText.textContent = "Listening...";

    try {
        recognition.start();
    } catch (error) {
        statusText.textContent =
            "Already listening. Please try again.";
    }
});

recognition.onresult = function (event) {
    const transcript =
        event.results[0][0].transcript;

    commandInput.value = transcript;

    handleCommand(transcript);
};

recognition.onerror = function (event) {
    statusText.textContent =
        "Voice error: " + event.error +
        ". Please try typing your command.";

    console.error("Voice recognition error:", event);
};

recognition.onend = function () {
    if (statusText.textContent === "Listening...") {
        statusText.textContent = "Ready.";
    }
};
} else {
listenButton.disabled = true;
statusText.textContent =
    "Voice recognition is not supported in this browser. " +
    "Please type your commands.";
}




