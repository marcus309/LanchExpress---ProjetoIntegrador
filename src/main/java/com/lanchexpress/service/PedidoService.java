package com.lanchexpress.service;

import com.lanchexpress.dto.ItemPedidoRequest;
import com.lanchexpress.dto.PedidoRequest;
import com.lanchexpress.exception.RecursoNaoEncontradoException;
import com.lanchexpress.exception.RegraNegocioException;
import com.lanchexpress.model.Cliente;
import com.lanchexpress.model.ItemPedido;
import com.lanchexpress.model.Pedido;
import com.lanchexpress.model.Pedido.StatusPedido;
import com.lanchexpress.model.Produto;
import com.lanchexpress.repository.ClienteRepository;
import com.lanchexpress.repository.PedidoRepository;
import com.lanchexpress.repository.ProdutoRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Random;

@Service
public class PedidoService {

    private static final String LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    private final Random random = new Random();

    private final PedidoRepository pedidoRepository;
    private final ProdutoRepository produtoRepository;
    private final ClienteRepository clienteRepository;

    public PedidoService(PedidoRepository pedidoRepository,
                         ProdutoRepository produtoRepository,
                         ClienteRepository clienteRepository) {
        this.pedidoRepository = pedidoRepository;
        this.produtoRepository = produtoRepository;
        this.clienteRepository = clienteRepository;
    }

    public List<Pedido> listarTodos() {
        return pedidoRepository.findAll();
    }

    public Pedido buscarPorId(Long id) {
        return pedidoRepository.findById(id)
                .orElseThrow(() -> new RecursoNaoEncontradoException(
                        "Pedido não encontrado com id: " + id));
    }

    public Pedido buscarPorCodigo(String codigo) {
        return pedidoRepository.findByCodigoRetirada(codigo)
                .orElseThrow(() -> new RecursoNaoEncontradoException(
                        "Pedido não encontrado com código: " + codigo));
    }

    public List<Pedido> listarPorCliente(Long clienteId) {
        return pedidoRepository.findByClienteIdOrderByDataCriacaoDesc(clienteId);
    }

    @Transactional
    public Pedido criar(PedidoRequest request) {
        if (request.getItens() == null || request.getItens().isEmpty()) {
            throw new RegraNegocioException("O pedido deve conter ao menos um item.");
        }

        Pedido pedido = new Pedido();

        if (request.getClienteId() != null) {
            Cliente cliente = clienteRepository.findById(request.getClienteId())
                    .orElseThrow(() -> new RecursoNaoEncontradoException(
                            "Cliente não encontrado com id: " + request.getClienteId()));
            pedido.setCliente(cliente);
        }

        for (ItemPedidoRequest itemReq : request.getItens()) {
            if (itemReq.getQuantidade() == null || itemReq.getQuantidade() <= 0) {
                throw new RegraNegocioException("Quantidade inválida para o produto " + itemReq.getProdutoId());
            }
            Produto produto = produtoRepository.findById(itemReq.getProdutoId())
                    .orElseThrow(() -> new RecursoNaoEncontradoException(
                            "Produto não encontrado com id: " + itemReq.getProdutoId()));
            if (Boolean.FALSE.equals(produto.getDisponivel())) {
                throw new RegraNegocioException("Produto indisponível: " + produto.getNome());
            }
            if (produto.getQuantidadeEstoque() != null
                    && produto.getQuantidadeEstoque() < itemReq.getQuantidade()) {
                throw new RegraNegocioException(
                        "Estoque insuficiente para " + produto.getNome()
                                + " (disponível: " + produto.getQuantidadeEstoque() + ").");
            }
            if (produto.getQuantidadeEstoque() != null) {
                produto.setQuantidadeEstoque(produto.getQuantidadeEstoque() - itemReq.getQuantidade());
                produtoRepository.save(produto);
            }
            pedido.adicionarItem(new ItemPedido(produto, itemReq.getQuantidade()));
        }

        pedido.setCodigoRetirada(gerarCodigoUnico());
        pedido.calcularTotal();
        return pedidoRepository.save(pedido);
    }

    @Transactional
    public Pedido atualizarStatus(Long id, StatusPedido novoStatus) {
        Pedido pedido = buscarPorId(id);
        pedido.setStatus(novoStatus);
        return pedidoRepository.save(pedido);
    }

    @Transactional
    public void cancelar(Long id) {
        Pedido pedido = buscarPorId(id);
        if (pedido.getStatus() == StatusPedido.RETIRADO) {
            throw new RegraNegocioException("Não é possível cancelar um pedido já retirado.");
        }
        pedido.setStatus(StatusPedido.CANCELADO);
        pedidoRepository.save(pedido);
    }

    @Transactional
    public void deletar(Long id) {
        Pedido pedido = buscarPorId(id);
        pedidoRepository.delete(pedido);
    }

    @Transactional
    public Pedido avaliar(Long id, Integer nota, String comentario) {
        if (nota == null || nota < 1 || nota > 5) {
            throw new RegraNegocioException("A nota deve estar entre 1 e 5.");
        }
        Pedido pedido = buscarPorId(id);
        pedido.setAvaliacao(nota);
        pedido.setComentarioAvaliacao(comentario);
        return pedidoRepository.save(pedido);
    }

    private String gerarCodigoUnico() {
        String codigo;
        int tentativas = 0;
        do {
            String prefixo = "" + LETRAS.charAt(random.nextInt(LETRAS.length()))
                    + LETRAS.charAt(random.nextInt(LETRAS.length()))
                    + LETRAS.charAt(random.nextInt(LETRAS.length()));
            int numero = 1000 + random.nextInt(9000);
            codigo = prefixo + "-" + numero;
            tentativas++;
            if (tentativas > 20) {
                throw new RegraNegocioException("Não foi possível gerar um código de retirada único.");
            }
        } while (pedidoRepository.existsByCodigoRetirada(codigo));
        return codigo;
    }
}
