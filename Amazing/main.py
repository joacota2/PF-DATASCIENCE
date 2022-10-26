from front import app
import waitress

if __name__ == "__main__":
    # app.run(debug=True, port=5000)
    waitress.serve(app, listen="0.0.0.0:5000")
