const API_BASE = "http://localhost:8000";

export interface LoadQuizResponse {
  title: string;
  num_questions: number;
}

export interface Question {
  id: number;
  question: string;
  choices: string[];
}

export async function loadQuiz(path: string): Promise<LoadQuizResponse> {
  const res = await fetch(`${API_BASE}/quiz/load`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ path }),
  });

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
}

export async function getQuestion(index: number): Promise<Question> {
  const res = await fetch(`${API_BASE}/quiz/question/${index}`);

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
}

export async function submitAnswer(
  questionId: number,
  choiceIndex: number
): Promise<{ correct: boolean }> {
  const res = await fetch(`${API_BASE}/quiz/answer`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question_id: questionId,
      choice_index: choiceIndex,
    }),
  });

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
}

export async function getScore(): Promise<{ score: number; total: number }> {
  const res = await fetch(`${API_BASE}/quiz/score`);

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
}
