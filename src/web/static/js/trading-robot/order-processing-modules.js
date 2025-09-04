/**
 * Order Processing Modules - V2 Compliant Order Processing Utilities
 * Handles all order processing and validation operations
 * 
 * @author Agent-1 - Integration & Core Systems Specialist
 * @version 1.0.0 - Trading Robot Frontend V2 Compliance
 * @license MIT
 */

/**
 * Order processing utilities for trading order management
 */
export class OrderProcessingModules {
    /**
     * Validate order data
     */
    static validateOrder(orderData) {
        const errors = [];

        if (!orderData.symbol || orderData.symbol.length < 1) {
            errors.push('Symbol is required');
        }

        if (!orderData.quantity || orderData.quantity < 1) {
            errors.push('Quantity must be at least 1');
        }

        if (orderData.type === 'limit' && (!orderData.price || orderData.price <= 0)) {
            errors.push('Price is required for limit orders');
        }

        if (orderData.type === 'stop' && (!orderData.stopPrice || orderData.stopPrice <= 0)) {
            errors.push('Stop price is required for stop orders');
        }

        if (orderData.type === 'stop_limit') {
            if (!orderData.price || orderData.price <= 0) {
                errors.push('Price is required for stop limit orders');
            }
            if (!orderData.stopPrice || orderData.stopPrice <= 0) {
                errors.push('Stop price is required for stop limit orders');
            }
        }

        return {
            valid: errors.length === 0,
            errors: errors
        };
    }

    /**
     * Simulate order execution
     */
    static async simulateOrderExecution(order) {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Simulate order processing
        order.status = 'submitted';

        // Simulate fill (for market orders)
        if (order.type === 'market') {
            await new Promise(resolve => setTimeout(resolve, 2000));
            order.status = 'filled';
            order.filledPrice = order.side === 'buy' ? 
                order.price * 1.001 : order.price * 0.999; // Simulate slippage
            order.filledQuantity = order.quantity;
        }
    }

    /**
     * Cancel order
     */
    static async cancelOrder(order, orderId) {
        if (!order) {
            console.error('❌ Order not found:', orderId);
            return false;
        }

        if (order.status === 'filled') {
            console.error('❌ Cannot cancel filled order');
            return false;
        }

        order.status = 'cancelled';
        return true;
    }

    /**
     * Process order submission
     */
    static async processOrderSubmission(orderData, orderIdCounter, orders) {
        // Validate order data
        const validation = this.validateOrder(orderData);
        if (!validation.valid) {
            return { success: false, errors: validation.errors };
        }

        // Create order object
        const order = {
            id: orderIdCounter,
            ...orderData,
            status: 'pending',
            timestamp: new Date(),
            filledPrice: null,
            filledQuantity: 0
        };

        // Add to orders list
        orders.unshift(order);
        
        // Simulate order submission
        console.log('📤 Submitting order:', order);
        await this.simulateOrderExecution(order);

        return { success: true, order: order };
    }

    /**
     * Generate order HTML
     */
    static generateOrderHTML(order) {
        return `
            <div class="order-item ${order.status}">
                <div class="order-header">
                    <span class="order-id">#${order.id}</span>
                    <span class="order-symbol">${order.symbol}</span>
                    <span class="order-side ${order.side}">${order.side.toUpperCase()}</span>
                    <span class="order-status ${order.status}">${order.status.toUpperCase()}</span>
                </div>
                <div class="order-details">
                    <span class="order-type">${order.type.toUpperCase()}</span>
                    <span class="order-quantity">${order.quantity}</span>
                    <span class="order-price">$${order.price ? order.price.toFixed(2) : 'Market'}</span>
                    ${order.filledPrice ? `<span class="filled-price">Filled: $${order.filledPrice.toFixed(2)}</span>` : ''}
                </div>
                <div class="order-actions">
                    ${order.status === 'pending' || order.status === 'submitted' ? 
                        `<button onclick="tradingOrderManager.cancelOrder(${order.id})" class="cancel-btn">Cancel</button>` : ''}
                </div>
            </div>
        `;
    }

    /**
     * Update order history display
     */
    static updateOrderHistoryDisplay(orders) {
        const orderHistory = document.getElementById('order-history');
        if (!orderHistory) return;

        orderHistory.innerHTML = orders.map(order => this.generateOrderHTML(order)).join('');
    }

    /**
     * Show order error
     */
    static showOrderError(errors) {
        const errorMessage = errors.join(', ');
        console.error('❌ Order error:', errorMessage);
        
        // Show error in UI
        const errorDiv = document.createElement('div');
        errorDiv.className = 'order-error';
        errorDiv.textContent = errorMessage;
        
        const form = document.getElementById('trading-order-form');
        if (form) {
            form.appendChild(errorDiv);
            setTimeout(() => errorDiv.remove(), 5000);
        }
    }

    /**
     * Load sample order history
     */
    static loadSampleOrderHistory() {
        return [
            {
                id: 1,
                symbol: 'AAPL',
                side: 'buy',
                type: 'market',
                quantity: 100,
                price: 150.00,
                status: 'filled',
                timestamp: new Date(Date.now() - 3600000),
                filledPrice: 150.25,
                filledQuantity: 100
            },
            {
                id: 2,
                symbol: 'GOOGL',
                side: 'sell',
                type: 'limit',
                quantity: 50,
                price: 2800.00,
                status: 'pending',
                timestamp: new Date(Date.now() - 1800000),
                filledPrice: null,
                filledQuantity: 0
            }
        ];
    }
}
