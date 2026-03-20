const form = document.getElementById("predict-form");
const resultBox = document.getElementById("result");
const predictedClassText = document.getElementById("predicted-class");
const probsBox = document.getElementById("probs");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    sepal_length: Number(document.getElementById("sepal_length").value),
    sepal_width: Number(document.getElementById("sepal_width").value),
    petal_length: Number(document.getElementById("petal_length").value),
    petal_width: Number(document.getElementById("petal_width").value),
  };

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Tahmin sirasinda hata olustu.");
    }

    predictedClassText.textContent = data.predicted_class_name;

    probsBox.innerHTML = "";
    Object.entries(data.probabilities).forEach(([className, prob]) => {
      const p = document.createElement("p");
      p.textContent = `${className}: ${(prob * 100).toFixed(2)}%`;
      probsBox.appendChild(p);
    });

    resultBox.classList.remove("hidden");
  } catch (error) {
    predictedClassText.textContent = `Hata: ${error.message}`;
    probsBox.innerHTML = "";
    resultBox.classList.remove("hidden");
  }
});
