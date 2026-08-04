const form = document.getElementById("weather-form");
const submitButton = document.getElementById("submit-btn");
const cityInput = document.getElementById("cidade");
const loader = document.getElementById("loader");
const errorMessage = document.getElementById("error-message");
const errorText = document.getElementById("error-text");
const forecastPanel = document.getElementById("forecast-panel");
const weatherContainer = document.querySelector(".weather-container");
const cityTitle = document.getElementById("city-title-header");
const resetButton = document.getElementById("botao-reset");
const showAllButton = document.getElementById("show-all-btn");
const dialog = document.getElementById("all-weather-dialog");
const closeDialogButton = document.getElementById("close-dialog-btn");
const summaryList = document.getElementById("all-weather-list");

const isLocalDevelopment = ["localhost", "127.0.0.1"].includes(
    window.location.hostname,
);
const API_BASE_URL = window.WEATHER_API_URL
    || (isLocalDevelopment ? "http://localhost:8000" : "");
const REQUEST_TIMEOUT_MS = 12000;

let cards = [];
let currentIndex = 0;
let weatherData = null;

function validateCity(city) {
    const normalizedCity = city.trim();

    if (normalizedCity.length < 2 || normalizedCity.length > 50) {
        return {
            valid: false,
            message: "O nome da cidade deve ter entre 2 e 50 caracteres.",
        };
    }

    if (!/^[a-zA-ZÀ-ÿ\s\-']+$/.test(normalizedCity)) {
        return {
            valid: false,
            message: "Use apenas letras, espaços, hífens e apóstrofos.",
        };
    }

    return { valid: true, city: normalizedCity };
}

function setHidden(element, hidden) {
    element.hidden = hidden;
}

function showError(message) {
    errorText.textContent = message;
    setHidden(errorMessage, false);
    setHidden(loader, true);
}

function clearError() {
    errorText.textContent = "";
    setHidden(errorMessage, true);
}

function showLoader() {
    clearError();
    setHidden(loader, false);
}

function setSubmitState(disabled) {
    submitButton.disabled = disabled;
    submitButton.setAttribute("aria-busy", String(disabled));
}

function createCards(data) {
    const temperature = Number(data.Temperatura);
    const feelsLike = Number(data["Sensação Térmica"]);
    const windSpeed = Number(data["Velocidade do Vento"]);

    if (![temperature, feelsLike, windSpeed].every(Number.isFinite)) {
        throw new Error("A API retornou dados meteorológicos inválidos.");
    }

    return [
        { title: "🌍 Cidade e país", value: `${data.Cidade}, ${data.País}` },
        { title: "🌡️ Temperatura", value: `${temperature.toFixed(1)} °C` },
        { title: "☁️ Descrição", value: data.Descrição },
        { title: "💧 Umidade", value: `${data.Umidade}%` },
        { title: "🤗 Sensação térmica", value: `${feelsLike.toFixed(1)} °C` },
        { title: "💨 Velocidade do vento", value: `${windSpeed.toFixed(2)} m/s` },
        { title: "📈 Pressão", value: `${data.Pressão} hPa` },
    ];
}

function getBackgroundImage(index) {
    const defaultBackgrounds = {
        0: "linear-gradient(135deg, #14b8a6 0%, #0f172a 100%)",
        3: "linear-gradient(135deg, #38bdf8 0%, #1d4ed8 100%)",
        4: "linear-gradient(135deg, #fb923c 0%, #c2410c 100%)",
        5: "linear-gradient(135deg, #67e8f9 0%, #0369a1 100%)",
        6: "linear-gradient(135deg, #a78bfa 0%, #4c1d95 100%)",
    };

    if (index === 1) {
        if (Number(weatherData.Temperatura) >= 30) {
            return "linear-gradient(135deg, #f97316 0%, #991b1b 100%)";
        }
        if (Number(weatherData.Temperatura) <= 15) {
            return "linear-gradient(135deg, #bae6fd 0%, #2563eb 100%)";
        }
        return "linear-gradient(135deg, #facc15 0%, #0284c7 100%)";
    }

    if (index === 2) {
        const description = String(weatherData.Descrição || "").toLowerCase();
        return description.includes("chuva") || description.includes("garoa")
            ? "linear-gradient(135deg, #475569 0%, #0f172a 100%)"
            : "linear-gradient(135deg, #94a3b8 0%, #334155 100%)";
    }

    return defaultBackgrounds[index]
        || "linear-gradient(135deg, #0f766e 0%, #0f172a 100%)";
}

function updatePagination() {
    const pagination = document.getElementById("pagination");
    pagination.replaceChildren();

    cards.forEach((_, index) => {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = "dot";
        dot.setAttribute("aria-label", `Abrir detalhe ${index + 1} de ${cards.length}`);

        if (index === currentIndex) {
            dot.classList.add("active");
            dot.setAttribute("aria-current", "true");
        }

        dot.addEventListener("click", () => {
            currentIndex = index;
            renderCard();
        });

        pagination.appendChild(dot);
    });
}

function renderCard() {
    if (cards.length === 0 || !weatherData) return;

    const currentCard = cards[currentIndex];
    document.getElementById("card-title").textContent = currentCard.title;
    document.getElementById("card-value").textContent = currentCard.value;

    document.querySelectorAll(".option-btn").forEach((button) => {
        const isActive = Number(button.dataset.index) === currentIndex;
        button.classList.toggle("active", isActive);

        if (isActive) {
            button.setAttribute("aria-current", "true");
        } else {
            button.removeAttribute("aria-current");
        }
    });

    forecastPanel.style.backgroundImage = getBackgroundImage(currentIndex);
    updatePagination();
}

async function parseJsonResponse(response) {
    const contentType = response.headers.get("content-type") || "";

    if (!contentType.includes("application/json")) {
        throw new Error("A API retornou uma resposta em formato inesperado.");
    }

    return response.json();
}

async function fetchWeather(city) {
    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

    try {
        const response = await fetch(
            `${API_BASE_URL}/weather/${encodeURIComponent(city)}`,
            { signal: controller.signal },
        );
        const data = await parseJsonResponse(response);

        if (!response.ok) {
            throw new Error(data.detail || "Não foi possível consultar a previsão.");
        }

        return data;
    } finally {
        window.clearTimeout(timeoutId);
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const validation = validateCity(cityInput.value);
    if (!validation.valid) {
        showError(validation.message);
        cityInput.focus();
        return;
    }

    showLoader();
    setSubmitState(true);

    try {
        const data = await fetchWeather(validation.city);
        const nextCards = createCards(data);

        weatherData = data;
        cards = nextCards;
        currentIndex = 0;

        setHidden(loader, true);
        clearError();
        setHidden(forecastPanel, false);
        weatherContainer.classList.add("show-result");
        cityTitle.textContent = data.Cidade;
        renderCard();
    } catch (error) {
        console.error("Erro ao consultar previsão:", error);

        if (error.name === "AbortError") {
            showError("A consulta demorou demais. Tente novamente.");
        } else if (error instanceof TypeError) {
            showError("Não foi possível conectar à API. Verifique se o back-end está disponível.");
        } else {
            showError(error.message || "Erro ao buscar previsão do tempo.");
        }
    } finally {
        setSubmitState(false);
    }
});

document.getElementById("next-btn").addEventListener("click", () => {
    if (cards.length === 0) return;
    currentIndex = (currentIndex + 1) % cards.length;
    renderCard();
});

document.getElementById("prev-btn").addEventListener("click", () => {
    if (cards.length === 0) return;
    currentIndex = (currentIndex - 1 + cards.length) % cards.length;
    renderCard();
});

document.querySelectorAll(".option-btn").forEach((button) => {
    button.addEventListener("click", () => {
        if (cards.length === 0) return;
        currentIndex = Number(button.dataset.index);
        renderCard();
    });
});

showAllButton.addEventListener("click", () => {
    if (cards.length === 0) return;

    summaryList.replaceChildren();
    cards.forEach((card) => {
        const item = document.createElement("div");
        const term = document.createElement("dt");
        const description = document.createElement("dd");

        term.textContent = card.title;
        description.textContent = card.value;
        item.append(term, description);
        summaryList.appendChild(item);
    });

    if (typeof dialog.showModal === "function") {
        dialog.showModal();
    } else {
        dialog.setAttribute("open", "");
    }
});

function closeDialog() {
    if (typeof dialog.close === "function") {
        dialog.close();
    } else {
        dialog.removeAttribute("open");
    }
}

closeDialogButton.addEventListener("click", closeDialog);
dialog.addEventListener("click", (event) => {
    if (event.target === dialog) closeDialog();
});

resetButton.addEventListener("click", () => {
    cityInput.value = "";
    cards = [];
    weatherData = null;
    currentIndex = 0;

    setHidden(forecastPanel, true);
    forecastPanel.style.backgroundImage = "";
    weatherContainer.classList.remove("show-result");
    cityTitle.textContent = "---";
    clearError();
    setHidden(loader, true);
    closeDialog();
    cityInput.focus();
});
