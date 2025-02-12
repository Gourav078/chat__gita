"use client";
import { useState, useEffect } from "react";
import ChatBox from "../components/ChatBox";
import { Button } from "@/components/ui/button"; 
import { Moon, Sun } from "lucide-react"; 
import { askGita } from "../utils/api";

const Page = () => {
  const [messages, setMessages] = useState<
    { role: "user" | "bot"; text: string }[]
  >([]);
  const [theme, setTheme] = useState<"light" | "dark">("light");

  useEffect(() => {
    const storedTheme = localStorage.getItem("theme") as "light" | "dark";
    if (storedTheme) {
      setTheme(storedTheme);
      document.documentElement.classList.toggle("dark", storedTheme === "dark");
    }
  }, []);

  const handleSendMessage = async (message: string) => {
    setMessages((prev) => [...prev, { role: "user", text: message }]);
    try {
      const botResponse = await askGita(message);
      setMessages((prev) => [...prev, { role: "bot", text: botResponse }]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Sorry, I encountered an error." },
      ]);
    }
  };

  const toggleTheme = () => {
    const newTheme = theme === "light" ? "dark" : "light";
    setTheme(newTheme);
    localStorage.setItem("theme", newTheme);
    document.documentElement.classList.toggle("dark", newTheme === "dark");
  };

  return (
    <div
      className={`min-h-screen transition-colors duration-300 ${
        theme === "dark" ? "bg-black text-white" : "bg-white text-black"
      }`}
    >
      {/* Header */}
      <header className="flex justify-between items-center p-4 border-b border-gray-200 dark:border-gray-800">
        <h1 className="text-3xl font-bold tracking-tight">Bhagavad Gita Chat</h1>

        <Button
          variant="outline"
          onClick={toggleTheme}
          className="flex items-center gap-2"
        >
          {theme === "light" ? (
            <>
              <Moon className="h-5 w-5" />
              <span>Dark Mode</span>
            </>
          ) : (
            <>
              <Sun className="h-5 w-5" />
              <span>Light Mode</span>
            </>
          )}
        </Button>
      </header>

      {/* Chat Box */}
      <div className="flex flex-col h-[calc(100vh-64px)]">
        <ChatBox onSendMessage={handleSendMessage} messages={messages} />
      </div>
    </div>
  );
};

export default Page;
