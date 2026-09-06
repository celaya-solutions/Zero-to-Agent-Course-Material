#!/usr/bin/env ruby
# Compatibility entry point for existing course maintenance commands.
require "rbconfig"
root = File.expand_path("..", __dir__)
python = File.join(root, ".venv", RbConfig::CONFIG["host_os"].match?(/mswin|mingw/) ? "Scripts/python.exe" : "bin/python")
abort "Run uv sync --frozen at the course root first" unless File.executable?(python)
exec python, File.join(root, "scripts/build_pdfs.py")
