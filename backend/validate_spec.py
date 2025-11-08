#!/usr/bin/env python3
"""
Utility script to validate project specification files.
"""

import sys
import argparse
from pathlib import Path

from spec_schema import ProjectSpec


def validate_spec(spec_path: str, verbose: bool = False) -> bool:
    """
    Validate a project specification file.
    
    Args:
        spec_path: Path to spec JSON file
        verbose: Whether to print detailed output
        
    Returns:
        True if valid, False otherwise
    """
    spec_file = Path(spec_path)
    
    if not spec_file.exists():
        print(f"✗ File not found: {spec_path}")
        return False
    
    try:
        # Load and validate
        spec = ProjectSpec.from_json_file(str(spec_file))
        
        print(f"✓ Spec is valid: {spec.project_name}")
        
        if verbose:
            print(f"\n  Project: {spec.project_name}")
            print(f"  Description: {spec.description[:80]}...")
            print(f"  Tech Stack: {', '.join(spec.tech_stack[:5])}")
            print(f"  APIs: {len(spec.apis)}")
            print(f"  Modules: {len(spec.modules)}")
            print(f"  Env Vars: {len(spec.env_variables)}")
            print(f"  Deployments: {len(spec.deployment)}")
            print(f"  FAQs: {len(spec.faq)}")
        
        # Run additional validation
        warnings = spec.validate_spec()
        
        if warnings:
            print(f"\n⚠ Validation warnings ({len(warnings)}):")
            for warning in warnings:
                print(f"  - {warning}")
            print()
        else:
            print("✓ No validation warnings\n")
        
        return True
        
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return False


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate project specification JSON files"
    )
    
    parser.add_argument(
        "spec",
        nargs="+",
        help="One or more spec files to validate"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print detailed information"
    )
    
    args = parser.parse_args()
    
    all_valid = True
    
    for spec_path in args.spec:
        if len(args.spec) > 1:
            print(f"\nValidating {spec_path}...")
            print("-" * 60)
        
        valid = validate_spec(spec_path, args.verbose)
        all_valid = all_valid and valid
        
        if len(args.spec) > 1:
            print()
    
    if not all_valid:
        sys.exit(1)


if __name__ == "__main__":
    main()
