export const askGita = async (question: string): Promise<string> => {
  const response = await fetch("http://localhost:8000/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_question: question }),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch response from server");
  }

  const data = await response.json();
  return data.message;
};