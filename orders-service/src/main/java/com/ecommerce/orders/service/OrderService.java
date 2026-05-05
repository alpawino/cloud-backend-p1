package com.ecommerce.orders.service;

import com.ecommerce.orders.dto.CreateOrderItemRequest;
import com.ecommerce.orders.dto.CreateOrderRequest;
import com.ecommerce.orders.dto.OrderDetailResponse;
import com.ecommerce.orders.dto.OrderResponse;
import com.ecommerce.orders.model.Order;
import com.ecommerce.orders.model.OrderDetail;
import com.ecommerce.orders.repository.OrderRepository;
import java.math.BigDecimal;
import java.util.List;
import java.util.stream.Collectors;
import javax.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;

    @Transactional
    public OrderResponse createOrder(CreateOrderRequest request) {
        Order order = new Order();
        order.setUserId(request.getUserId());

        BigDecimal total = BigDecimal.ZERO;
        for (CreateOrderItemRequest itemRequest : request.getItems()) {
            OrderDetail detail = new OrderDetail();
            detail.setProductId(itemRequest.getProductId());
            detail.setQuantity(itemRequest.getQuantity());
            detail.setUnitPrice(itemRequest.getUnitPrice());

            BigDecimal lineTotal = itemRequest.getUnitPrice()
                .multiply(BigDecimal.valueOf(itemRequest.getQuantity()));
            detail.setLineTotal(lineTotal);
            total = total.add(lineTotal);

            order.addDetail(detail);
        }

        order.setTotal(total);
        Order savedOrder = orderRepository.save(order);
        return mapToResponse(savedOrder);
    }

    @Transactional(readOnly = true)
    public OrderResponse getOrderById(Long orderId) {
        Order order = orderRepository.findById(orderId)
            .orElseThrow(() -> new EntityNotFoundException("Order not found: " + orderId));
        order.getDetails().size();
        return mapToResponse(order);
    }

    @Transactional(readOnly = true)
    public List<OrderResponse> getOrdersByUserId(Long userId) {
        return orderRepository.findByUserId(userId).stream()
            .map(this::mapToResponse)
            .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public List<OrderResponse> getAllOrders() {
        return orderRepository.findAll().stream()
            .peek(order -> order.getDetails().size())
            .map(this::mapToResponse)
            .collect(Collectors.toList());
    }

    private OrderResponse mapToResponse(Order order) {
        List<OrderDetailResponse> details = order.getDetails().stream()
            .map(detail -> new OrderDetailResponse(
                detail.getId(),
                detail.getProductId(),
                detail.getQuantity(),
                detail.getUnitPrice(),
                detail.getLineTotal()
            ))
            .collect(Collectors.toList());

        return new OrderResponse(
            order.getId(),
            order.getUserId(),
            order.getStatus(),
            order.getTotal(),
            order.getCreatedAt(),
            details
        );
    }
}
