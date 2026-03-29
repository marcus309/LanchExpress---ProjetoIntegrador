
let carrinho = JSON.parse(localStorage.getItem('lanchexpress_cart')) || [];


const catalogo = [
  { id: 1, nome: "Coxinha Crocante", preco: 6.50 },
  { id: 2, nome: "Hamburgão Assado", preco: 8.00 },
  { id: 3, nome: "Refrigerante Lata", preco: 5.00 },
  { id: 4, nome: "Pudim de Leite", preco: 8.00 },
  { id: 5, nome: "Esfiha de Carne", preco: 5.50 },
  { id: 6, nome: "Suco Natural", preco: 7.00 },
  { id: 7, nome: "Risólis de Queijo", preco: 6.00 },
  { id: 8, nome: "Brownie de Chocolate", preco: 7.50 },
  { id: 9, nome: "Bala de Morango", preco: 0.50 }
];



function adicionarAoCarrinho(idProduto) {
  const produto = catalogo.find(p => p.id === idProduto);
  if (produto) {
    const itemExistente = carrinho.find(item => item.id === idProduto);
    if (itemExistente) {
      itemExistente.quantidade += 1;
    } else {
      carrinho.push({ ...produto, quantidade: 1 });
    }
    salvarCarrinho();
    if(typeof showPremiumAlert !== 'undefined'){ showPremiumAlert(`${produto.nome} adicionado ao carrinho!`); } else { alert(`${produto.nome} adicionado ao carrinho!`); }
  }
}

function salvarCarrinho() {
  localStorage.setItem('lanchexpress_cart', JSON.stringify(carrinho));
}

function limparCarrinho() {
  carrinho = [];
  salvarCarrinho();
}


function alterarQuantidade(idProduto, delta) {
  const item = carrinho.find(item => item.id === idProduto);
  if (item) {
    item.quantidade += delta;
    if (item.quantidade <= 0) {
      carrinho = carrinho.filter(i => i.id !== idProduto);
    }
    salvarCarrinho();
    renderizarCarrinho();
  }
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
    let itemTotal = item.preco * item.quantidade;
    total += itemTotal;

    const emojis = { 1: '🍗', 2: '🍔', 3: '🧃', 4: '🍮', 5: '🥟', 6: '🍹', 7: '🥟', 8: '🍫', 9: '🍬'};
    const emoji = emojis[item.id] || '🍽️';

    const div = document.createElement('div');
    div.className = 'cart-item';
    div.innerHTML = `
      <div class="cart-item-img">${emoji}</div>
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


function gerarCodigo() {
  const codeDisplay = document.getElementById('codigoRetirada');
  if (!codeDisplay) return;


  if(carrinho.length > 0) {
    limparCarrinho();
  }

  const letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const num = Math.floor(1000 + Math.random() * 9000);
  const prefixo = letras.charAt(Math.floor(Math.random() * letras.length)) +
                  letras.charAt(Math.floor(Math.random() * letras.length)) +
                  letras.charAt(Math.floor(Math.random() * letras.length));
  
  codeDisplay.innerText = `${prefixo}-${num}`;
}


document.addEventListener('DOMContentLoaded', () => {
  renderizarCarrinho();
  gerarCodigo();
});


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
      if(callback) callback();
    }, 300);
  }, 2500);
}
