package com.ecommerce.orders.dto;

import com.ecommerce.orders.model.OrderStatus;
import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class OrderResponse {
    private Long id;
    private Long userId;
    private OrderStatus status;
    private BigDecimal total;
    private OffsetDateTime createdAt;
    private List<OrderDetailResponse> details;
}
