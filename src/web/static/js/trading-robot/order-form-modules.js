/**
 * Order Form Modules - V2 Compliant Order Form Utilities
 * Handles all order form creation and management operations
 *
 * @author Agent-1 - Integration & Core Systems Specialist
 * @version 1.0.0 - Trading Robot Frontend V2 Compliance
 * @license MIT
 */

/**
 * Order form utilities for trading order management
 */
export class OrderFormModules {
    /**
     * Setup order form
     */
    static setupOrderForm() {
        const orderForm = document.getElementById('order-form');
        if (!orderForm) return;

        orderForm.innerHTML = this.generateOrderFormHTML();
        this.setupOrderFormEvents();
    }

    /**
     * Generate order form HTML
     */
    static generateOrderFormHTML() {
        return `
            <form id="trading-order-form" class="order-form">
                <div class="form-group">
                    <label for="order-symbol">Symbol:</label>
                    <input type="text" id="order-symbol" name="symbol" required>
                </div>

                <div class="form-group">
                    <label for="order-side">Side:</label>
                    <select id="order-side" name="side" required>
                        <option value="buy">Buy</option>
                        <option value="sell">Sell</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="order-type">Type:</label>
                    <select id="order-type" name="type" required>
                        <option value="market">Market</option>
                        <option value="limit">Limit</option>
                        <option value="stop">Stop</option>
                        <option value="stop_limit">Stop Limit</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="order-quantity">Quantity:</label>
                    <input type="number" id="order-quantity" name="quantity" min="1" required>
                </div>

                <div class="form-group" id="price-group">
                    <label for="order-price">Price:</label>
                    <input type="number" id="order-price" name="price" step="0.01" min="0">
                </div>

                <div class="form-group" id="stop-price-group" style="display: none;">
                    <label for="order-stop-price">Stop Price:</label>
                    <input type="number" id="order-stop-price" name="stopPrice" step="0.01" min="0">
                </div>

                <button type="submit" class="submit-order-btn">Submit Order</button>
            </form>
        `;
    }

    /**
     * Setup order form events
     */
    static setupOrderFormEvents() {
        const form = document.getElementById('trading-order-form');
        const orderTypeSelect = document.getElementById('order-type');
        const priceGroup = document.getElementById('price-group');
        const stopPriceGroup = document.getElementById('stop-price-group');

        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleOrderSubmission(e);
            });
        }

        if (orderTypeSelect) {
            orderTypeSelect.addEventListener('change', (e) => {
                this.handleOrderTypeChange(e, priceGroup, stopPriceGroup);
            });
        }
    }

    /**
     * Handle order type change
     */
    static handleOrderTypeChange(event, priceGroup, stopPriceGroup) {
        const orderType = event.target.value;

        if (orderType === 'market') {
            priceGroup.style.display = 'none';
            stopPriceGroup.style.display = 'none';
        } else if (orderType === 'limit') {
            priceGroup.style.display = 'block';
            stopPriceGroup.style.display = 'none';
        } else if (orderType === 'stop') {
            priceGroup.style.display = 'none';
            stopPriceGroup.style.display = 'block';
        } else if (orderType === 'stop_limit') {
            priceGroup.style.display = 'block';
            stopPriceGroup.style.display = 'block';
        }
    }

    /**
     * Handle order submission
     */
    static handleOrderSubmission(event) {
        const formData = new FormData(event.target);
        const orderData = {
            symbol: formData.get('symbol').toUpperCase(),
            side: formData.get('side'),
            type: formData.get('type'),
            quantity: parseInt(formData.get('quantity')),
            price: parseFloat(formData.get('price')) || null,
            stopPrice: parseFloat(formData.get('stopPrice')) || null
        };

        // Trigger order submission callback
        if (window.tradingOrderManager) {
            window.tradingOrderManager.submitOrder(orderData);
        }

        event.target.reset();
    }

    /**
     * Generate order history HTML
     */
    static generateOrderHistoryHTML() {
        return `
            <div id="order-history" class="order-history">
                <h3>Order History</h3>
                <div class="order-list">
                    <!-- Orders will be populated here -->
                </div>
            </div>
        `;
    }

    /**
     * Setup order history display
     */
    static setupOrderHistoryDisplay() {
        const orderContainer = document.getElementById('order-container');
        if (!orderContainer) return;

        orderContainer.innerHTML = this.generateOrderHistoryHTML();
    }

    /**
     * Update order form validation
     */
    static updateOrderFormValidation(orderType) {
        const priceInput = document.getElementById('order-price');
        const stopPriceInput = document.getElementById('order-stop-price');

        if (orderType === 'limit' || orderType === 'stop_limit') {
            if (priceInput) priceInput.required = true;
        } else {
            if (priceInput) priceInput.required = false;
        }

        if (orderType === 'stop' || orderType === 'stop_limit') {
            if (stopPriceInput) stopPriceInput.required = true;
        } else {
            if (stopPriceInput) stopPriceInput.required = false;
        }
    }

    /**
     * Clear order form
     */
    static clearOrderForm() {
        const form = document.getElementById('trading-order-form');
        if (form) {
            form.reset();
            this.updateOrderFormValidation('market');
        }
    }

    /**
     * Set order form values
     */
    static setOrderFormValues(orderData) {
        const symbolInput = document.getElementById('order-symbol');
        const sideSelect = document.getElementById('order-side');
        const typeSelect = document.getElementById('order-type');
        const quantityInput = document.getElementById('order-quantity');
        const priceInput = document.getElementById('order-price');
        const stopPriceInput = document.getElementById('order-stop-price');

        if (symbolInput) symbolInput.value = orderData.symbol || '';
        if (sideSelect) sideSelect.value = orderData.side || 'buy';
        if (typeSelect) typeSelect.value = orderData.type || 'market';
        if (quantityInput) quantityInput.value = orderData.quantity || '';
        if (priceInput) priceInput.value = orderData.price || '';
        if (stopPriceInput) stopPriceInput.value = orderData.stopPrice || '';

        this.updateOrderFormValidation(orderData.type || 'market');
    }
}
