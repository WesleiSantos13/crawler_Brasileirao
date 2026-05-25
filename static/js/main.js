// Remova a URL fixa. Deixando vazio ou apenas '/' significa que ele vai buscar no próprio servidor
const BASE_URL = ''; 

async function carregarDados(endpoint) {
    const conteudo = document.getElementById('conteudo');
    const titulo = document.getElementById('titulo-pagina');
    
    titulo.innerText = endpoint;
    conteudo.innerHTML = '<p>Carregando dados...</p>';

    try {
        // Agora a requisição será feita para /artilharia, /confrontos, etc. no próprio domínio
        const resposta = await fetch(`${BASE_URL}/${endpoint}`);
        
        if (!resposta.ok) {
            throw new Error('Erro ao buscar dados na API');
        }

        const dados = await resposta.json();

        if (dados.length === 0) {
            conteudo.innerHTML = '<p>Nenhum dado encontrado.</p>';
            return;
        }

        conteudo.innerHTML = gerarTabela(dados);

    } catch (erro) {
        console.error(erro);
        conteudo.innerHTML = `<p style="color: red;">Erro ao carregar os dados. Verifique o console do navegador.</p>`;
    }
}

// A função gerarTabela(arrayDeObjetos) continua exatamente igual à anterior...
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