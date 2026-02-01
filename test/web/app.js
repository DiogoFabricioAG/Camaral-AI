const API_URL = "http://localhost:8000/api/v1/chat";
let sessionId = "test-session-" + Date.now();

const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const messagesContainer = document.getElementById("messagesContainer");

userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

function resetChat() {
  sessionId = "test-session-" + Date.now();
  messagesContainer.innerHTML = "";
  addMessage(
    "Hola, soy el asistente virtual de Camaral AI. ¿En qué puedo ayudarte hoy para potenciar tus ventas?",
    "bot",
  );
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  addMessage(text, "user");
  userInput.value = "";
  userInput.disabled = true;
  sendBtn.disabled = true;

  const loadingId = addLoading();

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        session_id: sessionId,
        message: text,
      }),
    });

    if (!response.ok) throw new Error("Network response was not ok");

    const data = await response.json();

    removeLoading(loadingId);
    addMessage(data.response, "bot");
  } catch (error) {
    removeLoading(loadingId);
    addMessage(
      "Lo siento, hubo un error de conexión. Por favor intenta de nuevo.",
      "bot",
    );
    console.error("Error:", error);
  } finally {
    userInput.disabled = false;
    sendBtn.disabled = false;
    userInput.focus();
  }
}

function addMessage(text, sender) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}-message`;

  const time = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  messageDiv.innerHTML = `
        <div class="message-content">${formatText(text)}</div>
        <div class="message-time">${time}</div>
    `;

  messagesContainer.appendChild(messageDiv);
  scrollToBottom();
}

function addLoading() {
  const id = "loading-" + Date.now();
  const messageDiv = document.createElement("div");
  messageDiv.className = `message bot-message`;
  messageDiv.id = id;

  messageDiv.innerHTML = `
        <div class="message-content">
            <span class="typing-dots">Escribiendo...</span>
        </div>
    `;

  messagesContainer.appendChild(messageDiv);
  scrollToBottom();
  return id;
}

function removeLoading(id) {
  const element = document.getElementById(id);
  if (element) element.remove();
}

function scrollToBottom() {
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function formatText(text) {
  const stripeRegex =
    /(https?:\/\/checkout\.stripe\.com\/c\/pay\/[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+)/g;

  let formatted = text
    .replace(
      stripeRegex,
      '<br><a href="$1" target="_blank" class="payment-btn">Pagar Ahora 💳</a><br>',
    )
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n/g, "<br>");

  return formatted;
}
