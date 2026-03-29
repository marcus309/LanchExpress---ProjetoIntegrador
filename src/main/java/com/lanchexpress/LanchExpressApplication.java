package com.lanchexpress;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class LanchExpressApplication {

    public static void main(String[] args) {
        System.out.println("🚀 Iniciando o LanchExpress Servidor Backend...");
        SpringApplication.run(LanchExpressApplication.class, args);
        System.out.println("✅ Servidor rodando com sucesso! Acesse http://localhost:8080");
    }

}
