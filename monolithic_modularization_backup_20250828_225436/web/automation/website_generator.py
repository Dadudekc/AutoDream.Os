"""
Website Generator for Agent_Cellphone_V2_Repository
Automatically generates websites from templates, configurations, and content specifications
"""

import json
import logging
import os
import shutil

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from jinja2 import Environment, FileSystemLoader, Template
import yaml


@dataclass
class WebsiteConfig:
    """Configuration for website generation"""

    name: str
    title: str
    description: str
    author: str
    version: str = "1.0.0"
    base_url: str = ""
    theme: str = "default"
    language: str = "en"
    meta_tags: Dict[str, str] = None
    social_media: Dict[str, str] = None
    analytics: Dict[str, str] = None
    seo: Dict[str, str] = None

    def __post_init__(self):
        if self.meta_tags is None:
            self.meta_tags = {}
        if self.social_media is None:
            self.social_media = {}
        if self.analytics is None:
            self.analytics = {}
        if self.seo is None:
            self.seo = {}


@dataclass
class PageConfig:
    """Configuration for individual pages"""

    name: str
    title: str
    template: str
    route: str
    content: Dict[str, Any] = None
    meta: Dict[str, str] = None
    components: List[str] = None

    def __post_init__(self):
        if self.content is None:
            self.content = {}
        if self.meta is None:
            self.meta = {}
        if self.components is None:
            self.components = []


@dataclass
class ComponentConfig:
    """Configuration for UI components"""

    name: str
    type: str  # header, footer, navigation, content, sidebar, etc.
    template: str
    data: Dict[str, Any] = None
    styles: Dict[str, str] = None
    scripts: List[str] = None

    def __post_init__(self):
        if self.data is None:
            self.data = {}
        if self.styles is None:
            self.styles = {}
        if self.scripts is None:
            self.scripts = []


