#!/bin/bash
echo "Building ZenCal for Linux..."

# Build single executable
pyinstaller zencal.py \
    --name=ZenCal \
    --onefile \
    --add-data="core:core" \
    --add-data="ui:ui" \
    --hidden-import=pystray \
    --hidden-import=PIL

echo ""
echo "============================================================"
echo "✓ Build complete!"
echo "============================================================"
echo ""
echo "Executable: dist/ZenCal"
echo ""
echo "Usage:"
echo "  ./ZenCal              → Launch overlay (runs in background)"
echo "  ./ZenCal --manager    → Launch manager GUI"
echo "  ./ZenCal --verbose    → Launch overlay with logs"
echo "============================================================"
