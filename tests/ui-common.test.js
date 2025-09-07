import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import {
    setupSearchInterface,
    setupDocumentManagement
} from '../src/web/static/js/vector-database/ui-common.js';

function createElement(tag, className, attrs = {}, text = '') {
    return {
        tagName: tag.toUpperCase(),
        className,
        attributes: { ...attrs },
        textContent: text,
        children: [],
        setAttribute(key, value) { this.attributes[key] = value; },
        appendChild(child) { this.children.push(child); }
    };
}

function addEventListenerMock(el, event, handler) {
    el._events = el._events || {};
    el._events[event] = handler;
}

describe('ui-common helpers', () => {
    it('setupSearchInterface stores elements and binds events', () => {
        const elements = {};
        const calls = [];
        setupSearchInterface({
            createElement,
            elements,
            addEventListener: addEventListenerMock,
            handleSearch: () => calls.push('search')
        });
        assert.ok(elements.searchInput);
        elements.searchButton._events.click();
        assert.deepEqual(calls, ['search']);
    });

    it('setupDocumentManagement stores elements', () => {
        const elements = {};
        const calls = [];
        setupDocumentManagement({
            createElement,
            elements,
            addEventListener: addEventListenerMock,
            handleAddDocument: () => calls.push('add')
        });
        assert.ok(elements.docList);
        elements.addButton._events.click();
        assert.deepEqual(calls, ['add']);
    });
});

