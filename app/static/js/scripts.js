function selectPlan(plan) {
    // Exibir o container do switch
    document.getElementById('switch-container').classList.remove('d-none');
    
    // Simular vereditos dos testes (aqui você pode fazer uma chamada AJAX para o backend)
    const verdicts = {
        'plano1': ['pass', 'fail', 'pass', 'fail'],
        'plano2': ['pass', 'pass', 'fail', 'pass'],
        'plano3': ['fail', 'fail', 'pass', 'pass']
    };

    const selectedVerdicts = verdicts[plan];

    // Atualizar os conectores com os vereditos dos testes
    for (let i = 1; i <= 4; i++) {
        const connector = document.getElementById('connector' + i);
        connector.className = 'connector ' + selectedVerdicts[i - 1];
    }
}
