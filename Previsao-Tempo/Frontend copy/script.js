const form = document.getElementById("weather-form");
const submitBtn = document.getElementById("submit-btn");
const cityInput = document.getElementById("cidade");
const loader = document.getElementById("loader");
const errorMessage = document.getElementById("error-message");
const errorText = document.getElementById("error-text");
const forecastPanel = document.getElementById("forecast-panel");
const weatherContainer = document.querySelector(".Weather-container");
const cityTitleHeader = document.getElementById("city-title-header");
const resetButton = document.getElementById("botao-reset");
const showAllButton = document.querySelector(".ver-tudo-btn");

const API_BASE_URL = window.WEATHER_API_URL || "http://localhost:8000";
const REQUEST_TIMEOUT_MS = 12000;

let cards = [];
let indiceAtual = 0;
let weatherData = null;

function validateCity(city) {
    const trimmedCity = city.trim();

    if (trimmedCity.length < 2 || trimmedCity.length > 50) {
        return {
            valid: false,
            message: "O nome da cidade deve ter entre 2 e 50 caracteres",
        };
    }

    if (!/^[a-zA-ZÀ-ÿ\s\-']+$/.test(trimmedCity)) {
        return {
            valid: false,
            message: "Use apenas letras, espaços, hífens e apóstrofos",
        };
    }

    return { valid: true, city: trimmedCity };
}

function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = "block";
    loader.style.display = "none";
}

function clearError() {
    errorMessage.style.display = "none";
    errorText.textContent = "";
}

function showLoader() {
    loader.style.display = "flex";
    clearError();
}

function setButtonState(disabled) {
    submitBtn.disabled = disabled;
    submitBtn.setAttribute("aria-busy", String(disabled));
}

function atualizarDots() {
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";

    cards.forEach((_, index) => {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.classList.add("dot");
        dot.setAttribute("aria-label", `Abrir detalhe ${index + 1}`);

        if (index === indiceAtual) {
            dot.classList.add("active");
            dot.setAttribute("aria-current", "true");
        }

        dot.addEventListener("click", () => {
            indiceAtual = index;
            renderizarCard();
        });

        pagination.appendChild(dot);
    });
}

function atualizarFundoPorCard(indice) {
    if (!weatherData) return;

    const backgrounds = {
        0: "img/world.jpg",
        2: "img/Cloud-sky.jpg",
        3: "img/water-drops.jpg",
        4: "img/Happy.jpg",
        5: "img/Windy-desert.jpg",
        6: "img/Pressure.jpg",
    };

    if (indice === 1) {
        if (weatherData.Temperatura >= 30) {
            forecastPanel.style.backgroundImage = "url('img/Hot-desert.jpg')";
        } else if (weatherData.Temperatura <= 15) {
            forecastPanel.style.backgroundImage = "url('img/snow.jpg')";
        } else {
            forecastPanel.style.backgroundImage = "url('img/Sunny-sky.jpg')";
        }
        return;
    }

    const image = backgrounds[indice] || "img/Default.jpg";
    forecastPanel.style.backgroundImage = `url('${image}')`;
}

function renderizarCard() {
    if (cards.length === 0) return;

    document.getElementById("card-title").textContent = cards[indiceAtual].titulo;
    document.getElementById("card-value").textContent = cards[indiceAtual].valor;

    atualizarDots();

    document.querySelectorAll(".option-btn").forEach((button) => {
        button.classList.remove("active");
        button.removeAttribute("aria-current");
    });

    const activeButton = document.querySelector(
        `.option-btn[data-index="${indiceAtual}"]`,
    );

    if (activeButton) {
        activeButton.classList.add("active");
        activeButton.setAttribute("aria-current", "true");
    }

    atualizarFundoPorCard(indiceAtual);
}

function buildCards(data) {
    return [
        { titulo: "🌍 Cidade e País", valor: `${data.Cidade}, ${data.País}` },
        { titulo: "🌡️ Temperatura", valor: `${Number(data.Temperatura).toFixed(1)} °C` },
        { titulo: "☁️ Descrição", valor: data.Descrição },
        { titulo: "💧 Umidade", valor: `${data.Umidade}%` },
        {
            titulo: "🤗 Sensação Térmica",
            valor: `${Number(data["Sensação Térmica"]).toFixed(1)} °C`,
        },
        {
            titulo: "💨 Velocidade do Vento",
            valor: `${Number(data["Velocidade do Vento"]).toFixed(2)} m/s`,
        },
        { titulo: "📈 Pressão", valor: `${data.Pressão} hPa` },
    ];
}

async function parseResponse(response) {
    const contentType = response.headers.get("content-type") || "";

    if (!contentType.includes("application/json")) {
        throw new Error("A API retornou uma resposta inválida");
    }

    return response.json();
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
    setButtonState(true);

    const controller = new AbortController();
    const timeoutId = window.setTimeout(
        () => controller.abort(),
        REQUEST_TIMEOUT_MS,
    );

    try {
        const response = await fetch(
            `${API_BASE_URL}/weather/${encodeURIComponent(validation.city)}`,
            { signal: controller.signal },
        );

        const data = await parseResponse(response);

        if (!response.ok) {
            throw new Error(data.detail || "Erro ao buscar previsão");
        }

        weatherData = data;
        cards = buildCards(data);
        indiceAtual = 0;

        loader.style.display = "none";
        clearError();
        forecastPanel.style.display = "flex";
        weatherContainer.classList.add("show-result");
        cityTitleHeader.textContent = data.Cidade;

        renderizarCard();
    } catch (error) {
        console.error("Erro ao consultar previsão:", error);

        if (error.name === "AbortError") {
            showError("A consulta demorou demais. Tente novamente.");
        } else if (error instanceof TypeError) {
            showError("Não foi possível conectar à API. Verifique se o backend está rodando.");
        } else {
            showError(error.message || "Erro ao buscar previsão do tempo");
        }
    } finally {
        window.clearTimeout(timeoutId);
        setButtonState(false);
    }
});

document.getElementById("next-btn").addEventListener("click", () => {
    if (cards.length === 0) return;
    indiceAtual = (indiceAtual + 1) % cards.length;
    renderizarCard();
});

document.getElementById("prev-btn").addEventListener("click", () => {
    if (cards.length === 0) return;
    indiceAtual = (indiceAtual - 1 + cards.length) % cards.length;
    renderizarCard();
});

document.querySelectorAll(".option-btn").forEach((button) => {
    button.addEventListener("click", () => {
        if (cards.length === 0) return;
        indiceAtual = Number(button.dataset.index);
        renderizarCard();
    });
});

if (showAllButton) {
    showAllButton.addEventListener("click", () => {
        if (cards.length === 0) return;

        const summary = cards
            .map((card) => `${card.titulo}: ${card.valor}`)
            .join("\n");

        window.alert(summary);
    });
}

resetButton.addEventListener("click", () => {
    cityInput.value = "";
    cards = [];
    weatherData = null;
    indiceAtual = 0;

    forecastPanel.style.display = "none";
    forecastPanel.style.backgroundImage = "";
    weatherContainer.classList.remove("show-result");
    cityTitleHeader.textContent = "---";
    clearError();
    loader.style.display = "none";
    cityInput.focus();
});
