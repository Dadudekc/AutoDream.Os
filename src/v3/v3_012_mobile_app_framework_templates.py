#!/usr/bin/env python3
"""
V3-012 Mobile Application Framework - Templates
==============================================

Component templates and code generation utilities for mobile framework.

Author: Agent-7 (Implementation Specialist)
License: MIT
V2 Compliance: ≤400 lines, modular design, template management
"""


from .v3_012_mobile_app_framework_core import ComponentType, MobileComponent


class ComponentTemplateManager:
    """Manages component templates and code generation"""

    def __init__(self):
        self.component_templates = self._initialize_component_templates()

    def _initialize_component_templates(self) -> dict[ComponentType, str]:
        """Initialize component templates"""
        return {
            ComponentType.SCREEN: """
import React from 'react';
import {{ View, Text, StyleSheet }} from 'react-native';

interface {component_name}Props {{
    {props_interface}
}}

const {component_name}: React.FC<{component_name}Props> = ({{ {props_destructure} }}) => {{
    return (
        <View style={{styles.container}}>
            <Text style={{styles.title}}>{component_name}</Text>
            {component_content}
        </View>
    );
}};

const styles = StyleSheet.create({{
    container: {{
        flex: 1,
        padding: 16,
        backgroundColor: '#ffffff',
    }},
    title: {{
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 16,
    }},
}});

export default {component_name};
""",
            ComponentType.WIDGET: """
import React from 'react';
import {{ View, Text, StyleSheet }} from 'react-native';

interface {component_name}Props {{
    {props_interface}
}}

const {component_name}: React.FC<{component_name}Props> = ({{ {props_destructure} }}) => {{
    return (
        <View style={{styles.container}}>
            {component_content}
        </View>
    );
}};

const styles = StyleSheet.create({{
    container: {{
        padding: 8,
        backgroundColor: '#f5f5f5',
        borderRadius: 8,
    }},
}});

export default {component_name};
""",
            ComponentType.SERVICE: """
import {{ Platform }} from 'react-native';

class {component_name} {{
    private static instance: {component_name};

    private constructor() {{
        // Private constructor for singleton
    }}

    public static getInstance(): {component_name} {{
        if (!{component_name}.instance) {{
            {component_name}.instance = new {component_name}();
        }}
        return {component_name}.instance;
    }}

    {service_methods}

    private log(message: string): void {{
        console.log(`[{component_name}] ${{message}}`);
    }}
}}

export default {component_name};
""",
            ComponentType.UTILITY: """
export class {component_name} {{
    {utility_methods}

    private static validateInput(input: any): boolean {{
        return input !== null && input !== undefined;
    }}
}}

export default {component_name};
""",
            ComponentType.STORAGE: """
import AsyncStorage from '@react-native-async-storage/async-storage';

export class {component_name} {{
    private static readonly STORAGE_KEY = '{storage_key}';

    {storage_methods}

    private static async handleError(error: any): Promise<void> {{
        console.error('Storage error:', error);
    }}
}}

export default {component_name};
""",
        }

    def generate_component_code(self, component: MobileComponent) -> str:
        """Generate code for mobile component"""
        template = self.component_templates.get(component.component_type, "")

        # Replace template variables
        code = template.replace("{component_name}", component.name)
        code = code.replace("{props_interface}", self._generate_props_interface(component))
        code = code.replace("{props_destructure}", self._generate_props_destructure(component))
        code = code.replace("{component_content}", self._generate_component_content(component))
        code = code.replace("{service_methods}", self._generate_service_methods(component))
        code = code.replace("{utility_methods}", self._generate_utility_methods(component))
        code = code.replace("{storage_methods}", self._generate_storage_methods(component))
        code = code.replace("{storage_key}", f"{component.name.upper()}_STORAGE")

        return code

    def _generate_props_interface(self, component: MobileComponent) -> str:
        """Generate TypeScript props interface"""
        if not component.properties:
            return ""

        props = []
        for prop_name, prop_type in component.properties.items():
            props.append(f"    {prop_name}: {prop_type};")
        return "\n".join(props)

    def _generate_props_destructure(self, component: MobileComponent) -> str:
        """Generate props destructuring"""
        if not component.properties:
            return ""
        return ", ".join(component.properties.keys())

    def _generate_component_content(self, component: MobileComponent) -> str:
        """Generate component content based on type"""
        if component.component_type == ComponentType.SCREEN:
            return "<Text>Screen content goes here</Text>"
        elif component.component_type == ComponentType.WIDGET:
            return "<Text>Widget content goes here</Text>"
        else:
            return "// Component content"

    def _generate_service_methods(self, component: MobileComponent) -> str:
        """Generate service methods"""
        methods = []
        for method in component.methods:
            methods.append(
                f"""
    public {method}(): void {{
        this.log('{method} called');
        // Implementation goes here
    }}"""
            )
        return "\n".join(methods)

    def _generate_utility_methods(self, component: MobileComponent) -> str:
        """Generate utility methods"""
        methods = []
        for method in component.methods:
            methods.append(
                f"""
    public static {method}(data: any): any {{
        if (!this.validateInput(data)) {{
            throw new Error('Invalid input data');
        }}
        // Implementation goes here
        return data;
    }}"""
            )
        return "\n".join(methods)

    def _generate_storage_methods(self, component: MobileComponent) -> str:
        """Generate storage methods"""
        methods = []
        for method in component.methods:
            if method == "save":
                methods.append(
                    f"""
    public static async {method}(key: string, value: any): Promise<void> {{
        try {{
            await AsyncStorage.setItem(key, JSON.stringify(value));
        }} catch (error) {{
            await this.handleError(error);
        }}
    }}"""
                )
            elif method == "load":
                methods.append(
                    f"""
    public static async {method}(key: string): Promise<any> {{
        try {{
            const value = await AsyncStorage.getItem(key);
            return value ? JSON.parse(value) : null;
        }} catch (error) {{
            await this.handleError(error);
            return null;
        }}
    }}"""
                )
            elif method == "delete":
                methods.append(
                    f"""
    public static async {method}(key: string): Promise<void> {{
        try {{
            await AsyncStorage.removeItem(key);
        }} catch (error) {{
            await this.handleError(error);
        }}
    }}"""
                )
            elif method == "clear":
                methods.append(
                    f"""
    public static async {method}(): Promise<void> {{
        try {{
            await AsyncStorage.clear();
        }} catch (error) {{
            await this.handleError(error);
        }}
    }}"""
                )
            elif method == "exists":
                methods.append(
                    f"""
    public static async {method}(key: string): Promise<boolean> {{
        try {{
            const value = await AsyncStorage.getItem(key);
            return value !== null;
        }} catch (error) {{
            await this.handleError(error);
            return false;
        }}
    }}"""
                )
        return "\n".join(methods)
