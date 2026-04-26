package com.lanchexpress.repository;

import com.lanchexpress.model.Pedido;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface PedidoRepository extends JpaRepository<Pedido, Long> {

    Optional<Pedido> findByCodigoRetirada(String codigoRetirada);

    List<Pedido> findByClienteIdOrderByDataCriacaoDesc(Long clienteId);

    boolean existsByCodigoRetirada(String codigoRetirada);
}
