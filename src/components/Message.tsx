"use client";
import { Card } from "@/components/ui/card"; // Shadcn Card

interface MessageProps {
  role: "user" | "bot";
  text: string;
}

const Message: React.FC<MessageProps> = ({ role, text }) => {
  const isUser = role === "user";

  return (
    <Card
      className={`p-4 rounded-lg max-w-[80%] ${
        isUser
          ? "ml-auto bg-blue-500 text-white dark:bg-blue-700"
          : "mr-auto bg-gray-300 text-black dark:bg-gray-800 dark:text-white"
      } shadow-md transition-transform hover:scale-[1.02]`}
    >
      {text}
    </Card>
  );
};

export default Message;