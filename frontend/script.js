const URL_BASE = "http://127.0.0.1:5004/";
const ENDPOINT_CHARADAS = "charadas/random";
let respostaCharada = "";  // Definição única

// Obtém a referência ao elemento HTML onde a pergunta da charada será exibida
let pergunta = document.querySelector("#pergunta");

async function buscarCharada() {
    try {
        const resposta = await fetch(URL_BASE + ENDPOINT_CHARADAS);
        const dadosCharada = await resposta.json();

        // Atualiza o conteúdo do elemento HTML com a pergunta da charada
        pergunta.innerHTML = `"${dadosCharada.pergunta}"`;

        // Garante que a resposta seja uma única palavra
        respostaCharada = dadosCharada.resposta.split(" ")[0].toLowerCase();  
        console.log("Resposta esperada:", respostaCharada);
    } catch (erro) {
        console.log("Erro ao buscar charada:", erro);
    }
}

document.querySelector(".btn-charada").addEventListener("click", buscarCharada);

document.addEventListener("DOMContentLoaded", function () {
    const inputResposta = document.querySelector("input");
    const btnResposta = document.querySelector(".btn-resposta");

    function verificarResposta() {
        let respostaUsuario = inputResposta.value.trim().toLowerCase();

        if (!respostaCharada) {
            alert("Erro: resposta da charada não carregada.");
            return;
        }

        if (respostaUsuario === respostaCharada) {
            alert("Parabéns! Você acertou! 🥳");
        } else {
            alert(`Ops! Não foi dessa vez. A resposta correta era: ${respostaCharada} 🙁`);
        }

        inputResposta.value = "";
    }

    btnResposta.addEventListener("click", verificarResposta);
    inputResposta.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            verificarResposta();
        }
    });

    buscarCharada();
});
