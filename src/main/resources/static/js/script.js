/* ==========================================================
   LanchExpress - Camada de integração com a API REST (Fase 3)
   Backend: Spring Boot — base /api
   ========================================================== */

const API_BASE = '/api';

const ApiService = {
  async _request(url, options = {}) {
    const opts = {
      headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
      ...options
    };
    const resp = await fetch(`${API_BASE}${url}`, opts);
    if (!resp.ok) {
      let mensagem = `Erro ${resp.status}`;
      try {
        const corpo = await resp.json();
        mensagem = corpo.mensagem || mensagem;
      } catch (_) { /* corpo vazio */ }
      throw new Error(mensagem);
    }
    if (resp.status === 204) return null;
    return resp.json();
  },

  // Produtos
  listarProdutos(categoria) {
    const qs = categoria && categoria !== 'todos' ? `?categoria=${encodeURIComponent(categoria)}` : '';
    return this._request(`/produtos${qs}`);
  },
  buscarProdutosPorNome(nome) {
    return this._request(`/produtos?nome=${encodeURIComponent(nome)}`);
  },

  // Clientes
  cadastrarCliente(dados) {
    return this._request('/clientes', { method: 'POST', body: JSON.stringify(dados) });
  },
  login(email, senha) {
    return this._request('/clientes/login', { method: 'POST', body: JSON.stringify({ email, senha }) });
  },
  buscarCliente(id) {
    return this._request(`/clientes/${id}`);
  },
  atualizarCliente(id, dados) {
    return this._request(`/clientes/${id}`, { method: 'PUT', body: JSON.stringify(dados) });
  },
  deletarCliente(id) {
    return this._request(`/clientes/${id}`, { method: 'DELETE' });
  },

  // Pedidos
  criarPedido(pedido) {
    return this._request('/pedidos', { method: 'POST', body: JSON.stringify(pedido) });
  },
  buscarPedido(id) {
    return this._request(`/pedidos/${id}`);
  },
  listarPedidosCliente(clienteId) {
    return this._request(`/pedidos?clienteId=${clienteId}`);
  },
  avaliarPedido(id, nota, comentario) {
    return this._request(`/pedidos/${id}/avaliar`, {
      method: 'POST',
      body: JSON.stringify({ nota, comentario })
    });
  }
};

/* ==========================================================
   Helpers globais
   ========================================================== */
const StatusLabel = {
  AGUARDANDO_PAGAMENTO: 'Aguardando pagamento',
  PAGO: 'Pago',
  EM_PREPARO: 'Em preparo',
  PRONTO: 'Pronto p/ retirada',
  RETIRADO: 'Retirado',
  CANCELADO: 'Cancelado'
};

function formatarMoeda(valor) {
  return 'R$ ' + Number(valor).toFixed(2).replace('.', ',');
}

function formatarData(iso) {
  const d = new Date(iso);
  return d.toLocaleDateString('pt-BR') + ' às ' + d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
}

/* ==========================================================
   Bottom Navigation Bar (injeta automaticamente)
   Para usar: <body data-bottom-nav="cardapio|historico|sobre|contato|perfil">
   ========================================================== */
function injetarBottomNav(ativo) {
  if (document.querySelector('.bottom-nav')) return;
  const nav = document.createElement('nav');
  nav.className = 'bottom-nav';
  const itens = [
    { key: 'cardapio',  href: 'produtos.html',  icon: '🍔', label: 'Cardápio' },
    { key: 'historico', href: 'historico.html', icon: '📋', label: 'Pedidos' },
    { key: 'sobre',     href: 'sobre.html',     icon: 'ℹ️', label: 'Sobre' },
    { key: 'contato',   href: 'contato.html',   icon: '✉️', label: 'Contato' },
    { key: 'perfil',    href: 'perfil.html',    icon: '👤', label: 'Perfil' }
  ];
  itens.forEach(it => {
    const a = document.createElement('a');
    a.className = 'bottom-nav-item' + (it.key === ativo ? ' active' : '');
    a.href = it.href;
    a.innerHTML = `<span class="nav-icon">${it.icon}</span><span>${it.label}</span>`;
    nav.appendChild(a);
  });
  document.body.appendChild(nav);
  document.querySelectorAll('.content').forEach(c => c.classList.add('has-bottom-nav'));
}

/* ==========================================================
   Favoritos (localStorage)
   ========================================================== */
