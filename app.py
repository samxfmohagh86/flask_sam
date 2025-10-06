# flask_app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)  # يسمح بالاستدعاءات من صفحات خارجية مثل coderpad

def solve_quadratic(a, b, c):
    # a, b, c are floats
    if abs(a) < 1e-12:
        # معاملة الحالة الخطية أو الثوابت
        if abs(b) < 1e-12:
            if abs(c) < 1e-12:
                return {"type": "infinite", "message": "لا نهائية من الحلول (0=0)."}
            else:
                return {"type": "none", "message": "لا يوجد حل (ثابت غير صفري)."}
        else:
            x = -c / b
            return {"type": "linear", "roots": [x], "message": f"معادلة خطية — الجذر: {x}"}
    D = b*b - 4*a*c
    if D > 0:
        sqrtD = math.sqrt(D)
        x1 = (-b + sqrtD) / (2*a)
        x2 = (-b - sqrtD) / (2*a)
        return {"type": "real_two", "roots": [x1, x2], "discriminant": D}
    elif abs(D) < 1e-12:
        x = -b / (2*a)
        return {"type": "real_one", "roots": [x], "discriminant": D}
    else:
        real = -b / (2*a)
        imag = math.sqrt(-D) / (2*a)
        r1 = {"real": real, "imag": imag}
        r2 = {"real": real, "imag": -imag}
        return {"type": "complex", "roots": [r1, r2], "discriminant": D}

@app.route("/")
def index():
    return jsonify({"message": "Flask quadratic solver is running"}), 200

# Accepts JSON POST with { "a": .., "b": .., "c": .. }
@app.route("/api/solve", methods=["POST"])
def api_solve_post():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "يرجى إرسال JSON مع الحقول a, b, c"}), 400
    try:
        a = float(data.get("a", 0))
        b = float(data.get("b", 0))
        c = float(data.get("c", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "القيم a, b, c يجب أن تكون أرقاماً"}), 400

    result = solve_quadratic(a, b, c)
    return jsonify({"input": {"a": a, "b": b, "c": c}, "result": result}), 200

# Optional: support GET for سهل التجريب
# /api/solve_get?a=1&b=2&c=3
@app.route("/api/solve_get", methods=["GET"])
def api_solve_get():
    try:
        a = float(request.args.get("a", 0))
        b = float(request.args.get("b", 0))
        c = float(request.args.get("c", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "القيم a, b, c يجب أن تكون أرقاماً"}), 400
    result = solve_quadratic(a, b, c)
    return jsonify({"input": {"a": a, "b": b, "c": c}, "result": result}), 200

if __name__ == "__main__":
    app.run(debug=True)
