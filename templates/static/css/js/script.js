function calculateIMC(event) {
    event.preventDefault(); // Impede o envio do formulário

    const peso = parseFloat(document.getElementById('peso').value);
    const altura = parseFloat(document.getElementById('altura').value) / 100; // converter cm para metros

    if (!isNaN(peso) && !isNaN(altura) && altura > 0) {
        const imc = peso / (altura * altura);
        document.getElementById('imcResult').textContent = `Seu IMC é ${imc.toFixed(2)}`;
    } else {
        document.getElementById('imcResult').textContent = 'Por favor, insira valores válidos.';
    }
}
