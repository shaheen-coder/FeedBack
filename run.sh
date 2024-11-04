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
    *)
        echo "FeedBack system Project Manager"
        echo "Usage:"
        echo "  ./manage.sh setup   - Setup virtual environment"
        echo "  ./manage.sh install - Install packages from requirements.txt"
        echo "  ./manage.sh run     - Run development server"
        ;;
esac
