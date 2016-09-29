python -c "import sys"
MSG=$?
if [ "$MSG" == "0" ]; then
    python test_stats.py  ./tests/test_hosts.txt ./tests/test_instances.txt
else
    echo "Worning: Python is NOT found in your system."
fi