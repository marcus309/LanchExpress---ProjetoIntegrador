package com.lanchexpress.config;

import com.lanchexpress.model.Cliente;
import com.lanchexpress.model.Produto;
import com.lanchexpress.repository.ClienteRepository;
import com.lanchexpress.repository.ProdutoRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.math.BigDecimal;
import java.util.List;

@Configuration
public class DataLoader {

    @Bean
    CommandLineRunner carregarDadosIniciais(ProdutoRepository produtoRepository,
                                            ClienteRepository clienteRepository) {
        return args -> {
            if (produtoRepository.count() == 0) {
                produtoRepository.saveAll(List.of(
                        new Produto("Coxinha Crocante", "Recheio frango c/ catupiry",
                                new BigDecimal("6.50"), "salgados", "🍗"),
                        new Produto("Hamburgão Assado", "Massa macia com queijo e presunto",
                                new BigDecimal("8.00"), "salgados", "🍔"),
                        new Produto("Refrigerante Lata", "Natural ou Limão 350ml geladinho",
                                new BigDecimal("5.00"), "bebidas", "🧃"),
                        new Produto("Pudim de Leite", "Com calda de caramelo artesanal",
                                new BigDecimal("8.00"), "sobremesas", "🍮"),
                        new Produto("Esfiha de Carne", "Tradicional com carne temperada",
                                new BigDecimal("5.50"), "salgados", "🥟"),
                        new Produto("Suco Natural", "Laranja, limão ou maracujá (400ml)",
                                new BigDecimal("7.00"), "bebidas", "🍹"),
                        new Produto("Risólis de Queijo", "Massa crocante com muito queijo derretido",
                                new BigDecimal("6.00"), "salgados", "🥟"),
                        new Produto("Brownie de Chocolate", "Massa úmida com gotas de chocolate",
                                new BigDecimal("7.50"), "sobremesas", "🍫"),
                        new Produto("Bala de Morango", "Bala tradicional recheada (unidade)",
                                new BigDecimal("0.50"), "sobremesas", "🍬")
                ));
                System.out.println("✅ DataLoader: 9 produtos cadastrados.");
            }

            if (clienteRepository.count() == 0) {
                clienteRepository.save(new Cliente(
                        "Aluno Demo", "demo@senac.br", "123456", "Senac São Paulo"));
                System.out.println("✅ DataLoader: cliente demo cadastrado (demo@senac.br / 123456).");
            }
        };
    }
}
