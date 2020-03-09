PRIVACY=privacy.txt
if [ ! -f "${PRIVACY}" ]; then
	echo "file not found: ${PRIVACY}"
	exit 1
fi

# negate the output (no results = 0, results = 1)
! grep -r --exclude-dir=".git" --exclude="privacy.txt" -f "${PRIVACY}" .
