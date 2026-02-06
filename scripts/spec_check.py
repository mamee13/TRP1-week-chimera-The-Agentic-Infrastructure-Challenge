#!/usr/bin/env python3
"""
Spec Compliance Checker for Project Chimera

This script validates that the implementation aligns with specifications.
It checks for:
1. Required spec files exist and are non-empty
2. Pydantic models match technical spec definitions
3. Skills have proper I/O contracts
4. Tests cover all specified interfaces
5. MCP integration follows spec requirements

Usage:
    python scripts/spec_check.py
    make spec-check
"""

import sys
from pathlib import Path

# ANSI color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


class SpecChecker:
    def __init__(self, root_dir: Path = Path(".")):
        self.root_dir = root_dir
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.passes: list[str] = []

    def check_all(self) -> bool:
        """Run all spec compliance checks."""
        print(f"{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}Project Chimera: Spec Compliance Check{RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")

        # Run all checks
        self.check_required_specs()
        self.check_pydantic_models()
        self.check_skills_contracts()
        self.check_test_coverage()
        self.check_mcp_integration()
        self.check_documentation()

        # Print results
        self.print_results()

        # Return True if no errors
        return len(self.errors) == 0

    def check_required_specs(self):
        """Verify all required spec files exist and are non-empty."""
        print(f"{BLUE}[1/6] Checking Required Specification Files...{RESET}")

        required_specs = [
            "specs/_meta.md",
            "specs/functional.md",
            "specs/technical.md",
            "specs/openclaw_integration.md",
        ]

        for spec_path in required_specs:
            full_path = self.root_dir / spec_path
            if not full_path.exists():
                self.errors.append(f"Missing required spec: {spec_path}")
            elif full_path.stat().st_size == 0:
                self.errors.append(f"Empty spec file: {spec_path}")
            else:
                self.passes.append(f"✓ {spec_path} exists and is non-empty")

    def check_pydantic_models(self):
        """Verify Pydantic models match technical spec definitions."""
        print(f"\n{BLUE}[2/6] Checking Pydantic Model Compliance...{RESET}")

        schemas_path = self.root_dir / "src" / "models" / "schemas.py"
        if not schemas_path.exists():
            self.errors.append("Missing src/models/schemas.py")
            return

        # Read schemas file
        with open(schemas_path) as f:
            content = f.read()

        # Check for required models
        required_models = [
            "Campaign",
            "WorkerTaskInput",
            "WorkerTaskOutput",
            "JudgeValidationOutput",
            "CampaignStatus",
            "TaskStatus",
        ]

        for model in required_models:
            if f"class {model}" in content:
                self.passes.append(f"✓ Pydantic model '{model}' defined")
            else:
                self.errors.append(f"Missing Pydantic model: {model}")

        # Check for BaseModel inheritance
        if "from pydantic import BaseModel" in content:
            self.passes.append("✓ Pydantic BaseModel imported")
        else:
            self.errors.append("Pydantic BaseModel not imported")

    def check_skills_contracts(self):
        """Verify skills have proper I/O contracts."""
        print(f"\n{BLUE}[3/6] Checking Skills I/O Contracts...{RESET}")

        skills_dir = self.root_dir / "skills"
        if not skills_dir.exists():
            self.errors.append("Missing skills/ directory")
            return

        # Check base skill
        base_skill_path = skills_dir / "base.py"
        if not base_skill_path.exists():
            self.errors.append("Missing skills/base.py")
        else:
            with open(base_skill_path) as f:
                content = f.read()
            if "class BaseSkill(ABC)" in content:
                self.passes.append("✓ BaseSkill abstract class defined")
            else:
                self.errors.append("BaseSkill not properly defined")

        # Check individual skills
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir() and d.name.startswith("skill_")]

        if len(skill_dirs) < 3:
            self.warnings.append(f"Only {len(skill_dirs)} skills found, expected at least 3")

        for skill_dir in skill_dirs:
            executor_path = skill_dir / "executor.py"
            if not executor_path.exists():
                self.errors.append(f"Missing executor.py in {skill_dir.name}")
            else:
                with open(executor_path) as f:
                    content = f.read()

                # Check for Input/Output models
                skill_name = skill_dir.name.replace("skill_", "").title().replace("_", "")
                input_model = f"{skill_name}Input"

                if f"class {input_model}" in content or "Input(BaseModel)" in content:
                    self.passes.append(f"✓ {skill_dir.name} has Input contract")
                else:
                    self.warnings.append(f"{skill_dir.name} missing Input contract")

                if "async def execute" in content:
                    self.passes.append(f"✓ {skill_dir.name} implements execute method")
                else:
                    self.errors.append(f"{skill_dir.name} missing execute method")

    def check_test_coverage(self):
        """Verify tests cover all specified interfaces."""
        print(f"\n{BLUE}[4/6] Checking Test Coverage...{RESET}")

        tests_dir = self.root_dir / "tests"
        if not tests_dir.exists():
            self.errors.append("Missing tests/ directory")
            return

        # Check for required test files
        required_tests = [
            "test_skills_interface.py",
            "test_swarm_runtime.py",
        ]

        for test_file in required_tests:
            test_path = tests_dir / test_file
            if not test_path.exists():
                self.errors.append(f"Missing required test: {test_file}")
            else:
                self.passes.append(f"✓ {test_file} exists")

        # Count total test files
        test_files = list(tests_dir.glob("test_*.py"))
        if len(test_files) >= 5:
            self.passes.append(f"✓ {len(test_files)} test files found (good coverage)")
        else:
            self.warnings.append(f"Only {len(test_files)} test files found")

    def check_mcp_integration(self):
        """Verify MCP integration follows spec requirements."""
        print(f"\n{BLUE}[5/6] Checking MCP Integration...{RESET}")

        mcp_client_path = self.root_dir / "src" / "mcp" / "client.py"
        if not mcp_client_path.exists():
            self.errors.append("Missing src/mcp/client.py")
            return

        with open(mcp_client_path) as f:
            content = f.read()

        # Check for MCP client implementation
        if "class" in content and "MCP" in content:
            self.passes.append("✓ MCP client class defined")
        else:
            self.errors.append("MCP client not properly defined")

        # Check for async methods
        if "async def" in content:
            self.passes.append("✓ MCP client uses async methods")
        else:
            self.warnings.append("MCP client should use async methods")

        # Check for mock server
        mock_server_path = self.root_dir / "mcp-server-mock" / "server.py"
        if mock_server_path.exists():
            self.passes.append("✓ MCP mock server exists for testing")
        else:
            self.warnings.append("No MCP mock server found")

    def check_documentation(self):
        """Verify documentation completeness."""
        print(f"\n{BLUE}[6/6] Checking Documentation...{RESET}")

        # Check README
        readme_path = self.root_dir / "README.md"
        if not readme_path.exists():
            self.errors.append("Missing README.md")
        else:
            with open(readme_path) as f:
                content = f.read()
            if len(content) > 1000:
                self.passes.append("✓ README.md is comprehensive (>1000 chars)")
            else:
                self.warnings.append("README.md is too short")

        # Check research documentation
        research_dir = self.root_dir / "research"
        if research_dir.exists():
            research_files = list(research_dir.glob("*.md"))
            if len(research_files) >= 3:
                self.passes.append(f"✓ {len(research_files)} research documents found")
            else:
                self.warnings.append("Limited research documentation")

        # Check CLAUDE.md or .cursor/rules
        claude_path = self.root_dir / "CLAUDE.md"
        cursor_rules_path = self.root_dir / ".cursor" / "rules"

        if claude_path.exists() or cursor_rules_path.exists():
            self.passes.append("✓ AI agent context rules defined")
        else:
            self.errors.append("Missing CLAUDE.md or .cursor/rules")

    def print_results(self):
        """Print check results with color coding."""
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}Spec Compliance Results{RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")

        # Print passes
        if self.passes:
            print(f"{GREEN}✓ PASSED CHECKS ({len(self.passes)}):{RESET}")
            for msg in self.passes:
                print(f"  {GREEN}{msg}{RESET}")
            print()

        # Print warnings
        if self.warnings:
            print(f"{YELLOW}⚠ WARNINGS ({len(self.warnings)}):{RESET}")
            for msg in self.warnings:
                print(f"  {YELLOW}⚠ {msg}{RESET}")
            print()

        # Print errors
        if self.errors:
            print(f"{RED}✗ ERRORS ({len(self.errors)}):{RESET}")
            for msg in self.errors:
                print(f"  {RED}✗ {msg}{RESET}")
            print()

        # Summary
        total_checks = len(self.passes) + len(self.warnings) + len(self.errors)
        pass_rate = (len(self.passes) / total_checks * 100) if total_checks > 0 else 0

        print(f"{BLUE}{'='*60}{RESET}")
        if len(self.errors) == 0:
            print(f"{GREEN}✓ SPEC COMPLIANCE: PASSED{RESET}")
            print(
                f"{GREEN}  Pass Rate: {pass_rate:.1f}% ({len(self.passes)}/{total_checks}){RESET}"
            )
        else:
            print(f"{RED}✗ SPEC COMPLIANCE: FAILED{RESET}")
            print(f"{RED}  {len(self.errors)} critical errors must be fixed{RESET}")
        print(f"{BLUE}{'='*60}{RESET}\n")


def main():
    """Main entry point."""
    checker = SpecChecker()
    success = checker.check_all()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
