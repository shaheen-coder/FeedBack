#!/usr/bin/env bashc
# Detect the operating system
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)

# Setup virtual environment
setup() {
    echo "Setting up virtual environment..."
    if [ "$OS" == "linux" ]; then
        python3 -m venv venv
        source venv/bin/activate
    elif [ "$OS" == "windows" ]; then
        python -m venv venv
        .\venv\Scripts\activate
    fi
    echo "Virtual environment created and activated"
}

# Deactivate virtual environment
deactivate_env() {
    echo "Deactivating virtual environment..."
    if [ "$VIRTUAL_ENV" ]; then
        deactivate
        echo "Virtual environment deactivated"
    else
        echo "No virtual environment is currently active"
    fi
}

# Install packages from requirements.txt
install() {
    echo "Installing packages from requirements.txt..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        echo "Packages installed successfully"
    else
        echo "Error: requirements.txt not found"
        exit 1
    fi
}

# Run Django server
run() {
    echo "Starting Django server..."
    if [ -f "manage.py" ]; then
        python manage.py runserver
    else
        echo "Error: manage.py not found"
        exit 1
    fi
}

# Main script logic
case "$1" in
    "setup")
        setup
        ;;
    "install")
        install
        ;;
    "run")
        run
        ;;
    "deactivate")
        deactivate_env
        ;;
    *)
        echo "FeedBack system Project Manager"
        echo "Usage:"
        echo "  ./run.sh setup       - Setup virtual environment"
        echo "  ./run.sh install     - Install packages from requirements.txt"
        echo "  ./run.sh run         - Run development server"
        echo "  ./run.sh deactivate  - Deactivate virtual environment"
        ;;
esac
