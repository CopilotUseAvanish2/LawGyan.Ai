const form = document.querySelector("#chat-form");
const input = document.querySelector("#message-input");
const messages = document.querySelector("#messages");
const welcome = document.querySelector("#welcome");
const typing = document.querySelector("#typing");
const sendButton = document.querySelector("#send-button");

function addUserMessage(text) {
  const row = document.createElement("article");
  row.className = "message user";
  const body = document.createElement("div");
  body.className = "message-body";
  const content = document.createElement("div");
  content.className = "message-text";
  content.textContent = text;
  body.append(content);
  row.append(body);
  messages.append(row);
}

function addAssistantMessage(data) {
  const row = document.createElement("article");
  row.className = "message assistant";
  const avatar = document.createElement("span");
  avatar.className = "message-avatar";
  avatar.setAttribute("aria-hidden", "true");
  avatar.textContent = "LG";
  const body = document.createElement("div");
  body.className = "message-body";

  const label = document.createElement("div");
  label.className = "intent-label";
  label.textContent = "GENERAL INFORMATION · " + data.title;
  const heading = document.createElement("h2");
  heading.className = "assistant-heading";
  heading.textContent = data.title;
  const summary = document.createElement("p");
  summary.className = "response-summary";
  summary.textContent = data.summary;
  body.append(label, heading, summary);

  const stepsSection = document.createElement("section");
  stepsSection.className = "response-section";
  const stepsTitle = document.createElement("h3");
  stepsTitle.textContent = "Possible next steps";
  const steps = document.createElement("ol");
  data.steps.forEach((step) => {
    const item = document.createElement("li");
    item.textContent = step;
    steps.append(item);
  });
  stepsSection.append(stepsTitle, steps);
  body.append(stepsSection);

  const avoid = document.createElement("div");
  avoid.className = "avoid-note";
  avoid.textContent = "Avoid: " + data.avoid;
  body.append(avoid);

  data.resources.forEach((resource) => {
    const link = document.createElement("a");
    link.className = "resource-link";
    link.href = resource.url;
    link.target = "_blank";
    link.rel = "noreferrer";
    link.textContent = resource.label + " ↗";
    body.append(link);
  });

  const caveat = document.createElement("p");
  caveat.className = "response-caveat";
  caveat.textContent = "This is general information, not legal advice. Laws and procedures can vary by state and facts. For urgent or case-specific help, contact a qualified lawyer or legal aid service.";
  body.append(caveat);
  row.append(avatar, body);
  messages.append(row);
}

function showError(message) {
  addAssistantMessage({
    title: "I couldn't process that just now",
    summary: message,
    steps: ["Please try again in a moment."],
    avoid: "Do not rely on an incomplete response for a legal deadline or emergency.",
    resources: [{ label: "Find legal aid through NALSA", url: "https://nalsa.gov.in/" }],
  });
}

async function sendMessage(text) {
  welcome.classList.add("hidden");
  addUserMessage(text);
  typing.classList.remove("hidden");
  sendButton.disabled = true;
  input.disabled = true;
  try {
    const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]").value;
    const response = await fetch("/api/chat/", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
      body: JSON.stringify({ message: text }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "The request could not be completed.");
    addAssistantMessage(data);
  } catch (error) {
    showError(error.message || "Please check your connection and try again.");
  } finally {
    typing.classList.add("hidden");
    sendButton.disabled = false;
    input.disabled = false;
    input.focus();
    window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text || sendButton.disabled) return;
  input.value = "";
  input.style.height = "auto";
  sendMessage(text);
});

input.addEventListener("input", () => {
  input.style.height = "auto";
  input.style.height = `${Math.min(input.scrollHeight, 120)}px`;
});

input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

document.querySelectorAll("[data-prompt]").forEach((button) => {
  button.addEventListener("click", () => {
    input.value = button.dataset.prompt;
    form.requestSubmit();
  });
});

function resetChat() {
  messages.replaceChildren();
  welcome.classList.remove("hidden");
  input.value = "";
  input.focus();
}

document.querySelector("#new-chat").addEventListener("click", resetChat);
document.querySelector("#clear-chat").addEventListener("click", resetChat);