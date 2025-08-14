# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### ComfyUI (Main Project)
```bash
# Start ComfyUI server
python main.py

# Run with CPU only (if no GPU)
python main.py --cpu

# Run with specific arguments
python main.py --preview-method auto --output-directory /path/to/output

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest
pytest -m "not inference"  # Skip inference tests
pytest -m "not execution"  # Skip execution tests
pytest tests-unit/  # Run unit tests only

# Lint code
ruff check .

# Development with latest frontend
python main.py --front-end-version Comfy-Org/ComfyUI_frontend@latest
```

### Other Projects
```bash
# Web projects (scholis, sonar, etc.)
cd Development/web/<project-name>
pip install -r requirements.txt
python app.py  # or python main.py

# Flask applications
cd Development/web/<project-name>/flask_app
pip install -r requirements.txt
python app.py
```

## Architecture Overview

### ComfyUI Core Architecture

ComfyUI is a node-based visual AI workflow system with the following key components:

**Entry Points:**
- `main.py` - Primary application entry point, handles CLI args and server startup
- `server.py` - Web server implementation using aiohttp, handles API routes and WebSocket connections

**Core Systems:**
- `execution.py` - Workflow execution engine with caching and progress tracking
- `nodes.py` - Base node definitions and core node types (CLIPTextEncode, samplers, etc.)
- `folder_paths.py` - Model file discovery and path management system

**Model Management:**
- `comfy/` - Core AI model implementations, samplers, and utilities
  - `comfy/model_management.py` - GPU memory management and model loading
  - `comfy/sd.py` - Stable Diffusion model implementations
  - `comfy/samplers.py` - Various sampling algorithms
  - `comfy/ldm/` - Large diffusion model architectures (Flux, SD3, SDXL, etc.)

**Execution System:**
- `comfy_execution/` - Modern execution framework
  - `graph.py` - Workflow graph representation and validation
  - `caching.py` - Hierarchical caching system for execution optimization
  - `progress.py` - Progress tracking and reporting

**Application Layer:**
- `app/` - Application services and management
  - `user_manager.py` - User session and authentication
  - `model_manager.py` - Model file management and organization
  - `frontend_management.py` - Frontend version and asset management

**API Integration:**
- `comfy_api_nodes/` - External API integrations (OpenAI, Stability, etc.)

### Key Design Patterns

**Node System:** All AI operations are implemented as nodes with standardized INPUT_TYPES/RETURN_TYPES interfaces. Each node class defines its inputs, outputs, and processing function.

**Caching:** Sophisticated multi-level caching system prevents re-execution of unchanged workflow segments. Uses dependency tracking and cache invalidation.

**Model Loading:** Dynamic model loading with memory management. Models are loaded on-demand and cached based on available GPU memory.

**Execution Graph:** Workflows are represented as directed graphs. Only changed portions are re-executed between runs.

## Model and File Organization

Models are organized in `models/` directory with specific subdirectories:
- `checkpoints/` - Main model files (.ckpt, .safetensors)
- `vae/` - VAE models
- `loras/` - LoRA adapters  
- `controlnet/` - ControlNet models
- `clip_vision/` - CLIP vision encoders
- `upscale_models/` - Super-resolution models

Configuration via `extra_model_paths.yaml` to share models between UIs.

## Custom Nodes

Custom functionality via `custom_nodes/` directory. Each custom node package can extend the base node system with new operations and model integrations.

## Frontend Architecture

Modern Vue.js/TypeScript frontend in separate repository, compiled to `web/` directory. Supports both stable releases and daily development builds via `--front-end-version` flag.

## Testing Strategy

- `tests/` - Integration tests requiring models and inference
- `tests-unit/` - Fast unit tests without model dependencies  
- `pytest.ini` configured with markers to selectively run test categories
- Tests are marked as `inference` or `execution` for selective execution

## Development Notes

- Python 3.12 recommended, 3.13 supported but some custom nodes may not be compatible
- Supports multiple GPU backends: NVIDIA CUDA, AMD ROCm, Intel XPU, Apple Metal
- CPU fallback available for development without GPU
- Memory management is critical due to large model sizes
- WebSocket-based real-time communication for progress and results