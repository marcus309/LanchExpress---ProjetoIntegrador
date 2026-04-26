package com.lanchexpress.service;

import com.lanchexpress.exception.RecursoNaoEncontradoException;
import com.lanchexpress.exception.RegraNegocioException;
import com.lanchexpress.model.Cliente;
import com.lanchexpress.repository.ClienteRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ClienteService {

    private final ClienteRepository clienteRepository;

    public ClienteService(ClienteRepository clienteRepository) {
        this.clienteRepository = clienteRepository;
    }

    public List<Cliente> listarTodos() {
        return clienteRepository.findAll();
    }

    public Cliente buscarPorId(Long id) {
        return clienteRepository.findById(id)
                .orElseThrow(() -> new RecursoNaoEncontradoException(
                        "Cliente não encontrado com id: " + id));
    }

    public Cliente cadastrar(Cliente cliente) {
        if (clienteRepository.existsByEmail(cliente.getEmail())) {
            throw new RegraNegocioException("E-mail já cadastrado: " + cliente.getEmail());
        }
        cliente.setId(null);
        return clienteRepository.save(cliente);
    }

    public Cliente atualizar(Long id, Cliente dados) {
        Cliente cliente = buscarPorId(id);
        cliente.setNome(dados.getNome());
        cliente.setInstituicao(dados.getInstituicao());
        if (dados.getSenha() != null && !dados.getSenha().isBlank()) {
            cliente.setSenha(dados.getSenha());
        }
        return clienteRepository.save(cliente);
    }

    public void deletar(Long id) {
        Cliente cliente = buscarPorId(id);
        clienteRepository.delete(cliente);
    }

    public Cliente autenticar(String email, String senha) {
        Cliente cliente = clienteRepository.findByEmail(email)
                .orElseThrow(() -> new RegraNegocioException("E-mail ou senha inválidos."));
        if (!cliente.getSenha().equals(senha)) {
            throw new RegraNegocioException("E-mail ou senha inválidos.");
        }
        return cliente;
    }
}
