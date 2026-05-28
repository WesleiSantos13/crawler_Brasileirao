const BASE_URL = ''; // Caminho relativo, pois está junto com o Flask
let tabelaAtual = ''; // Lembra qual tabela está aberta

// 1. Função para carregar as tabelas completas
async function carregarDados(endpoint) {
    tabelaAtual = endpoint; 
    const conteudo = document.getElementById('conteudo');
    const titulo = document.getElementById('titulo-pagina');
    
    const ano = document.getElementById('input-ano').value; 

    let url = `${BASE_URL}/${endpoint}`;
    let textoTitulo = endpoint;

    if (ano) {
        url = `${BASE_URL}/${endpoint}/ano/${ano}`;
        textoTitulo = `${endpoint} de ${ano}`; 
    }
    
    titulo.innerText = textoTitulo;

    // ---  (Salva a altura da tabela atual) ---
    const alturaAtual = conteudo.offsetHeight;
    if (alturaAtual > 50) {
        conteudo.style.minHeight = `${alturaAtual}px`;
    }

    conteudo.innerHTML = '<p style="text-align: center; color: #666; padding: 20px;">Carregando dados...</p>';

    try {
        const resposta = await fetch(url);
        let dados = await resposta.json();

        if (dados.length === 0) {
            conteudo.innerHTML = `<p style="text-align: center; color: #666;">Nenhum dado encontrado para ${textoTitulo}.</p>`;
            conteudo.style.minHeight = 'auto'; // Libera a altura se não houver dados
            return;
        }

        // Verifica se a tabela é de confrontos para traduzir os IDs
        if (endpoint.includes('confrontos')) {
            try {
                const resTimes = await fetch(`${BASE_URL}/times`);
                const times = await resTimes.json();

                const mapaTimes = {};
                times.forEach(t => {
                    mapaTimes[t.id] = t.nome;
                });

                dados = dados.map(jogo => {
                    const jogoFormatado = { ...jogo };
                    
                    if ('mandante_id' in jogoFormatado) {
                        jogoFormatado['Mandante'] = mapaTimes[jogoFormatado.mandante_id] || "Desconhecido";
                        delete jogoFormatado.mandante_id; 
                    }
                    if ('visitante_id' in jogoFormatado) {
                        jogoFormatado['Visitante'] = mapaTimes[jogoFormatado.visitante_id] || "Desconhecido";
                        delete jogoFormatado.visitante_id; 
                    }
                    
                    return jogoFormatado;
                });
            } catch (erroTimes) {
                console.error("Erro ao buscar os times para converter os IDs:", erroTimes);
            }
        }

        conteudo.innerHTML = gerarTabela(dados);
    } catch (erro) {
        console.error("Erro na tabela:", erro);
        conteudo.innerHTML = `<p style="color: red; text-align: center;">Erro ao carregar os dados.</p>`;
    } finally {
        // --- LIBERA A ALTURA (Permite que a nova tabela defina o tamanho da página) ---
        conteudo.style.minHeight = 'auto';
    }
}

// 2. Busca os "Top 1" HISTÓRICOS (Recordes Gerais)
async function carregarTopEstatisticas() {
    document.getElementById('titulo-estatisticas').innerText = "🏆 Estatisticas do Brasileirão";
    document.getElementById('label-campeao').innerText = "👑 Maior Pontuador";
    document.getElementById('input-ano').value = ""; 

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
    
    if (tabelaAtual !== '') {
        carregarDados(tabelaAtual);
    }
}

// 3. Busca as estatísticas de UM ANO ESPECÍFICO
async function atualizarPorAno() {
    const ano = document.getElementById('input-ano').value;
    
    if (!ano) {
        alert("Por favor, digite um ano válido.");
        return;
    }

    document.getElementById('titulo-estatisticas').innerText = `📊 Estatísticas do Ano de ${ano}`;
    document.getElementById('label-campeao').innerText = "👑 Campeão do Ano";

    colocarCardsEmModoCarregando();

    try {
        const resClass = await fetch(`${BASE_URL}/classificacao/ano/${ano}`);
        const dadosClass = await resClass.json();
        if(dadosClass.length > 0) {
            document.getElementById('card-campeao').innerText = `${dadosClass[0].time} (${dadosClass[0].pontos} pts)`;
        } else { document.getElementById('card-campeao').innerText = "Sem dados"; }

        const resArt = await fetch(`${BASE_URL}/artilharia/ano/${ano}`);
        const dadosArt = await resArt.json();
        if(dadosArt.length > 0) {
            dadosArt.sort((a, b) => b.gols - a.gols); 
            document.getElementById('card-artilheiro').innerText = `${dadosArt[0].jogador} (${dadosArt[0].gols} gols)`; 
        } else { document.getElementById('card-artilheiro').innerText = "Sem dados"; }

        const resAss = await fetch(`${BASE_URL}/assistencias/ano/${ano}`);
        const dadosAss = await resAss.json();
        if(dadosAss.length > 0) {
            dadosAss.sort((a, b) => b.assistencias - a.assistencias);
            document.getElementById('card-assistencia').innerText = `${dadosAss[0].jogador} (${dadosAss[0].assistencias} ass)`;
        } else { document.getElementById('card-assistencia').innerText = "Sem dados"; }

        const resHat = await fetch(`${BASE_URL}/hattricks/ano/${ano}`);
        const dadosHat = await resHat.json();
        if(dadosHat.length > 0) {
            document.getElementById('card-hattrick').innerText = dadosHat[0].jogador;
        } else { document.getElementById('card-hattrick').innerText = "Nenhum no ano"; }

    } catch (erro) {
        console.error("Erro ao buscar dados do ano:", erro);
        alert("Erro ao processar dados. O ano pode não existir no banco.");
    }
    
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

window.onload = () => {
    carregarTopEstatisticas();
};