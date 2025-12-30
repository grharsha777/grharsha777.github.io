const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const chatbox = document.querySelector(".chatbox");
const chatbotToggler = document.querySelector(".chatbot-toggler");
const chatbotCloseBtn = document.querySelector(".close-btn");

let userMessage = null; // Variable to store user's message

// Harsha's Portfolio Knowledge Base
const knowledgeBase = {
    "projects": "I've built several agentic systems including the **Gemini DevOps Copilot**, **Mentara AI**, and **Code Vortex**. Which one would you like to know more about?",
    "about": "I'm G R Harsha, an AI Engineer specializing in **Agentic Systems** and **DevOps Automation**. I look beyond simple chatbots to build autonomous systems that reason and act.",
    "contact": "You can reach me at **grharsha128@gmail.com** or connect with me on LinkedIn. I'm open to internships and collaborations! Scroll down to the Contact section?",
    "skills": "My tech stack includes **Python, FastAPI, LangChain, AutoGen, Docker, and Kubernetes**. I focus on production-grade AI engineering.",
    "gemini": "**Gemini DevOps Copilot** is an AI assistant that automates CI/CD configs and incident response using the Gemini API. It's designed to reduce toil for DevOps teams.",
    "mentara": "**Mentara AI** is a mental wellness platform combining full-stack development with LLMs to provide supportive conversations.",
    "code vortex": "**Code Vortex** is a suite of developer tools designed to automate documentation and code review processes.",
    "experience": "I'm currently a B.Tech CSE (AI) student at NIAT & Yenepoya University. I've also been a Mentor at **GSSoC** and a Campus Ambassador.",
    "agentic": "My 'Agentic' approach means I build systems that use **ReAct loops** (Reasoning + Acting). My agents don't just talk; they use tools, query databases, and execute workflows.",
    "default": "I can tell you about my **projects**, **skills**, **experience**, or how to **contact** Harsha. What would you like to know?"
};

const suggestions = [
    "Show best project",
    "Explain tech stack",
    "Share résumé",
    "Contact info"
];

const createChatLi = (message, className) => {
    // Create a chat <li> element with passed message and className
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", className);
    let chatContent = className === "outgoing" ? `<p></p>` : `<img src="images/harsha_avatar.jpg" alt="AI"><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").textContent = message;
    return chatLi;
}

// Add Suggestion Chips to Chat Interface
const renderSuggestions = () => {
    const suggestionsContainer = document.createElement("div");
    suggestionsContainer.classList.add("chat-suggestions");

    suggestions.forEach(text => {
        const chip = document.createElement("button");
        chip.classList.add("suggestion-chip");
        chip.textContent = text;
        chip.addEventListener("click", () => {
            chatInput.value = text;
            handleChat();
        });
        suggestionsContainer.appendChild(chip);
    });

    // Insert before chatbox (or inside specific container if preferred)
    // For this design, we put it above the input area
    const chatInputArea = document.querySelector(".chat-input");
    chatInputArea.parentNode.insertBefore(suggestionsContainer, chatInputArea);
}

const generateResponse = async (userMsg) => {
    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userMsg })
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();
        return data.response;
    } catch (error) {
        console.error("Error connecting to Chatbot API:", error);
        return "I'm having trouble connecting to my brain (Backend Server). Please ensure the Python server is running at http://localhost:8000.";
    }
}

const handleChat = async () => {
    userMessage = chatInput.value.trim();
    if (!userMessage) return;

    chatInput.value = "";
    chatInput.style.height = "auto";
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);

    // Show waiting animation
    const incomingChatLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(incomingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);

    try {
        const responseText = await generateResponse(userMessage);
        const messageElement = incomingChatLi.querySelector("p");
        // Simple markdown parsing for bold
        messageElement.innerHTML = responseText.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
    } catch (err) {
        incomingChatLi.querySelector("p").textContent = "Sorry, something went wrong.";
    }
    chatbox.scrollTo(0, chatbox.scrollHeight);
}

// Initialize
renderSuggestions();

chatInput.addEventListener("input", () => {
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    // If Enter key is pressed without Shift key and the window 
    // width is greater than 800px, handle the chat
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

sendChatBtn.addEventListener("click", handleChat);
chatbotCloseBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));
