const BASE_URL = ''; // Caminho relativo, pois está junto com o Flask
let tabelaAtual = ''; // Lembra qual tabela está aberta

// 1. Função para carregar as tabelas completas
async function carregarDados(endpoint) {
    tabelaAtual = endpoint; // Salva a tabela atual na memória
    const conteudo = document.getElementById('conteudo');
    const titulo = document.getElementById('titulo-pagina');
    
    // Pega o ano que está digitado no campo de texto (se houver)
    const ano = document.getElementById('input-ano').value; 

    // Define a URL base e o título padrão
    let url = `${BASE_URL}/${endpoint}`;
    let textoTitulo = endpoint;

    // Se o usuário digitou um ano, ajustamos a URL para a rota de filtro
    if (ano) {
        url = `${BASE_URL}/${endpoint}/ano/${ano}`;
        textoTitulo = `${endpoint} de ${ano}`; // Ex: "artilharia de 2023"
    }
    
    titulo.innerText = textoTitulo;
    conteudo.innerHTML = '<p>Carregando dados...</p>';

    try {
        const resposta = await fetch(url);
        const dados = await resposta.json();

        if (dados.length === 0) {
            conteudo.innerHTML = `<p>Nenhum dado encontrado para ${textoTitulo}.</p>`;
            return;
        }
        conteudo.innerHTML = gerarTabela(dados);
    } catch (erro) {
        console.error("Erro na tabela:", erro);
        conteudo.innerHTML = `<p style="color: red;">Erro ao carregar os dados.</p>`;
    }
}

// 2. Busca os "Top 1" HISTÓRICOS (Recordes Gerais)
async function carregarTopEstatisticas() {
    document.getElementById('titulo-estatisticas').innerText = "🏆 Recordes Históricos do Brasileirão";
    document.getElementById('label-campeao').innerText = "👑 Maior Pontuador";
    document.getElementById('input-ano').value = ""; // Limpa o campo do ano

    colocarCardsEmModoCarregando();

    try {
        const resClassificacao = await fetch(`${BASE_URL}/classificacao/top?top=1`);
        const dadosClass = await resClassificacao.json();
        if(dadosClass.length > 0) document.getElementById('card-campeao').innerText = `${dadosClass[0].time} (${dadosClass[0].pontos} pts)`;

        const resArtilharia = await fetch(`${BASE_URL}/artilharia/top?top=1`);
        const dadosArt = await resArtilharia.json();
        if(dadosArt.length > 0) document.getElementById('card-artilheiro').innerText = `${dadosArt[0].jogador} (${dadosArt[0].gols} gols)`; 

        const resAssistencia = await fetch(`${BASE_URL}/assistencias/top?top=1`);
        const dadosAss = await resAssistencia.json();
        if(dadosAss.length > 0) document.getElementById('card-assistencia').innerText = `${dadosAss[0].jogador} (${dadosAss[0].assistencias} ass)`;

        const resHattrick = await fetch(`${BASE_URL}/hattricks`);
        const dadosHat = await resHattrick.json();
        if(dadosHat.length > 0) {
            const contagem = {}; let maiorJogador = ""; let maxHattricks = 0;
            dadosHat.forEach(h => {
                contagem[h.jogador] = (contagem[h.jogador] || 0) + 1;
                if (contagem[h.jogador] > maxHattricks) { maxHattricks = contagem[h.jogador]; maiorJogador = h.jogador; }
            });
            document.getElementById('card-hattrick').innerText = `${maiorJogador} (${maxHattricks}x)`;
        }
    } catch (erro) {
        console.error("Erro ao buscar o TOP estatísticas:", erro);
    }
    //Se tiver alguma tabela aberta, atualiza
    if (tabelaAtual !== '') {
        carregarDados(tabelaAtual);
    }
}

