from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Task TABLE Configuration
class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    date: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)

    def to_dict(self):
        # LOOPS INTO EACH COLUMN OF THE DB OR DATA RECORDS - METHOD 1
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

        # LOOPS INTO EACH COLUMN OF THE DB OR DATA RECORDS - METHOD 2 (DICTIONARY COMPREHENSION)
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        map_url = request.form.get("map_url")
        img_url = request.form.get("img_url")
        location = request.form.get("loc")
        has_sockets = bool(request.form.get("sockets"))
        has_toilet = bool(request.form.get("toilet"))
        has_wifi = bool(request.form.get("wifi"))
        can_take_calls = bool(request.form.get("calls"))
        seats = request.form.get("seats")
        coffee_price = request.form.get("coffee_price")

        # Verifies that the name is not empty
        if not name:
            return jsonify(error="Name is required."), 400

        # Create a new Task object
        new_cafe = Task(
            name=name,
            map_url=map_url,
            img_url=img_url,
            location=location,
            has_sockets=has_sockets,
            has_toilet=has_toilet,
            has_wifi=has_wifi,
            can_take_calls=can_take_calls,
            seats=seats,
            coffee_price=coffee_price,
        )

        # Aggiungi il nuovo cafe al database
        try:
            db.session.add(new_cafe)
            db.session.commit()
            return jsonify(success="Successfully added the new cafe.")
        except Exception as e:
            db.session.rollback()
            return jsonify(error=f"Failed to add the new cafe: {str(e)}"), 500
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)