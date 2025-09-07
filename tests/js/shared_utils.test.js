import { test } from 'node:test';
import assert from 'node:assert/strict';
import { dom, createEventBus } from '../../src/web/static/js/shared_utils.js';

// Basic DOM stubs
const mockDocument = {
    readyState: 'complete',
    _callback: null,
    addEventListener(event, cb) {
        if (event === 'DOMContentLoaded') {
            this._callback = cb;
        }
    },
    createElement(tag) {
        return {
            tagName: tag.toUpperCase(),
            attributes: {},
            className: '',
            textContent: '',
            setAttribute(key, value) {
                this.attributes[key] = value;
                this[key] = value;
            },
            appendChild(child) {
                (this.children ||= []).push(child);
            },
            classList: {
                classes: new Set(),
                add(cls) { this.classes.add(cls); },
                remove(cls) { this.classes.delete(cls); },
                contains(cls) { return this.classes.has(cls); }
            }
        };
    }
};

global.document = mockDocument;
global.window = {};
global.HTMLElement = function() {};

function createMockElement() {
    return mockDocument.createElement('div');
}

test('addClass adds class', () => {
    const el = createMockElement();
    dom.addClass(el, 'test');
    assert.ok(el.classList.contains('test'));
});

test('removeClass removes class', () => {
    const el = createMockElement();
    dom.addClass(el, 'test');
    dom.removeClass(el, 'test');
    assert.ok(!el.classList.contains('test'));
});

test('toggleClass toggles class', () => {
    const el = createMockElement();
    dom.toggleClass(el, 'test');
    assert.ok(el.classList.contains('test'));
    dom.toggleClass(el, 'test');
    assert.ok(!el.classList.contains('test'));
});

test('ready calls callback immediately when document ready', () => {
    mockDocument.readyState = 'complete';
    let called = false;
    dom.ready(() => { called = true; });
    assert.ok(called);
});

test('createElement applies attributes and content', () => {
    const el = dom.createElement('span', { className: 'x', id: 'y' }, 'hello');
    assert.strictEqual(el.className, 'x');
    assert.strictEqual(el.id, 'y');
    assert.strictEqual(el.textContent, 'hello');
});

test('event bus emits and triggers events', () => {
    const bus = createEventBus();
    let data = null;
    const handler = d => { data = d; };
    bus.on('test', handler);
    bus.emit('test', 42);
    assert.strictEqual(data, 42);
    bus.off('test', handler);
    data = null;
    bus.trigger('test', 1);
    assert.strictEqual(data, null);
});
