#!/usr/bin/env python3
"""
V3-012: UI Components
====================

Core UI components for Dream.OS mobile app.
V2 compliant with focus on essential UI elements.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class ComponentState(Enum):
    """Component states."""

    LOADING = "loading"
    SUCCESS = "success"
    ERROR = "error"
    EMPTY = "empty"
    DISABLED = "disabled"


class ComponentType(Enum):
    """Component types."""

    BUTTON = "button"
    INPUT = "input"
    TEXT = "text"
    IMAGE = "image"
    LIST = "list"
    CARD = "card"
    MODAL = "modal"
    NAVIGATION = "navigation"


@dataclass
class UIComponent:
    """UI component structure."""

    component_id: str
    name: str
    component_type: ComponentType
    props: dict[str, Any]
    state: ComponentState
    children: list[str]
    styles: dict[str, Any]
    events: list[str]


class ComponentFactory:
    """Factory for creating UI components."""

    @staticmethod
    def create_button(
        component_id: str, text: str, on_press: str = None, style: str = "primary"
    ) -> UIComponent:
        """Create button component."""
        return UIComponent(
            component_id=component_id,
            name=f"Button_{component_id}",
            component_type=ComponentType.BUTTON,
            props={"text": text, "on_press": on_press, "style": style},
            state=ComponentState.SUCCESS,
            children=[],
            styles={
                "backgroundColor": "#007AFF" if style == "primary" else "#8E8E93",
                "textColor": "#FFFFFF",
                "padding": "12px 24px",
                "borderRadius": "8px",
            },
            events=["onPress", "onLongPress"],
        )

    @staticmethod
    def create_input(
        component_id: str, placeholder: str = "", input_type: str = "text"
    ) -> UIComponent:
        """Create input component."""
        return UIComponent(
            component_id=component_id,
            name=f"Input_{component_id}",
            component_type=ComponentType.INPUT,
            props={"placeholder": placeholder, "type": input_type, "value": ""},
            state=ComponentState.SUCCESS,
            children=[],
            styles={
                "borderWidth": "1px",
                "borderColor": "#C7C7CC",
                "padding": "12px",
                "borderRadius": "8px",
                "fontSize": "16px",
            },
            events=["onChange", "onFocus", "onBlur"],
        )

    @staticmethod
    def create_text(component_id: str, text: str, style: str = "body") -> UIComponent:
        """Create text component."""
        return UIComponent(
            component_id=component_id,
            name=f"Text_{component_id}",
            component_type=ComponentType.TEXT,
            props={"text": text, "style": style},
            state=ComponentState.SUCCESS,
            children=[],
            styles={
                "fontSize": "16px" if style == "body" else "24px",
                "fontWeight": "normal" if style == "body" else "bold",
                "color": "#000000",
            },
            events=[],
        )

    @staticmethod
    def create_card(component_id: str, title: str, content: str) -> UIComponent:
        """Create card component."""
        return UIComponent(
            component_id=component_id,
            name=f"Card_{component_id}",
            component_type=ComponentType.CARD,
            props={"title": title, "content": content},
            state=ComponentState.SUCCESS,
            children=[],
            styles={
                "backgroundColor": "#FFFFFF",
                "padding": "16px",
                "borderRadius": "12px",
                "shadowColor": "#000000",
                "shadowOffset": "0px 2px",
                "shadowOpacity": "0.1",
                "shadowRadius": "4px",
            },
            events=["onPress"],
        )

    @staticmethod
    def create_list(component_id: str, items: list[str]) -> UIComponent:
        """Create list component."""
        return UIComponent(
            component_id=component_id,
            name=f"List_{component_id}",
            component_type=ComponentType.LIST,
            props={"items": items, "renderItem": "default"},
            state=ComponentState.SUCCESS,
            children=[],
            styles={"backgroundColor": "#F2F2F7", "padding": "8px"},
            events=["onItemPress", "onRefresh"],
        )


class ComponentRenderer:
    """Component rendering logic."""

    def __init__(self):
        self.rendered_components = {}

    def render_component(self, component: UIComponent) -> dict[str, Any]:
        """Render component to JSON structure."""
        rendered = {
            "id": component.component_id,
            "type": component.component_type.value,
            "name": component.name,
            "props": component.props,
            "state": component.state.value,
            "styles": component.styles,
            "events": component.events,
            "children": component.children,
            "rendered_at": datetime.now().isoformat(),
        }

        self.rendered_components[component.component_id] = rendered
        return rendered

    def render_screen(self, components: list[UIComponent]) -> dict[str, Any]:
        """Render multiple components as a screen."""
        rendered_components = []

        for component in components:
            rendered = self.render_component(component)
            rendered_components.append(rendered)

        return {
            "screen": {
                "components": rendered_components,
                "total_components": len(rendered_components),
                "rendered_at": datetime.now().isoformat(),
            }
        }

    def get_component(self, component_id: str) -> dict[str, Any] | None:
        """Get rendered component by ID."""
        return self.rendered_components.get(component_id)

    def update_component_state(self, component_id: str, new_state: ComponentState) -> bool:
        """Update component state."""
        if component_id in self.rendered_components:
            self.rendered_components[component_id]["state"] = new_state.value
            self.rendered_components[component_id]["updated_at"] = datetime.now().isoformat()
            return True
        return False


class ComponentValidator:
    """Component validation logic."""

    @staticmethod
    def validate_component(component: UIComponent) -> dict[str, Any]:
        """Validate component structure."""
        errors = []
        warnings = []

        # Check required fields
        if not component.component_id:
            errors.append("Component ID is required")

        if not component.name:
            errors.append("Component name is required")

        if not component.component_type:
            errors.append("Component type is required")

        # Check props
        if component.component_type == ComponentType.BUTTON:
            if "text" not in component.props:
                errors.append("Button component requires 'text' prop")

        elif component.component_type == ComponentType.INPUT:
            if "placeholder" not in component.props:
                warnings.append("Input component should have 'placeholder' prop")

        # Check styles
        if not component.styles:
            warnings.append("Component has no styles defined")

        # Check events
        if not component.events:
            warnings.append("Component has no events defined")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "component_id": component.component_id,
        }

    @staticmethod
    def validate_screen(components: list[UIComponent]) -> dict[str, Any]:
        """Validate screen with multiple components."""
        all_valid = True
        component_results = []

        for component in components:
            result = ComponentValidator.validate_component(component)
            component_results.append(result)
            if not result["valid"]:
                all_valid = False

        return {
            "valid": all_valid,
            "total_components": len(components),
            "valid_components": sum(1 for r in component_results if r["valid"]),
            "component_results": component_results,
        }


def main():
    """Main execution function."""
    print("🎨 V3-012 UI Components - Testing...")

    # Create sample components
    factory = ComponentFactory()
    renderer = ComponentRenderer()
    validator = ComponentValidator()

    # Create test components
    button = factory.create_button("btn1", "Click Me", "onButtonPress")
    input_field = factory.create_input("input1", "Enter text here")
    text = factory.create_text("text1", "Hello World", "title")
    card = factory.create_card("card1", "Sample Card", "This is card content")
    list_comp = factory.create_list("list1", ["Item 1", "Item 2", "Item 3"])

    components = [button, input_field, text, card, list_comp]

    # Validate components
    validation_result = validator.validate_screen(components)
    print(
        f"✅ Validation: {validation_result['valid_components']}/{validation_result['total_components']} components valid"
    )

    # Render components
    screen = renderer.render_screen(components)
    print(f"🎨 Rendered: {screen['screen']['total_components']} components")

    # Test state update
    renderer.update_component_state("btn1", ComponentState.LOADING)
    updated_component = renderer.get_component("btn1")
    print(f"🔄 State update: {updated_component['state'] if updated_component else 'Failed'}")

    print("✅ V3-012 UI Components completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())
