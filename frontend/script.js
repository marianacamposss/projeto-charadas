const URL_BASE = "http://127.0.0.1:5000/";
const ENDPOINT_CHARADAS = "charadas";
let respostaCharada = "";  // Variável global para armazenar a resposta da charada

document.addEventListener("DOMContentLoaded", function () {
    const pergunta = document.querySelector("#pergunta");
    const inputResposta = document.querySelector("input");
    const btnResposta = document.querySelector(".btn-resposta");
    const btnCharada = document.querySelector(".btn-charada");

    async function buscarCharada() {
        try {
            const resposta = await fetch(URL_BASE + ENDPOINT_CHARADAS);
            const dadosCharada = await resposta.json();

            pergunta.innerHTML = `"${dadosCharada.pergunta}"`;

            // Pega apenas a primeira palavra da resposta e transforma em minúscula
            respostaCharada = dadosCharada.resposta.split(" ")[0].toLowerCase();  
            console.log("Resposta esperada:", respostaCharada);
        } catch (erro) {
            console.log("Erro ao buscar charada:", erro);
        }
    }

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

    // Adiciona os eventos depois que o DOM está carregado
    btnResposta.addEventListener("click", verificarResposta);
    btnCharada.addEventListener("click", buscarCharada);
    inputResposta.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            verificarResposta();
        }
    });

    // Busca uma charada inicial ao carregar a página
    buscarCharada();
});
