python -c "import sys"
MSG=$?
if [ "$MSG" == "0" ]; then
    python stats.py
else
    echo "Worning: Python is NOT found in your system."
fi