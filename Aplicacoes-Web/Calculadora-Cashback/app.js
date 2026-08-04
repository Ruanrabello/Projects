const PRODUCTION_API_URL = "https://calculadora-cashback-csom.onrender.com";
const isLocalEnvironment = ["localhost", "127.0.0.1"].includes(window.location.hostname);
const API_URL = window.CASHBACK_API_URL
  || (isLocalEnvironment ? "http://127.0.0.1:8000" : PRODUCTION_API_URL);
const REQUEST_TIMEOUT_MS = 12000;

const form = document.getElementById("cashback-form");
const submitButton = document.getElementById("submit-button");
const result = document.getElementById("result");
const errorMessage = document.getElementById("error-message");
const historyList = document.getElementById("history-list");
const historyStatus = document.getElementById("history-status");

const currencyFormatter = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

async function requestJson(path, options = {}) {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(`${API_URL}${path}`, {
      ...options,
      signal: controller.signal,
    });

    const contentType = response.headers.get("content-type") || "";
    const data = contentType.includes("application/json")
      ? await response.json()
      : {};

    if (!response.ok) {
      throw new Error(data.detail || "Não foi possível concluir a operação.");
    }

    return data;
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error("A API demorou demais para responder.");
    }
    if (error instanceof TypeError) {
      throw new Error("Não foi possível conectar à API.");
    }
    throw error;
  } finally {
    window.clearTimeout(timeoutId);
  }
}

function clearFeedback() {
  result.textContent = "";
  errorMessage.textContent = "";
}

function setSubmitState(disabled) {
  submitButton.disabled = disabled;
  submitButton.textContent = disabled ? "Calculando..." : "Calcular cashback";
  submitButton.setAttribute("aria-busy", String(disabled));
}

function renderHistory(items) {
  historyList.replaceChildren();

  if (!items.length) {
    const emptyItem = document.createElement("li");
    emptyItem.className = "empty-state";
    emptyItem.textContent = "Nenhum cálculo registrado para este acesso.";
    historyList.appendChild(emptyItem);
    return;
  }

  items.forEach((item) => {
    const listItem = document.createElement("li");
    const description = document.createElement("strong");
    const value = document.createElement("span");

    description.textContent = `${item.tipo_cliente.toUpperCase()} · Compra ${currencyFormatter.format(item.valor_compra)}`;
    value.textContent = `Cashback ${currencyFormatter.format(item.valor_cashback)}`;

    listItem.append(description, value);
    historyList.appendChild(listItem);
  });
}

async function loadHistory() {
  historyStatus.textContent = "Atualizando...";

  try {
    const data = await requestJson("/historico");
    renderHistory(data.historico || []);
    historyStatus.textContent = "Últimos 10 cálculos";
  } catch (error) {
    renderHistory([]);
    historyStatus.textContent = "Histórico indisponível";
    console.error("Falha ao carregar histórico:", error);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearFeedback();
  setSubmitState(true);

  const payload = {
    tipo_cliente: document.getElementById("tipo").value,
    valor_compra: Number(document.getElementById("valor").value),
    cupom: Number(document.getElementById("cupom").value),
  };

  try {
    const data = await requestJson("/calcular-cashback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    result.textContent = `Valor final: ${currencyFormatter.format(data.valor_final)} · Cashback: ${currencyFormatter.format(data.cashback)}`;
    await loadHistory();
  } catch (error) {
    errorMessage.textContent = error.message;
  } finally {
    setSubmitState(false);
  }
});

loadHistory();
