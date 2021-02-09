from app import app, ENV

if __name__ == '__main__':
    app.run(debug=(ENV=='dev'))