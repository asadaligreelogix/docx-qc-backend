#!/usr/bin/env python3
"""
CLI script for DOCX Quality Control Checker
"""

import sys
import os
import json
from app.services.docx_checker import DocxChecker
from app.config import Config

def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python cli.py <path_to_docx_file> [--json]")
        sys.exit(1)
    
    docx_path = sys.argv[1]
    output_json = "--json" in sys.argv
    
    if not os.path.exists(docx_path):
        print(f"Error: File '{docx_path}' not found.")
        sys.exit(1)
    
    if not docx_path.lower().endswith('.docx'):
        print("Error: File must be a .docx file.")
        sys.exit(1)
    
    # Run checks
    config = Config()
    checker = DocxChecker(docx_path, config)
    report = checker.run_all_checks()
    
    if output_json:
        # Output JSON format
        print(json.dumps(report.to_dict(), indent=2))
    else:
        # Output human-readable format
        print_results(report)
    
    # Exit with appropriate code
    passed = sum(1 for r in report.results if r.passed)
    total = len(report.results)
    
    if passed == total:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

def print_results(report):
    """Print formatted results"""
    print("\n" + "="*60)
    print("DOCX QUALITY CONTROL CHECK RESULTS")
    print("="*60)
    
    passed = sum(1 for r in report.results if r.passed)
    total = len(report.results)
    
    print(f"\nOverall: {passed}/{total} checks passed\n")
    
    for i, result in enumerate(report.results, 1):
        status = "✓ PASS" if result.passed else "✗ FAIL"
        print(f"{i:2d}. {status} - {result.rule_name}")
        print(f"    {result.message}")
        if result.details:
            print(f"    Details: {result.details}")
        print()
    
    # Summary
    if passed == total:
        print("🎉 All QC checks passed! Document meets all requirements.")
    else:
        print(f"⚠️  {total - passed} issues found. Please review and fix the failed checks.")

if __name__ == "__main__":
    main() 