const Favoritos = {
  _key: 'lanchexpress_favoritos',
  todos() { return JSON.parse(localStorage.getItem(this._key)) || []; },
  is(id) { return this.todos().includes(id); },
  toggle(id) {
    const lista = this.todos();
    const idx = lista.indexOf(id);
    if (idx >= 0) lista.splice(idx, 1); else lista.push(id);
    localStorage.setItem(this._key, JSON.stringify(lista));
    return idx < 0;
  }
};

/* ==========================================================
   Carrinho local (sincroniza com o backend só na finalização)
   ========================================================== */
let carrinho = JSON.parse(localStorage.getItem('lanchexpress_cart')) || [];

function salvarCarrinho() {
  localStorage.setItem('lanchexpress_cart', JSON.stringify(carrinho));
}

function limparCarrinho() {
  carrinho = [];
  salvarCarrinho();
}

function adicionarAoCarrinho(produto) {
  if (!produto || !produto.id) return;
  const itemExistente = carrinho.find(i => i.id === produto.id);
  if (itemExistente) {
    itemExistente.quantidade += 1;
  } else {
    carrinho.push({
      id: produto.id,
      nome: produto.nome,
      preco: Number(produto.preco),
      emoji: produto.emoji || '🍽️',
      quantidade: 1
    });
  }
  salvarCarrinho();
  if (typeof showPremiumAlert !== 'undefined') {
    showPremiumAlert(`${produto.nome} adicionado ao carrinho!`);
  }
}

function alterarQuantidade(idProduto, delta) {
  const item = carrinho.find(i => i.id === idProduto);
  if (!item) return;
  item.quantidade += delta;
  if (item.quantidade <= 0) {
    carrinho = carrinho.filter(i => i.id !== idProduto);
  }
  salvarCarrinho();
  renderizarCarrinho();
}

function renderizarCarrinho() {
  const cartList = document.getElementById('cartList');
  const cartTotalText = document.getElementById('cartTotalText');
  const emptyMsg = document.getElementById('emptyMsg');
  const bottomBar = document.getElementById('checkoutBottomBar');

  if (!cartList) return;

  if (carrinho.length === 0) {
    if (emptyMsg) emptyMsg.style.display = 'block';
    cartList.innerHTML = '';
    if (bottomBar) bottomBar.style.display = 'none';
    return;
  }

  if (emptyMsg) emptyMsg.style.display = 'none';
  if (bottomBar) bottomBar.style.display = 'flex';

  cartList.innerHTML = '';
  let total = 0;

  carrinho.forEach(item => {
    total += item.preco * item.quantidade;
    const div = document.createElement('div');
    div.className = 'cart-item';
    div.innerHTML = `
      <div class="cart-item-img">${item.emoji || '🍽️'}</div>
      <div class="cart-item-details">
        <h4>${item.nome}</h4>
        <span class="price">R$ ${item.preco.toFixed(2).replace('.', ',')}</span>
      </div>
      <div class="cart-qtd-controls">
        <button class="qtd-btn" onclick="alterarQuantidade(${item.id}, -1)">-</button>
        <span class="qtd-value">${item.quantidade}</span>
        <button class="qtd-btn" onclick="alterarQuantidade(${item.id}, 1)">+</button>
      </div>
    `;
    cartList.appendChild(div);
  });

  if (cartTotalText) {
    cartTotalText.innerHTML = `R$ ${total.toFixed(2).replace('.', ',')}`;
  }
}

/* ==========================================================
   Alerta visual
   ========================================================== */
function showPremiumAlert(message, type = 'success', callback = null) {
  const alertBox = document.createElement('div');
  alertBox.className = `premium-alert alert-${type}`;
  alertBox.innerHTML = `
    <div class="alert-icon">${type === 'success' ? '✅' : '⚠️'}</div>
    <div class="alert-msg">${message}</div>
  `;
  document.body.appendChild(alertBox);

  setTimeout(() => alertBox.classList.add('show'), 100);
  setTimeout(() => {
    alertBox.classList.remove('show');
    setTimeout(() => {
      alertBox.remove();
      if (callback) callback();
    }, 300);
  }, 2500);
}

/* ==========================================================
   Inicialização padrão (telas que apenas exibem o carrinho)
   A retirada.html cria o pedido por conta própria — não disparamos aqui.
   ========================================================== */
document.addEventListener('DOMContentLoaded', () => {
  renderizarCarrinho();
});
