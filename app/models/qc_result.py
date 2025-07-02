#!/usr/bin/env python3
"""
QC Result model for storing check results with enhanced violation tracking
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class ViolationType(Enum):
    """Types of QC violations"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    SUCCESS = "success"

@dataclass
class ViolationLocation:
    """Location information for a violation"""
    element_type: str  # paragraph, table, cell, etc.
    element_index: Optional[int] = None
    text_preview: Optional[str] = None
    line_number: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "element_type": self.element_type,
            "element_index": self.element_index,
            "text_preview": self.text_preview,
            "line_number": self.line_number
        }

@dataclass
class QCResult:
    """Container for QC check results with enhanced violation tracking"""
    rule_name: str
    passed: bool
    message: str
    violation_type: ViolationType = ViolationType.ERROR
    details: Optional[str] = None
    locations: Optional[List[ViolationLocation]] = None
    rule_number: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "rule_name": self.rule_name,
            "rule_number": self.rule_number,
            "passed": self.passed,
            "message": self.message,
            "violation_type": self.violation_type.value,
            "details": self.details,
            "locations": [loc.to_dict() for loc in (self.locations or [])]
        }

@dataclass
class QCReport:
    """Complete QC report with enhanced summary and statistics"""
    document_path: str
    timestamp: datetime
    results: list[QCResult]
    
    def get_summary(self) -> Dict[str, Any]:
        """Get enhanced summary statistics"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        errors = sum(1 for r in self.results if not r.passed and r.violation_type == ViolationType.ERROR)
        warnings = sum(1 for r in self.results if not r.passed and r.violation_type == ViolationType.WARNING)
        info = sum(1 for r in self.results if not r.passed and r.violation_type == ViolationType.INFO)
        
        return {
            "total_checks": total,
            "passed_checks": passed,
            "failed_checks": total - passed,
            "errors": errors,
            "warnings": warnings,
            "info": info,
            "success_rate": round((passed / total) * 100, 2) if total > 0 else 0,
            "overall_status": "PASS" if passed == total else "FAIL",
            "severity": "ERROR" if errors > 0 else "WARNING" if warnings > 0 else "INFO" if info > 0 else "SUCCESS"
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "document_path": self.document_path,
            "timestamp": self.timestamp.isoformat(),
            "summary": self.get_summary(),
            "checks": [result.to_dict() for result in self.results]
        } 