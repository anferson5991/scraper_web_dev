const { ipcRenderer } = require('electron');

const urlInput = document.getElementById('url-input');
const scrapeButton = document.getElementById('scrape-button');
const resultLabel = document.getElementById('result-label');

scrapeButton.addEventListener('click', () => {
    const urlBase = urlInput.value;
    if (urlBase) {
        // Enviar um evento para o backend para iniciar o scraping
        ipcRenderer.send('start-scraping', { urlBase });
        resultLabel.innerText = 'Coletando e salvando dados... Aguarde!';
    } else {
        alert('Por favor, insira a URL base do APP na PlayStore.');
    }
});

// Evento de resposta do backend
ipcRenderer.on('scraping-result', (event, result) => {
    if (result.success) {
        resultLabel.innerText = 'Dados coletados e salvos com sucesso!';
        // Aqui você pode adicionar lógica para exibir os resultados do scraping na interface.
    } else {
        resultLabel.innerText = 'Ocorreu um erro ao coletar/salvar dados.';
    }
});
