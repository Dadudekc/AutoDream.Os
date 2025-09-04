/**
 * Trading Order Manager - V2 Compliant Order Management
 * Order submission, tracking, and execution management
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-1 - Integration & Core Systems Specialist
 * @version 1.0.0 - Trading Robot Frontend V2 Compliance
 * @license MIT
 */

import { OrderFormModules } from './order-form-modules.js';
import { OrderProcessingModules } from './order-processing-modules.js';

// ================================
// TRADING ORDER MANAGER
// ================================

/**
 * Order Manager for trading order submission and tracking
 * Handles order creation, submission, tracking, and execution
 */
export class TradingOrderManager {
    constructor() {
        this.orders = [];
        this.orderCallbacks = [];
        this.orderIdCounter = 1;
        this.orderTypes = ['market', 'limit', 'stop', 'stop_limit'];
        this.orderSides = ['buy', 'sell'];
        this.orderStatuses = ['pending', 'submitted', 'filled', 'cancelled', 'rejected'];
    }

    /**
     * Initialize order manager
     */
    async initialize() {
        try {
            console.log('📋 Initializing Trading Order Manager...');
            await this.loadOrderHistory();
            OrderFormModules.setupOrderForm();
            console.log('✅ Trading Order Manager initialized');
        } catch (error) {
            console.error('❌ Trading Order Manager initialization failed:', error);
            throw error;
        }
    }

    /**
     * Load order history
     */
    async loadOrderHistory() {
        try {
            this.orders = OrderProcessingModules.loadSampleOrderHistory();
        } catch (error) {
            console.error('❌ Error loading order history:', error);
            throw error;
        }
    }

    /**
     * Submit order
     */
    async submitOrder(orderData) {
        try {
            const result = await OrderProcessingModules.processOrderSubmission(
                orderData, 
                this.orderIdCounter++, 
                this.orders
            );

            if (!result.success) {
                OrderProcessingModules.showOrderError(result.errors);
                return;
            }

            // Notify callbacks
            this.notifyOrderCallbacks(result.order);
            
            // Update UI
            this.updateOrderHistory();
            
        } catch (error) {
            console.error('❌ Error submitting order:', error);
            OrderProcessingModules.showOrderError(['Failed to submit order']);
        }
    }

    /**
     * Cancel order
     */
    async cancelOrder(orderId) {
        const order = this.orders.find(o => o.id === orderId);
        const success = await OrderProcessingModules.cancelOrder(order, orderId);
        
        if (success) {
            this.notifyOrderCallbacks(order);
            this.updateOrderHistory();
        }
    }

    /**
     * Update order history display
     */
    updateOrderHistory() {
        OrderProcessingModules.updateOrderHistoryDisplay(this.orders);
    }

    /**
     * Add callback for order events
     */
    addOrderCallback(callback) {
        this.orderCallbacks.push(callback);
    }

    /**
     * Remove callback
     */
    removeOrderCallback(callback) {
        const index = this.orderCallbacks.indexOf(callback);
        if (index > -1) {
            this.orderCallbacks.splice(index, 1);
        }
    }

    /**
     * Notify order callbacks
     */
    notifyOrderCallbacks(order) {
        this.orderCallbacks.forEach(callback => {
            try {
                callback(order);
            } catch (error) {
                console.error('❌ Error in order callback:', error);
            }
        });
    }

    /**
     * Get order history
     */
    getOrderHistory() {
        return [...this.orders];
    }

    /**
     * Get order by ID
     */
    getOrderById(orderId) {
        return this.orders.find(order => order.id === orderId);
    }

    /**
     * Get orders by status
     */
    getOrdersByStatus(status) {
        return this.orders.filter(order => order.status === status);
    }

    /**
     * Get orders by symbol
     */
    getOrdersBySymbol(symbol) {
        return this.orders.filter(order => order.symbol === symbol);
    }

    /**
     * Get pending orders
     */
    getPendingOrders() {
        return this.getOrdersByStatus('pending');
    }

    /**
     * Get filled orders
     */
    getFilledOrders() {
        return this.getOrdersByStatus('filled');
    }

    /**
     * Get cancelled orders
     */
    getCancelledOrders() {
        return this.getOrdersByStatus('cancelled');
    }

    /**
     * Get order statistics
     */
    getOrderStatistics() {
        const stats = {
            total: this.orders.length,
            pending: this.getPendingOrders().length,
            filled: this.getFilledOrders().length,
            cancelled: this.getCancelledOrders().length,
            buy: this.orders.filter(o => o.side === 'buy').length,
            sell: this.orders.filter(o => o.side === 'sell').length
        };

        return stats;
    }

    /**
     * Clear order history
     */
    clearOrderHistory() {
        this.orders = [];
        this.updateOrderHistory();
    }

    /**
     * Export order history
     */
    exportOrderHistory() {
        const dataStr = JSON.stringify(this.orders, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = 'order-history.json';
        link.click();
        
        URL.revokeObjectURL(url);
    }

    /**
     * Import order history
     */
    async importOrderHistory(file) {
        try {
            const text = await file.text();
            const importedOrders = JSON.parse(text);
            
            if (Array.isArray(importedOrders)) {
                this.orders = importedOrders;
                this.updateOrderHistory();
                console.log('✅ Order history imported successfully');
            } else {
                throw new Error('Invalid file format');
            }
        } catch (error) {
            console.error('❌ Error importing order history:', error);
            throw error;
        }
    }

    /**
     * Get next order ID
     */
    getNextOrderId() {
        return this.orderIdCounter;
    }

    /**
     * Set order ID counter
     */
    setOrderIdCounter(counter) {
        this.orderIdCounter = counter;
    }

    /**
     * Destroy order manager
     */
    destroy() {
        this.orders = [];
        this.orderCallbacks = [];
        this.orderIdCounter = 1;
    }
}

// Make available globally for form callbacks
window.tradingOrderManager = null;