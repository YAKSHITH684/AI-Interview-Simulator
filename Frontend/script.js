async function uploadResume() {

    let file = document.getElementById("fileInput").files[0];
    if (!file) return alert("Upload file");

    let formData = new FormData();
    formData.append("file", file);

    let res = await fetch("http://127.0.0.1:8000/upload-resume", {
        method: "POST",
        body: formData
    });

    let data = await res.json();

    document.getElementById("result").innerHTML = `
        <p><b>Skills:</b> ${data.skills.join(", ")}</p>
        <p><b>Projects:</b></p>
        <ul>${data.projects.map(p => `<li>${p}</li>`).join("")}</ul>
    `;

    let score = Math.min(100, data.skills.length * 20);

    document.getElementById("scoreBar").style.width = score + "%";
    document.getElementById("scoreText").innerText = score + "%";
}


/* CHAT */
async function sendMessage() {

    let input = document.getElementById("userInput");
    let chatBox = document.getElementById("chatBox");

    let question = input.value;
    if (!question) return;

    chatBox.innerHTML += `<p><b>You:</b> ${question}</p>`;

    let res = await fetch("http://127.0.0.1:8000/ask-ai", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
    });

    let data = await res.json();

    chatBox.innerHTML += `<p><b>AI:</b> ${data.answer}</p>`;

    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;
}