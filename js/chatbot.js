const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const chatbox = document.querySelector(".chatbox");
const chatbotToggler = document.querySelector(".chatbot-toggler");
const chatbotCloseBtn = document.querySelector(".close-btn");

let userMessage = null; // Variable to store user's message

// Harsha's Portfolio Knowledge Base
const knowledgeBase = {
    "projects": "I've built several agentic systems including the <a href='https://github.com/grharsha777/Gemini-DevOps-Copilot' target='_blank'>Gemini DevOps Copilot</a>, <a href='https://github.com/grharsha777/MentaraAI' target='_blank'>Mentara AI</a>, and <a href='https://github.com/grharsha777/Code-Vortex' target='_blank'>Code Vortex</a>. Which one would you like to know more about?",
    "about": "I'm G R Harsha, an AI Engineer specializing in **Agentic Systems** and **DevOps Automation**. I look beyond simple chatbots to build autonomous systems that reason and act.",
    "contact": "You can reach me at <a href='mailto:grharsha128@gmail.com'>grharsha128@gmail.com</a> or connect with me on <a href='https://www.linkedin.com/in/grharsha777/' target='_blank'>LinkedIn</a>. I'm open to internships and collaborations!",
    "skills": "My tech stack includes **Python, FastAPI, LangChain, AutoGen, Docker, and Kubernetes**. I focus on production-grade AI engineering.",
    "gemini": "**Gemini DevOps Copilot** is an AI assistant that automates CI/CD configs and incident response. View it on <a href='https://github.com/grharsha777/Gemini-DevOps-Copilot' target='_blank'>GitHub</a>.",
    "mentara": "**Mentara AI** is a mental wellness platform combining full-stack development with LLMs. Check the <a href='https://github.com/grharsha777/MentaraAI' target='_blank'>Repo</a>.",
    "code vortex": "**Code Vortex** is a suite of developer tools for automated documentation. See more on <a href='https://github.com/grharsha777/Code-Vortex' target='_blank'>GitHub</a>.",
    "experience": "I'm a B.Tech CSE (AI) student. I've been a Mentor at **GSSoC** and a Campus Ambassador. View my <a href='https://drive.google.com/file/d/1BnObISeyCMV9UTi9V_qIKWJitsyrycq1/view' target='_blank'>Full Résumé</a>.",
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
            body: JSON.stringify({ message: userMsg }),
            signal: AbortSignal.timeout(5000) // Timeout after 5s
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();
        return data.response;
    } catch (error) {
        console.warn("Backend unreachable, falling back to local Knowledge Base:", error);
        return getFallbackResponse(userMsg);
    }
}

// Intelligent Client-Side Fallback Matcher
const getFallbackResponse = (query) => {
    const lowerQuery = query.toLowerCase();

    // 1. Keyword Mapping
    const keywords = {
        "project": "projects",
        "work": "projects",
        "repo": "projects",
        "about": "about",
        "who are you": "about",
        "identity": "about",
        "contact": "contact",
        "email": "contact",
        "reach": "contact",
        "skill": "skills",
        "tech": "skills",
        "stack": "skills",
        "experience": "experience",
        "study": "experience",
        "education": "experience",
        "gemini": "gemini",
        "devops": "gemini",
        "mentara": "mentara",
        "vortex": "code vortex",
        "agentic": "agentic",
        "reasoning": "agentic"
    };

    // 2. Find Match
    for (const [key, category] of Object.entries(keywords)) {
        if (lowerQuery.includes(key)) {
            return knowledgeBase[category] || knowledgeBase["default"];
        }
    }

    return knowledgeBase["default"];
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
