# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Cygnet is a small C compiler implementation in Python, developed by following the book "Writing A C Compiler" by Nora Sandler. This is an educational compiler project in its early stages.

## Architecture

**CLI Framework**: Uses Typer for command-line interface management. The main entry point is defined in `src/cygnet/main.py` with the `app` object, which is registered as the `cygnet` console script in `pyproject.toml`.

**Project Structure**:
- `src/cygnet/` - Main compiler source code
  - `main.py` - CLI application with Typer commands
  - `__init__.py` - Package initialization (currently empty)
- `tests/` - Test directory (currently empty)

**Current Commands**:
- `cygnet clitest` - Test command to verify CLI functionality
- `cygnet build` - Placeholder for compiler build command (not yet implemented)
- `cygnet --version` / `cygnet -v` - Display version information

## Development Setup

**Environment**: Python 3.10+ required. Uses a virtual environment (`.venv/`).

**Installation**:
```bash
# Install in editable mode for development
pip install -e .
```

**Running the CLI**:
```bash
# After installation, the cygnet command is available
cygnet clitest
cygnet --version

# Or run directly without installation
python -m cygnet.main
```

## Dependencies

- `typer>=0.12` - CLI framework for building command-line applications
- Standard library: `importlib.metadata` for version information

## Build System

Uses setuptools with PEP 517 configuration in `pyproject.toml`:
- Package located in `src/` directory
- Entry point: `cygnet = "cygnet.main:app"`
- Build requires: `setuptools>=75`, `wheel`

## Testing

The `tests/` directory exists but currently contains no test files. As compiler features are implemented following the book, tests should be added here.

## Key Implementation Notes

This project follows the structure and approach from "Writing A C Compiler" by Nora Sandler. The compiler implementation will be built incrementally, adding lexer, parser, semantic analysis, and code generation phases as the book progresses.

The `build` command in `main.py` is currently a placeholder for the main compiler pipeline that will be implemented.

## Claude Code Assistance Guidance

This section describes how Claude Code should assist the developer with this project:
- At no point should Claude either create source code or other files or amend existing files unless explicitly requested by the developer
- The intended methodology is for Claude to help direct the development but not write any of the code
- The developer will ask questions about how best to approach a design, options for design decisions and so on. Claude should respond with suggestions and recommendations and explain benefits of each.
- Keep options in responses to a reasonable limit, ideally 2 max 3
- Be very succinct, no unnecessary language--the Emacs UI that I use does not have much space, so critical to keep responses compressed
- Assume that any prompt asking "how's that", or "is this right now", "what do I do from here" or similar phrasing means I have updated files and you need to reread latest versions before responding
