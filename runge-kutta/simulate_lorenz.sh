function clean_up() {
    if [[ -d "$TEMP_ENV_PATH" ]]; then
        echo "Cleaning up ..."
        rm -rf "$TEMP_ENV_PATH"
        echo "Done"
    fi
}

trap clean_up EXIT

TEMP_ENV_PATH="/tmp/temp_env"

clean_up

python3 -m venv "$TEMP_ENV_PATH"
source "${TEMP_ENV_PATH}/bin/activate"

echo "Installing necessary packages ... "
pip install --upgrade pip &> /dev/null
pip install -r "$(dirname ${0})"/requirements.txt &> /dev/null
echo $'Done\n'

echo "Running simulation ..."
./simulate_lorenz.py
