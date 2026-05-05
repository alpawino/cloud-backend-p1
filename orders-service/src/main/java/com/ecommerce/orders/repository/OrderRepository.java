package com.ecommerce.orders.repository;

import com.ecommerce.orders.model.Order;
import java.util.List;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OrderRepository extends JpaRepository<Order, Long> {

    @EntityGraph(attributePaths = "details")
    List<Order> findByUserId(Long userId);
}
