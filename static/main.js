function updateTranscript(text) {
    const transcriptDiv = document.getElementById('transcript');
    transcriptDiv.innerHTML += `<p>${text}</p>`;
}

document.getElementById('start-btn').addEventListener("click", () => {
    fetch("/start-call", { method: "POST" })
      .then(response => response.json())
      .then(data => updateTranscript(data.message))
      .catch(err => updateTranscript("Error starting conversation."));
});

document.getElementById('stop-btn').addEventListener("click", () => {
    fetch("/stop-call", { method: "POST" })
      .then(response => response.json())
      .then(data => updateTranscript(data.message))
      .catch(err => updateTranscript("Error stopping conversation."));
});

document.getElementById('exchange-btn').addEventListener("click", () => {
    fetch("/select-exchange", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ exchange: "Binance" })
    })
    .then(response => response.json())
    .then(data => updateTranscript(data.message))
    .catch(err => updateTranscript("Error selecting exchange."));
});

document.getElementById('symbol-btn').addEventListener("click", () => {
    fetch("/select-symbol", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ exchange: "binance", symbol: "BTCUSDT" })
    })
    .then(response => response.json())
    .then(data => updateTranscript(data.message))
    .catch(err => updateTranscript("Error selecting symbol."));
});

document.getElementById('order-btn').addEventListener("click", () => {
    fetch("/place-order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ exchange: "Binance", symbol: "BTCUSDT", quantity: "1", targetPrice: "25000" })
    })
    .then(response => response.json())
    .then(data => updateTranscript(data.message))
    .catch(err => updateTranscript("Error placing order."));
});

// Check if the browser supports SpeechRecognition (or webkitSpeechRecognition)
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRecognition) {
  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = "en-US";

  document.getElementById('voice-start-btn').addEventListener('click', () => {
    recognition.start();
  });

  recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript.trim().toLowerCase();
    updateTranscript(`You said: ${transcript}`);

    // If the user selects Binance first
    if (transcript.includes("binance")) {
        fetch("/select-exchange", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ exchange: "binance" })
        })
        .then(response => response.json())
        .then(data => {
            updateTranscript(data.message);
            speakText(data.message);
        })
        .catch(err => updateTranscript("Error selecting exchange."));
    }
    // Otherwise, assume they are specifying a symbol
    else {
        fetch("/select-symbol", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ symbol: transcript }) // Send exact voice text
        })
        .then(response => response.json())
        .then(data => {
            updateTranscript(data.message);
            speakText(data.message);
        })
        .catch(err => updateTranscript("Error selecting symbol."));
    }
};

  recognition.onerror = function (event) {
    console.error("Voice recognition error:", event.error);
    updateTranscript("Voice recognition error: " + event.error);
  };
} else {
  updateTranscript("Your browser does not support the Web Speech API.");
}

function speakText(text) {
  const synth = window.speechSynthesis;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US";
  synth.speak(utterance);
}

// After updating the transcript, you can call this function:
function updateTranscript(text) {
  const transcriptDiv = document.getElementById('transcript');
  transcriptDiv.innerHTML += `<p>${text}</p>`;
  // Also speak the response aloud:
  speakText(text);
}

recognition.onresult = (event) => {
  const transcript = event.results[0][0].transcript;
  updateTranscript(`You said: ${transcript}`);

  // Send to /select-exchange endpoint as an example:
  fetch("/select-exchange", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ exchange: transcript })
  })
  .then(response => response.json())
  .then(data => {
    updateTranscript(data.message);
    speakText(data.message);
  })
  .catch(err => updateTranscript("Error processing the exchange selection."));
};