class WebsiteGenerator:
    """Main website generator class"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.parent.parent.parent
        self.web_dir = self.project_root / "src" / "web"
        self.templates_dir = self.web_dir / "templates"
        self.static_dir = self.web_dir / "static"
        self.output_dir = self.project_root / "generated_websites"

        self.logger = self._setup_logging()
        self.jinja_env = self._setup_jinja()

        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True)

        self.logger.info(
            f"Website Generator initialized. Project root: {self.project_root}"
        )

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger("WebsiteGenerator")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _setup_jinja(self) -> Environment:
        """Setup Jinja2 template environment"""
        loader = FileSystemLoader(str(self.templates_dir))
        env = Environment(loader=loader)

        # Add custom filters
        env.filters["jsonify"] = lambda obj: json.dumps(obj, indent=2)
        env.filters["slugify"] = (
            lambda text: text.lower().replace(" ", "-").replace("_", "-")
        )

        return env

    def generate_website(
        self,
        config: WebsiteConfig,
        pages: List[PageConfig],
        components: List[ComponentConfig] = None,
    ) -> Path:
        """Generate a complete website from configuration"""
        try:
            self.logger.info(f"Starting website generation for: {config.name}")

            # Create website directory
            website_dir = self.output_dir / config.name
            if website_dir.exists():
                shutil.rmtree(website_dir)
            website_dir.mkdir(parents=True)

            # Generate components first
            if components:
                self._generate_components(website_dir, components)

            # Generate pages
            self._generate_pages(website_dir, config, pages, components)

            # Generate static assets
            self._generate_static_assets(website_dir, config)

            # Generate configuration files
            self._generate_config_files(website_dir, config, pages, components)

            # Generate sitemap
            self._generate_sitemap(website_dir, config, pages)

            self.logger.info(f"Website generated successfully at: {website_dir}")
            return website_dir

        except Exception as e:
            self.logger.error(f"Failed to generate website: {e}")
            raise

    def _generate_components(
        self, website_dir: Path, components: List[ComponentConfig]
    ):
        """Generate reusable UI components"""
        components_dir = website_dir / "components"
        components_dir.mkdir(exist_ok=True)

        for component in components:
            try:
                component_file = components_dir / f"{component.name}.html"

                # Load component template
                template = self.jinja_env.get_template(component.template)

                # Render component
                rendered = template.render(
                    component=component,
                    data=component.data,
                    styles=component.styles,
                    scripts=component.scripts,
                )

                # Write component file
                component_file.write_text(rendered, encoding="utf-8")
                self.logger.debug(f"Generated component: {component.name}")

            except Exception as e:
                self.logger.warning(
                    f"Failed to generate component {component.name}: {e}"
                )

    def _generate_pages(
        self,
        website_dir: Path,
        config: WebsiteConfig,
        pages: List[PageConfig],
        components: List[ComponentConfig] = None,
    ):
        """Generate individual pages"""
        pages_dir = website_dir / "pages"
        pages_dir.mkdir(exist_ok=True)

        for page in pages:
            try:
                # Create page directory if needed
                page_dir = pages_dir / page.name
                page_dir.mkdir(exist_ok=True)

                # Load page template
                template = self.jinja_env.get_template(page.template)

                # Prepare template context
                context = {
                    "config": config,
                    "page": page,
                    "components": components or [],
                    "current_page": page.name,
                    "base_url": config.base_url,
                }

                # Merge page content
                context.update(page.content)

                # Render page
                rendered = template.render(**context)

                # Write page file
                index_file = page_dir / "index.html"
                index_file.write_text(rendered, encoding="utf-8")

                self.logger.debug(f"Generated page: {page.name}")

            except Exception as e:
                self.logger.warning(f"Failed to generate page {page.name}: {e}")

    def _generate_static_assets(self, website_dir: Path, config: WebsiteConfig):
        """Generate static assets (CSS, JS, images)"""
        static_dir = website_dir / "static"
        static_dir.mkdir(exist_ok=True)

        # Copy existing static assets
        if self.static_dir.exists():
            shutil.copytree(self.static_dir, static_dir, dirs_exist_ok=True)
            self.logger.debug("Copied existing static assets")

        # Generate theme-specific assets
        self._generate_theme_assets(static_dir, config.theme)

    def _generate_theme_assets(self, static_dir: Path, theme: str):
        """Generate theme-specific CSS and JS"""
        css_dir = static_dir / "css"
        js_dir = static_dir / "js"

        css_dir.mkdir(exist_ok=True)
        js_dir.mkdir(exist_ok=True)

        # Generate theme CSS
        theme_css = self._generate_theme_css(theme)
        theme_file = css_dir / f"theme_{theme}.css"
        theme_file.write_text(theme_css, encoding="utf-8")

        # Generate theme JS
        theme_js = self._generate_theme_js(theme)
        theme_file = js_dir / f"theme_{theme}.js"
        theme_file.write_text(theme_js, encoding="utf-8")

        self.logger.debug(f"Generated theme assets for: {theme}")

    def _generate_theme_css(self, theme: str) -> str:
        """Generate theme-specific CSS"""
        if theme == "default":
            return """
/* Default Theme CSS */
:root {
    --primary-color: #3498db;
    --secondary-color: #2ecc71;
    --accent-color: #e74c3c;
    --text-color: #2c3e50;
    --background-color: #ecf0f1;
    --border-color: #bdc3c7;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--background-color);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 15px;
}

