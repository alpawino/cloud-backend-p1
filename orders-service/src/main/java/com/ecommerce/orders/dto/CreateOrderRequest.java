package com.ecommerce.orders.dto;

import java.util.List;
import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class CreateOrderRequest {

    @NotNull
    private Long userId;

    @Valid
    @NotEmpty
    private List<CreateOrderItemRequest> items;
}
