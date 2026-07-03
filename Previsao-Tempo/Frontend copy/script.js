const form = document.getElementById("weather-form");
const submitBtn = document.getElementById("submit-btn");
const cityInput = document.getElementById("cidade");
const loader = document.getElementById("loader");
const errorMessage = document.getElementById("error-message");
const errorText = document.getElementById("error-text");

let cards = [];
let indiceAtual = 0;
let weatherData = null;

function validateCity(city) {
    const trimmedCity = city.trim();

    if (trimmedCity.length < 2 || trimmedCity.length > 50) {
        return { valid: false, message: "O nome da cidade deve ter entre 2 e 50 caracteres" };
    }
    if (!/^[a-zA-ZÀ-ÿ\s\-]+$/.test(trimmedCity)) {
        return { valid: false, message: "Use apenas letras, hífens e espaços no nome da cidade" };
    }
    return { valid: true };
}

function renderizarCard() {
    if(cards.length === 0) return;

    document.getElementById("card-title").textContent =
        cards[indiceAtual].titulo;

    document.getElementById("card-value").textContent =
        cards[indiceAtual].valor;

    atualizarDots();

    document
        .querySelectorAll(".option-btn")
        .forEach(btn => btn.classList.remove("active"));

    const botaoAtivo =
        document.querySelector(
            `.option-btn[data-index="${indiceAtual}"]`
        );

    if (botaoAtivo) {
        botaoAtivo.classList.add("active");
    }

    atualizarFundoPorCard(indiceAtual);
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
    errorMessage.style.display = "none";
}

function setButtonState(disabled) {
    submitBtn.disabled = disabled;
}

function atualizarDots(){
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";

    cards.forEach((_, index)=>{
        const dot = document.createElement("div");
        dot.classList.add("dot");
        if(index === indiceAtual){
            dot.classList.add("active");
        }
        pagination.appendChild(dot);
    });
}

function atualizarFundoPorCard(indice){

    if(!weatherData) return;

    const painel = document.getElementById("forecast-panel");

    switch(indice){

        case 0:
            painel.style.backgroundImage =
                "url('img/world.jpg')";
            break;

        case 1:

            if(weatherData.Temperatura >= 30){

                painel.style.backgroundImage =
                    "url('img/Hot-desert.jpg')";

            } else if(weatherData.Temperatura <= 15){

                painel.style.backgroundImage =
                    "url('img/snow.jpg')";

            } else {

                painel.style.backgroundImage =
                    "url('img/Sunny-sky.jpg')";
            }

            break;

        case 2:
            painel.style.backgroundImage =
                "url('img/Cloud-sky.jpg')";
            break;

        case 3:
            painel.style.backgroundImage =
                "url('img/water-drops.jpg')";
            break;

        case 4:
            painel.style.backgroundImage =
                "url('img/Happy.jpg')";
            break;

        case 5:
            painel.style.backgroundImage =
                "url('img/Windy-desert.jpg')";
            break;

        case 6:
            painel.style.backgroundImage =
                "url('img/Pressure.jpg')";
            break;
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const city = cityInput.value;

    const validation = validateCity(city);
    if (!validation.valid) {
        showError(validation.message);
        return;
    }

    clearError();
    showLoader();
    setButtonState(true);

    try {
        const response = await fetch(
            `http://localhost:8000/weather/${encodeURIComponent(city)}`
        );
        const data = await response.json();
        weatherData = data;

        if (!response.ok) {
            throw new Error(data.detail || "Erro ao buscar previsão");
        }

        loader.style.display = "none";
        clearError();
        document.getElementById("forecast-panel").style.display = "flex"; // ← adiciona isso
        document.querySelector(".Weather-container").classList.add("show-result");


        // Atualiza dinamicamente o título do cabeçalho da direita com a cidade retornada
        document.getElementById("city-title-header").textContent = `${data.Cidade}`;

        cards = [
            { titulo: "🌍 Cidade e País", valor: `${data.Cidade}, ${data.País}` },
            { titulo: "🌡️ Temperatura", valor: `${data.Temperatura.toFixed(1)} °C` },
            { titulo: "☁️ Descrição", valor: data.Descrição },
            { titulo: "💧 Umidade", valor: `${data.Umidade}%` },
            { titulo: "🤗 Sensação Térmica", valor: `${data["Sensação Térmica"].toFixed(1)} °C` },
            { titulo: "💨 Velocidade do Vento", valor: `${data["Velocidade do Vento"].toFixed(2)} m/s` },
            { titulo: "📈 Pressão", valor: `${data.Pressão} hPa` }
        ];

        indiceAtual = 0;
        renderizarCard();

    } catch (error) {
        let errorMsg = "Erro ao buscar previsão do tempo";
        if (error.name === "AbortError") {
            errorMsg = "Requisição expirou. Tente novamente";
        } else if (error.message.includes("Failed to fetch")) {
            errorMsg = "Erro de conexão. Verifique se a API do Python está rodando";
        } else if (error.message) {
            errorMsg = error.message;
        }
        console.error("Erro:", error);
        showError(errorMsg);
    } finally {
        setButtonState(false);
    }
});

document.getElementById("next-btn").addEventListener("click", ()=>{
    if(cards.length === 0) return;
    indiceAtual++;
    if(indiceAtual >= cards.length) indiceAtual = 0;
    renderizarCard();
});

document.getElementById("prev-btn").addEventListener("click", ()=>{
    if(cards.length === 0) return;
    indiceAtual--;
    if(indiceAtual < 0) indiceAtual = cards.length - 1;
    renderizarCard();
});

// Adiciona o evento de clique para os botões da barra de atalhos
document.querySelectorAll(".option-btn").forEach(botao => {

    botao.addEventListener("click", () => {

        if(cards.length === 0) return;

        indiceAtual = parseInt(
            botao.getAttribute("data-index")
        );

        renderizarCard();
    });

});

document.getElementById("botao-reset")
.addEventListener("click", () => {

    cityInput.value = "";

    cards = [];
    weatherData = null;
    indiceAtual = 0;

    document.getElementById("forecast-panel")
        .style.display = "none";

    document.getElementById("forecast-panel")
        .style.backgroundImage = "";

    document.querySelector(".Weather-container")
        .classList.remove("show-result");


});
