#!/usr/bin/env python3

from app import create_app

# Cria a instância da aplicação Flask
app = create_app()

if __name__ == '__main__':
    # Inicia o servidor Flask
    app.run(debug=True, port=5000, host='0.0.0.0')
