import { useState } from "react";
import axiosClient from "../api/axiosClient";

function LabInput({ activeProfile, setResults, setEvaluationId }) {
  const [formData, setFormData] = useState({});
  const [detectedPanels, setDetectedPanels] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: parseFloat(e.target.value),
    });
  };

  const detectPanels = async () => {
    setLoading(true);
    try {
      const response = await axiosClient.post("/detect", formData);
      setDetectedPanels(response.data.detected_panels);
    } catch (err) {
      alert("Detection failed");
    }
    setLoading(false);
  };

  const runEvaluation = async (panels) => {
    setLoading(true);
    try {
      const response = await axiosClient.post(
        `/evaluate/${activeProfile}`,
        {
          panels: panels,
          data: formData,
        }
      );

      setResults(response.data.results);
      setEvaluationId(response.data.evaluation_id);
    } catch (err) {
      alert("Evaluation failed");
    }
    setLoading(false);
  };

  return (
    <div style={{ marginTop: "20px" }}>
      <h3>Enter Lab Values</h3>

      <input name="fasting_glucose_level" placeholder="Fasting Glucose" onChange={handleChange}/>
      <input name="HbA1c_level" placeholder="HbA1c" onChange={handleChange}/>
      <input name="serum_creatinine" placeholder="Creatinine" onChange={handleChange}/>
      <input name="age" placeholder="Age" onChange={handleChange}/>
      <input name="sex" placeholder="Sex (1=Male,0=Female)" onChange={handleChange}/>

      <br/><br/>
      <button onClick={detectPanels}>Detect Panels</button>

      {loading && <p>Processing...</p>}

      {detectedPanels.length > 0 && (
        <div>
          <h4>Detected Panels:</h4>

          <button onClick={() => runEvaluation(detectedPanels)}>
            Analyze All
          </button>

          {detectedPanels.map((panel) => (
            <button
              key={panel}
              onClick={() => runEvaluation([panel])}
              style={{ marginLeft: "5px" }}
            >
              Analyze {panel}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default LabInput;