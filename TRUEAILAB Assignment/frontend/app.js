document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const messageInput = document.getElementById("message-input");
    const sendBtn = document.getElementById("send-btn");
    const newChatBtn = document.getElementById("new-chat-btn");
    const loadingIndicator = document.getElementById("loading");

    // Manage or initialize Session ID
    if (!localStorage.getItem("sessionId")) {
        localStorage.setItem("sessionId", "sess_" + Math.random().toString(36).substr(2, 9));
    }

    function appendMessage(text, sender) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", sender);
        msgDiv.innerText = text;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto Scroll
    }

    async function sendMessage() {
        const text = messageInput.value.trim();
        if (!text) return;

        appendMessage(text, "user");
        messageInput.value = "";
        loadingIndicator.classList.remove("hidden");

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    sessionId: localStorage.getItem("sessionId"),
                    message: text
                })
            });

            const data = await response.json();
            loadingIndicator.classList.add("hidden");

            if (response.ok) {
                appendMessage(data.reply, "assistant");
            } else {
                appendMessage("Error: " + (data.detail || "Failed to fetch response."), "assistant");
            }
        } catch (error) {
            loadingIndicator.classList.add("hidden");
            appendMessage("Network error occurred. Please verify backend is running.", "assistant");
        }
    }

    sendBtn.addEventListener("click", sendMessage);
    messageInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });

    newChatBtn.addEventListener("click", () => {
        localStorage.setItem("sessionId", "sess_" + Math.random().toString(36).substr(2, 9));
        chatBox.innerHTML = "";
        appendMessage("Hello! Started a brand new session. How can I help you from the documents base today?", "assistant");
    });
});