// 3.  Busca as estatísticas de UM ANO ESPECÍFICO
async function atualizarPorAno() {
    const ano = document.getElementById('input-ano').value;
    
    if (!ano) {
        alert("Por favor, digite um ano válido.");
        return;
    }

    // Muda os títulos para fazer sentido com a busca anual
    document.getElementById('titulo-estatisticas').innerText = `📊 Estatísticas do Ano de ${ano}`;
    document.getElementById('label-campeao').innerText = "👑 Campeão do Ano";

    colocarCardsEmModoCarregando();

    try {
        // CAMPEÃO (Pega o 1º da classificação daquele ano)
        const resClass = await fetch(`${BASE_URL}/classificacao/ano/${ano}`);
        const dadosClass = await resClass.json();
        if(dadosClass.length > 0) {
            document.getElementById('card-campeao').innerText = `${dadosClass[0].time} (${dadosClass[0].pontos} pts)`;
        } else { document.getElementById('card-campeao').innerText = "Sem dados"; }

        // ARTILHEIRO (Pega o 1º da artilharia daquele ano)
        const resArt = await fetch(`${BASE_URL}/artilharia/ano/${ano}`);
        const dadosArt = await resArt.json();
        if(dadosArt.length > 0) {
            dadosArt.sort((a, b) => b.gols - a.gols); // Garante que o maior venha primeiro
            document.getElementById('card-artilheiro').innerText = `${dadosArt[0].jogador} (${dadosArt[0].gols} gols)`; 
        } else { document.getElementById('card-artilheiro').innerText = "Sem dados"; }

        // ASSISTÊNCIAS (Pega o 1º das assistências daquele ano)
        const resAss = await fetch(`${BASE_URL}/assistencias/ano/${ano}`);
        const dadosAss = await resAss.json();
        if(dadosAss.length > 0) {
            dadosAss.sort((a, b) => b.assistencias - a.assistencias);
            document.getElementById('card-assistencia').innerText = `${dadosAss[0].jogador} (${dadosAss[0].assistencias} ass)`;
        } else { document.getElementById('card-assistencia').innerText = "Sem dados"; }

        // HAT-TRICKS (Pega o 1º destaque de hat-tricks daquele ano)
        const resHat = await fetch(`${BASE_URL}/hattricks/ano/${ano}`);
        const dadosHat = await resHat.json();
        if(dadosHat.length > 0) {
            document.getElementById('card-hattrick').innerText = dadosHat[0].jogador;
        } else { document.getElementById('card-hattrick').innerText = "Nenhum no ano"; }

    } catch (erro) {
        console.error("Erro ao buscar dados do ano:", erro);
        alert("Erro ao processar dados. O ano pode não existir no banco.");
    }
    // Se tiver alguma tabela aberta, atualiza ela também
    if (tabelaAtual !== '') {
        carregarDados(tabelaAtual);
    }
}

// 4. Função auxiliar: Muda o texto dos cards para "Carregando..."
function colocarCardsEmModoCarregando() {
    document.getElementById('card-campeao').innerText = "Buscando...";
    document.getElementById('card-artilheiro').innerText = "Buscando...";
    document.getElementById('card-assistencia').innerText = "Buscando...";
    document.getElementById('card-hattrick').innerText = "Buscando...";
}

// 5. Função auxiliar para desenhar a tabela HTML
function gerarTabela(arrayDeObjetos) {
    const colunas = Object.keys(arrayDeObjetos[0]);
    let tabelaHTML = '<table><thead><tr>';
    colunas.forEach(coluna => { tabelaHTML += `<th>${coluna}</th>`; });
    tabelaHTML += '</tr></thead><tbody>';
    arrayDeObjetos.forEach(linha => {
        tabelaHTML += '<tr>';
        colunas.forEach(coluna => { tabelaHTML += `<td>${linha[coluna]}</td>`; });
        tabelaHTML += '</tr>';
    });
    tabelaHTML += '</tbody></table>';
    return tabelaHTML;
}

// Dispara o carregamento dos painéis TOP automaticamente quando a página abrir
window.onload = () => {
    carregarTopEstatisticas();
};