package com.lanchexpress.service;

import com.lanchexpress.exception.RecursoNaoEncontradoException;
import com.lanchexpress.model.Produto;
import com.lanchexpress.repository.ProdutoRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ProdutoService {

    private final ProdutoRepository produtoRepository;

    public ProdutoService(ProdutoRepository produtoRepository) {
        this.produtoRepository = produtoRepository;
    }

    public List<Produto> listarTodos() {
        return produtoRepository.findAll();
    }

    public List<Produto> listarDisponiveis() {
        return produtoRepository.findByDisponivelTrue();
    }

    public List<Produto> listarPorCategoria(String categoria) {
        return produtoRepository.findByCategoriaIgnoreCase(categoria);
    }

    public List<Produto> buscarPorNome(String nome) {
        return produtoRepository.findByNomeContainingIgnoreCase(nome);
    }

    public Produto buscarPorId(Long id) {
        return produtoRepository.findById(id)
                .orElseThrow(() -> new RecursoNaoEncontradoException(
                        "Produto não encontrado com id: " + id));
    }

    public Produto criar(Produto produto) {
        produto.setId(null);
        if (produto.getDisponivel() == null) {
            produto.setDisponivel(true);
        }
        return produtoRepository.save(produto);
    }

    public Produto atualizar(Long id, Produto dados) {
        Produto produto = buscarPorId(id);
        produto.setNome(dados.getNome());
        produto.setDescricao(dados.getDescricao());
        produto.setPreco(dados.getPreco());
        produto.setCategoria(dados.getCategoria());
        produto.setEmoji(dados.getEmoji());
        if (dados.getDisponivel() != null) {
            produto.setDisponivel(dados.getDisponivel());
        }
        return produtoRepository.save(produto);
    }

    public void deletar(Long id) {
        Produto produto = buscarPorId(id);
        produtoRepository.delete(produto);
    }
}
