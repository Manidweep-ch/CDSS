function PanelCard({ data }) {
  return (
    <div style={{
      border: "1px solid black",
      padding: "10px",
      margin: "10px"
    }}>
      <h4>{data.panel}</h4>

      <p><b>Final Decision:</b> {data.final_decision}</p>
      <p><b>Severity:</b> {data.severity}</p>
      <p><b>Confidence:</b> {data.confidence}</p>
      <p><b>Decision Source:</b> {data.decision_source}</p>

      <details>
        <summary>Explainability</summary>
        <pre>
          {JSON.stringify(data.ml_explainability, null, 2)}
        </pre>
      </details>
    </div>
  );
}

export default PanelCard;