.btn {
    display: inline-block;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-primary {
    background-color: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background-color: #2980b9;
}
"""
        else:
            return f"/* {theme} theme CSS */\n/* Customize as needed */"

    def _generate_theme_js(self, theme: str) -> str:
        """Generate theme-specific JavaScript"""
        if theme == "default":
            return """
// Default Theme JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Default theme loaded');

    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');

    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
        });
    }
});
"""
        else:
            return f"// {theme} theme JavaScript\n// Customize as needed"

    def _generate_config_files(
        self,
        website_dir: Path,
        config: WebsiteConfig,
        pages: List[PageConfig],
        components: List[ComponentConfig] = None,
    ):
        """Generate configuration files for the website"""
        config_dir = website_dir / "config"
        config_dir.mkdir(exist_ok=True)

        # Generate website config
        website_config = {
            "website": asdict(config),
            "pages": [asdict(page) for page in pages],
            "components": [asdict(comp) for comp in (components or [])],
            "generated_at": str(Path.cwd()),
            "generator_version": "1.0.0",
        }

        # Save as JSON
        config_file = config_dir / "website_config.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(website_config, f, indent=2, ensure_ascii=False)

        # Save as YAML
        config_file = config_dir / "website_config.yaml"
        with open(config_file, "w", encoding="utf-8") as f:
            yaml.dump(website_config, f, default_flow_style=False, allow_unicode=True)

        self.logger.debug("Generated configuration files")

    def _generate_sitemap(
        self, website_dir: Path, config: WebsiteConfig, pages: List[PageConfig]
    ):
        """Generate XML sitemap for SEO"""
        sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{config.base_url}/</loc>
        <lastmod>{Path.cwd()}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>"""

        for page in pages:
            sitemap_content += f"""
    <url>
        <loc>{config.base_url}/{page.route}</loc>
        <lastmod>{Path.cwd()}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>"""

        sitemap_content += """
</urlset>"""

        sitemap_file = website_dir / "sitemap.xml"
        sitemap_file.write_text(sitemap_content, encoding="utf-8")

        self.logger.debug("Generated sitemap.xml")

    def generate_from_template(
        self,
        template_name: str,
        config: WebsiteConfig,
        custom_data: Dict[str, Any] = None,
    ) -> Path:
        """Generate website from a predefined template"""
        try:
            self.logger.info(f"Generating website from template: {template_name}")

            # Load template configuration
            template_config = self._load_template_config(template_name)

            # Merge custom data
            if custom_data:
                template_config.update(custom_data)

            # Generate website
            return self.generate_website(
                config=config,
                pages=template_config.get("pages", []),
                components=template_config.get("components", []),
            )

        except Exception as e:
            self.logger.error(f"Failed to generate from template {template_name}: {e}")
            raise

    def _load_template_config(self, template_name: str) -> Dict[str, Any]:
        """Load configuration for a predefined template"""
        template_file = self.templates_dir / "templates" / f"{template_name}.yaml"

        if not template_file.exists():
            raise FileNotFoundError(f"Template {template_name} not found")

        with open(template_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def create_basic_website(self, name: str, title: str, description: str) -> Path:
        """Create a basic website with minimal configuration"""
        config = WebsiteConfig(
            name=name, title=title, description=description, author="Website Generator"
        )

        pages = [
            PageConfig(
                name="home",
                title=title,
                template="base/responsive_base.html",
                route="/",
                content={"heading": title, "description": description},
            ),
            PageConfig(
                name="about",
                title=f"About - {title}",
                template="base/responsive_base.html",
                route="/about",
                content={
                    "heading": "About Us",
                    "description": "Learn more about our company",
                },
            ),
            PageConfig(
                name="contact",
                title=f"Contact - {title}",
                template="base/responsive_base.html",
                route="/contact",
                content={
                    "heading": "Contact Us",
                    "description": "Get in touch with us",
                },
            ),
        ]

        components = [
            ComponentConfig(
                name="header",
                type="header",
                template="base/responsive_base.html",
                data={"site_name": title},
            ),
            ComponentConfig(
                name="footer",
                type="footer",
                template="base/responsive_base.html",
                data={"year": "2024", "site_name": title},
            ),
        ]

        return self.generate_website(config, pages, components)


# Convenience functions
def create_website_generator(project_root: Path = None) -> WebsiteGenerator:
    """Create a new website generator instance"""
    return WebsiteGenerator(project_root)


def generate_basic_website(
    name: str, title: str, description: str, project_root: Path = None
) -> Path:
    """Generate a basic website with minimal configuration"""
    generator = create_website_generator(project_root)
    return generator.create_basic_website(name, title, description)
