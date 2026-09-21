from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
import os, csv, io

app = Flask(__name__)

REPORT_FOLDER = "reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        farmer_name = request.form.get("farmer_name", "")
        farm_name = request.form.get("farm_name", "")
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")
        crop = request.form.get("crop", "")
        farm_area = float(request.form.get("farm_area", 0))
        moisture = float(request.form.get("moisture", 0))
        nitrogen = float(request.form.get("nitrogen", 0))
        phosphorus = float(request.form.get("phosphorus", 0))
        potassium = float(request.form.get("potassium", 0))
        temperature = float(request.form.get("temperature", 0))
        humidity = float(request.form.get("humidity", 0))

        moisture_status = "Low" if moisture < 30 else "Normal" if moisture <= 70 else "High"
        n_status = "Low" if nitrogen < 40 else "Normal" if nitrogen <= 80 else "High"
        p_status = "Low" if phosphorus < 30 else "Normal" if phosphorus <= 70 else "High"
        k_status = "Low" if potassium < 30 else "Normal" if potassium <= 80 else "High"
        temp_status = "Low" if temperature < 20 else "Suitable" if temperature <= 35 else "High"
        humidity_status = "Low" if humidity < 40 else "Normal" if humidity <= 80 else "High"

        low = []
        if nitrogen < 40: low.append("Nitrogen")
        if phosphorus < 30: low.append("Phosphorus")
        if potassium < 30: low.append("Potassium")

        if not low:
            fertilizer = "No major N/P/K deficiency detected"
            quantity = "No additional fertilizer recommended from this prototype analysis"
            timing = "Continue monitoring and follow crop-specific soil-test guidance"
            explanation = "The entered N, P and K values are within the prototype normal ranges."
        elif len(low) == 1:
            nutrient = low[0]
            fertilizer = f"{nutrient}-focused fertilizer"
            quantity = f"Calculate crop-specific dose for {farm_area:g} area using a qualified agronomic recommendation"
            timing = "Apply at the crop-appropriate growth stage after confirming the soil test"
            explanation = f"{nutrient} is below the prototype threshold, so the system flags it for attention."
        else:
            fertilizer = "Balanced NPK fertilizer"
            quantity = f"Calculate crop-specific dose for {farm_area:g} area using a qualified agronomic recommendation"
            timing = "Apply at the crop-appropriate growth stage after confirming the soil test"
            explanation = "More than one nutrient is below the prototype threshold."

        now = datetime.now().strftime("%d-%m-%Y %I:%M %p")

        return jsonify({
            "farmer": {"name": farmer_name, "farm": farm_name, "email": email, "phone": phone},
            "crop": crop, "farm_area": farm_area,
            "values": {
                "moisture": moisture, "nitrogen": nitrogen, "phosphorus": phosphorus,
                "potassium": potassium, "temperature": temperature, "humidity": humidity
            },
            "status": {
                "moisture": moisture_status, "nitrogen": n_status, "phosphorus": p_status,
                "potassium": k_status, "temperature": temp_status, "humidity": humidity_status
            },
            "recommendation": {
                "fertilizer": fertilizer, "quantity": quantity,
                "timing": timing, "explanation": explanation
            },
            "datetime": now
        })
    except (ValueError, TypeError):
        return jsonify({"error": "Please enter valid numeric values."}), 400

@app.route("/download-report", methods=["POST"])
def download_report():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No report data received."}), 400

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"smart_fertilizer_report_{stamp}.txt"
    path = os.path.join(REPORT_FOLDER, filename)

    farmer = data.get("farmer", {})
    values = data.get("values", {})
    status = data.get("status", {})
    rec = data.get("recommendation", {})

    report = f"""SMART FERTILIZER MANAGEMENT SYSTEM
=====================================

FARMER DETAILS
--------------
Farmer Name : {farmer.get('name','')}
Farm Name   : {farmer.get('farm','')}
Email       : {farmer.get('email','')}
Phone       : {farmer.get('phone','')}
Crop        : {data.get('crop','')}
Farm Area   : {data.get('farm_area','')}

SENSOR VALUES
-------------
Soil Moisture : {values.get('moisture','')} %
Nitrogen      : {values.get('nitrogen','')}
Phosphorus    : {values.get('phosphorus','')}
Potassium     : {values.get('potassium','')}
Temperature   : {values.get('temperature','')} °C
Humidity      : {values.get('humidity','')} %

ANALYSIS
--------
Moisture    : {status.get('moisture','')}
Nitrogen    : {status.get('nitrogen','')}
Phosphorus  : {status.get('phosphorus','')}
Potassium   : {status.get('potassium','')}
Temperature : {status.get('temperature','')}
Humidity    : {status.get('humidity','')}

FERTILIZER RECOMMENDATION
-------------------------
Recommended Fertilizer : {rec.get('fertilizer','')}
Recommended Quantity   : {rec.get('quantity','')}
Application Timing     : {rec.get('timing','')}
Explanation            : {rec.get('explanation','')}

Date & Time : {data.get('datetime','')}
"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(report)

    return send_file(path, as_attachment=True, download_name=filename, mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True)
