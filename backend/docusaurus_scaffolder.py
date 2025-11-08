"""
Docusaurus site scaffolding and configuration.
Initializes and configures a Docusaurus classic site.
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Optional


class DocusaurusScaffolder:
    """Handles Docusaurus site creation and configuration."""
    
    def __init__(self, site_dir: str):
        """
        Initialize scaffolder.
        
        Args:
            site_dir: Absolute path to site directory
        """
        self.site_dir = Path(site_dir)
        self.docs_dir = self.site_dir / "docs"
        self.config_file = self.site_dir / "docusaurus.config.js"
        self.sidebar_file = self.site_dir / "sidebars.js"
        self.package_file = self.site_dir / "package.json"
    
    def scaffold_site(self, project_name: str, force: bool = False) -> None:
        """
        Create a new Docusaurus site or reconfigure existing one.
        
        Args:
            project_name: Name of the project
            force: Whether to overwrite existing site
        """
        if self.site_dir.exists() and not force:
            print(f"Site directory {self.site_dir} already exists, reconfiguring...")
            self._configure_existing_site(project_name)
        else:
            print(f"Creating new Docusaurus site at {self.site_dir}...")
            self._create_new_site(project_name)
        
        # Ensure docs directory exists
        self.docs_dir.mkdir(parents=True, exist_ok=True)
    
    def _create_new_site(self, project_name: str) -> None:
        """Create a new Docusaurus site from scratch."""
        # Use npx to create Docusaurus site
        cmd = [
            "npx",
            "create-docusaurus@latest",
            str(self.site_dir),
            "classic",
            "--skip-install"
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✓ Created Docusaurus site at {self.site_dir}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to create Docusaurus site: {e.stderr}")
        
        # Configure the site
        self._configure_site(project_name)
        
        # Install dependencies
        self._install_dependencies()
    
    def _configure_existing_site(self, project_name: str) -> None:
        """Reconfigure an existing Docusaurus site."""
        if not self.config_file.exists():
            raise RuntimeError(f"Not a valid Docusaurus site: {self.site_dir}")
        
        self._configure_site(project_name)
    
    def _configure_site(self, project_name: str) -> None:
        """
        Configure Docusaurus for docs-only mode with docs as homepage.
        
        Args:
            project_name: Project name for site title
        """
        config_content = f"""// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

/** @type {{import('@docusaurus/types').Config}} */
const config = {{
  title: '{project_name}',
  tagline: 'Documentation',
  favicon: 'img/favicon.ico',

  url: 'https://your-docusaurus-site.example.com',
  baseUrl: '/',

  organizationName: 'your-org',
  projectName: '{project_name.lower().replace(" ", "-")}',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {{
    defaultLocale: 'en',
    locales: ['en'],
  }},

  presets: [
    [
      'classic',
      /** @type {{import('@docusaurus/preset-classic').Options}} */
      ({{
        docs: {{
          routeBasePath: '/', // Docs-only mode, docs at root
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: undefined,
        }},
        blog: false, // Disable blog
        theme: {{
          customCss: require.resolve('./src/css/custom.css'),
        }},
      }}),
    ],
  ],

  themeConfig:
    /** @type {{import('@docusaurus/preset-classic').ThemeConfig}} */
    ({{
      navbar: {{
        title: '{project_name}',
        logo: {{
          alt: '{project_name} Logo',
          src: 'img/logo.svg',
        }},
        items: [
          {{
            type: 'doc',
            docId: 'index',
            position: 'left',
            label: 'Docs',
          }},
        ],
      }},
      footer: {{
        style: 'dark',
        links: [],
        copyright: `Copyright © ${{new Date().getFullYear()}} {project_name}. Built with Docusaurus.`,
      }},
      prism: {{
        theme: require('prism-react-renderer/themes/github'),
        darkTheme: require('prism-react-renderer/themes/dracula'),
      }},
    }}),
}};

module.exports = config;
"""
        
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        print(f"✓ Configured Docusaurus site for '{project_name}'")
    
    def _install_dependencies(self) -> None:
        """Install npm dependencies."""
        print("Installing dependencies (this may take a minute)...")
        
        try:
            subprocess.run(
                ["npm", "install"],
                cwd=str(self.site_dir),
                check=True,
                capture_output=True,
                text=True
            )
            print("✓ Dependencies installed")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to install dependencies: {e.stderr}")
    
    def ensure_dependencies(self) -> None:
        """Ensure dependencies are installed."""
        node_modules = self.site_dir / "node_modules"
        
        if not node_modules.exists():
            self._install_dependencies()
    
    def build_site(self) -> Path:
        """
        Build the static site.
        
        Returns:
            Path to the build directory
        """
        print("Building static site...")
        
        try:
            result = subprocess.run(
                ["npm", "run", "build"],
                cwd=str(self.site_dir),
                check=True,
                capture_output=True,
                text=True
            )
            
            build_dir = self.site_dir / "build"
            if not build_dir.exists():
                raise RuntimeError("Build directory not created")
            
            print(f"✓ Site built successfully at {build_dir}")
            return build_dir
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Build failed: {e.stderr}")
    
    def start_dev_server(self) -> subprocess.Popen:
        """
        Start the Docusaurus development server.
        
        Returns:
            Process handle
        """
        print("Starting development server...")
        
        proc = subprocess.Popen(
            ["npm", "run", "start"],
            cwd=str(self.site_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("✓ Dev server started (http://localhost:3000)")
        return proc
    
    def create_directory_structure(self, sections: list[str]) -> None:
        """
        Create directory structure for documentation sections.
        
        Args:
            sections: List of section names
        """
        for section in sections:
            section_dir = self.docs_dir / section
            section_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"✓ Created {len(sections)} section directories")
    
    def clear_default_docs(self) -> None:
        """Remove default Docusaurus documentation."""
        if self.docs_dir.exists():
            import shutil
            
            # Remove all files and subdirectories in docs/
            for item in self.docs_dir.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            
            print("✓ Cleared default documentation")
    
    def validate_site(self) -> bool:
        """
        Validate that the site structure is correct.
        
        Returns:
            True if valid, False otherwise
        """
        required_files = [
            self.config_file,
            self.sidebar_file,
            self.package_file
        ]
        
        for file_path in required_files:
            if not file_path.exists():
                print(f"✗ Missing required file: {file_path}")
                return False
        
        if not self.docs_dir.exists():
            print(f"✗ Missing docs directory: {self.docs_dir}")
            return False
        
        print("✓ Site structure is valid")
        return True
