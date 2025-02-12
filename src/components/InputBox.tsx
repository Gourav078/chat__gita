"use client";
import React from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface InputBoxProps {
  onSendMessage: (message: string) => void;
}

const InputBox: React.FC<InputBoxProps> = ({ onSendMessage }) => {
  const [input, setInput] = React.useState("");

  const handleSubmit = () => {
    if (input.trim()) {
      onSendMessage(input);
      setInput("");
    }
  };

  return (
    <div
      className="p-4 bg-gray-200 dark:bg-gray-900 border-t border-gray-300 dark:border-gray-700"
      style={{ boxShadow: "0 -4px 10px rgba(0, 0, 0, 0.1)" }}
    >
      <div className="flex items-center gap-2">
        <Input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          className="flex-1 bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-600 text-black dark:text-white placeholder:text-gray-500 dark:placeholder:text-gray-400"
        />
        <Button onClick={handleSubmit}>Send</Button>
      </div>
    </div>
  );
};

export default InputBox;