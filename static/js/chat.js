async function sendMessage() {
    const input = document.getElementById("chat-input");
    const chatBox = document.getElementById("chat-box");

    const message = input.value.trim();
    if (!message) return;

    // User message
    chatBox.innerHTML += `
        <div class="chat-message user">
            <div class="chat-label">You</div>
            <div class="bubble">${message}</div>
        </div>
    `;
    input.value = "";

    // Running indicator
    const statusId = "scan-" + Date.now();
    chatBox.innerHTML += `
        <div class="chat-message ai" id="${statusId}">
            <div class="chat-label">Cyber AI</div>
            <div class="bubble">⏳ Running scan...</div>
        </div>
    `;
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        const statusDiv = document.getElementById(statusId);

        if (data.status === "done") {
            const output = Array.isArray(data.reply)
                ? data.reply.join("\n")
                : data.reply;

            statusDiv.innerHTML = `
                <div class="chat-label">Cyber AI</div>
                <div class="bubble">
                    ✅ <b>${data.tool.toUpperCase()} scan complete</b><br><br>
                    <pre>${output}</pre>
                </div>
            `;
        } else {
            statusDiv.innerHTML = `
                <div class="chat-label">Cyber AI</div>
                <div class="bubble">❌ ${data.reply}</div>
            `;
        }

    } catch (err) {
        document.getElementById(statusId).innerHTML = `
            <div class="chat-label">Cyber AI</div>
            <div class="bubble">❌ Network error</div>
        `;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}
