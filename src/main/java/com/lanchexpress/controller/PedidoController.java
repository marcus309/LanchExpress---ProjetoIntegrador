package com.lanchexpress.controller;

import com.lanchexpress.dto.PedidoRequest;
import com.lanchexpress.model.Pedido;
import com.lanchexpress.model.Pedido.StatusPedido;
import com.lanchexpress.service.PedidoService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/pedidos")
@CrossOrigin(origins = "*")
public class PedidoController {

    private final PedidoService pedidoService;

    public PedidoController(PedidoService pedidoService) {
        this.pedidoService = pedidoService;
    }

    @GetMapping
    public ResponseEntity<List<Pedido>> listar(@RequestParam(required = false) Long clienteId) {
        if (clienteId != null) {
            return ResponseEntity.ok(pedidoService.listarPorCliente(clienteId));
        }
        return ResponseEntity.ok(pedidoService.listarTodos());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Pedido> buscarPorId(@PathVariable Long id) {
        return ResponseEntity.ok(pedidoService.buscarPorId(id));
    }

    @GetMapping("/codigo/{codigo}")
    public ResponseEntity<Pedido> buscarPorCodigo(@PathVariable String codigo) {
        return ResponseEntity.ok(pedidoService.buscarPorCodigo(codigo));
    }

    @PostMapping
    public ResponseEntity<Pedido> criar(@RequestBody PedidoRequest request) {
        Pedido pedido = pedidoService.criar(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(pedido);
    }

    @PatchMapping("/{id}/status")
    public ResponseEntity<Pedido> atualizarStatus(@PathVariable Long id,
                                                   @RequestParam StatusPedido status) {
        return ResponseEntity.ok(pedidoService.atualizarStatus(id, status));
    }

    @PostMapping("/{id}/cancelar")
    public ResponseEntity<Void> cancelar(@PathVariable Long id) {
        pedidoService.cancelar(id);
        return ResponseEntity.noContent().build();
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletar(@PathVariable Long id) {
        pedidoService.deletar(id);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/{id}/avaliar")
    public ResponseEntity<Pedido> avaliar(@PathVariable Long id,
                                           @RequestBody AvaliacaoRequest body) {
        return ResponseEntity.ok(pedidoService.avaliar(id, body.nota, body.comentario));
    }

    public static class AvaliacaoRequest {
        public Integer nota;
        public String comentario;
    }
}
