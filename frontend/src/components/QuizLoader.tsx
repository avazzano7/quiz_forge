import React, { useState } from "react";
import { loadQuiz } from "../api/quizApi";

export default function QuizLoader() {
  const [path, setPath] = useState("");
  const [loading, setLoading] = useState(false);
  const [quizTitle, setQuizTitle] = useState<string | null>(null);
  const [numQuestions, setNumQuestions] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleLoad = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await loadQuiz(path);
      setQuizTitle(data.title);
      setNumQuestions(data.num_questions);
    } catch (err: any) {
      setError(err.message || "Failed to load quiz");
      setQuizTitle(null);
      setNumQuestions(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Load a Quiz</h2>
      <input
        type="text"
        placeholder="Enter YAML file path"
        value={path}
        onChange={(e) => setPath(e.target.value)}
        style={{ width: "300px" }}
      />
      <button onClick={handleLoad} disabled={loading || !path}>
        {loading ? "Loading..." : "Load Quiz"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {quizTitle && (
        <div>
          <h3>Quiz Loaded:</h3>
          <p>
            <strong>Title:</strong> {quizTitle}
          </p>
          <p>
            <strong>Number of Questions:</strong> {numQuestions}
          </p>
        </div>
      )}
    </div>
  );
}
