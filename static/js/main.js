const BASE_URL = ''; // Caminho relativo, pois está junto com o Flask

// 1. Função para carregar as tabelas completas quando clicar nos botões azuis
async function carregarDados(endpoint) {
    const conteudo = document.getElementById('conteudo');
    const titulo = document.getElementById('titulo-pagina');
    
    titulo.innerText = endpoint;
    conteudo.innerHTML = '<p>Carregando dados...</p>';

    try {
        const resposta = await fetch(`${BASE_URL}/${endpoint}`);
        const dados = await resposta.json();

        if (dados.length === 0) {
            conteudo.innerHTML = '<p>Nenhum dado encontrado.</p>';
            return;
        }
        conteudo.innerHTML = gerarTabela(dados);
    } catch (erro) {
        console.error("Erro na tabela:", erro);
        conteudo.innerHTML = `<p style="color: red;">Erro ao carregar os dados.</p>`;
    }
}

// 2. NOVA FUNÇÃO: Busca os "Top 1" das suas rotas e coloca nos 4 painéis
async function carregarTopEstatisticas() {
    try {
        // 👑 MAIOR PONTUADOR (Pega o 1º da rota /classificacao/top)
        const resClassificacao = await fetch(`${BASE_URL}/classificacao/top?top=1`);
        const dadosClass = await resClassificacao.json();
        if(dadosClass.length > 0) {
            document.getElementById('card-campeao').innerText = `${dadosClass[0].time} (${dadosClass[0].pontos} pts)`;
        }

        // ⚽ MAIOR ARTILHEIRO (Pega o 1º da rota /artilharia/top)
        const resArtilharia = await fetch(`${BASE_URL}/artilharia/top?top=1`);
        const dadosArt = await resArtilharia.json();
        if(dadosArt.length > 0) {
            document.getElementById('card-artilheiro').innerText = `${dadosArt[0].jogador} (${dadosArt[0].gols} gols)`; 
        }

        // 👟 LÍDER DE ASSISTÊNCIAS (Pega o 1º da rota /assistencias/top)
        const resAssistencia = await fetch(`${BASE_URL}/assistencias/top?top=1`);
        const dadosAss = await resAssistencia.json();
        if(dadosAss.length > 0) {
            document.getElementById('card-assistencia').innerText = `${dadosAss[0].jogador} (${dadosAss[0].assistencias} ass)`;
        }

        // 🔥 REI DO HAT-TRICK (Como não há rota /top, o JS calcula o jogador que mais repete)
        const resHattrick = await fetch(`${BASE_URL}/hattricks`);
        const dadosHat = await resHattrick.json();
        if(dadosHat.length > 0) {
            const contagem = {};
            let maiorJogador = "";
            let maxHattricks = 0;
            
            // Conta quantas vezes cada jogador aparece na lista
            dadosHat.forEach(h => {
                contagem[h.jogador] = (contagem[h.jogador] || 0) + 1;
                if (contagem[h.jogador] > maxHattricks) {
                    maxHattricks = contagem[h.jogador];
                    maiorJogador = h.jogador;
                }
            });
            document.getElementById('card-hattrick').innerText = `${maiorJogador} (${maxHattricks}x)`;
        }

    } catch (erro) {
        console.error("Erro ao buscar o TOP estatísticas:", erro);
    }
}

// 3. Função auxiliar para desenhar a tabela HTML
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