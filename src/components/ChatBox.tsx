"use client";
import Message from "./Message";
import InputBox from "./InputBox";
import { ScrollArea } from "@/components/ui/scroll-area"; // Shadcn ScrollArea

interface ChatBoxProps {
  onSendMessage: (message: string) => void;
  messages: { role: "user" | "bot"; text: string }[];
}

const ChatBox: React.FC<ChatBoxProps> = ({ onSendMessage, messages }) => {
  return (
    <div className="flex flex-col h-full">
      {/* Messages Area */}
      <ScrollArea className="flex-1 p-4 space-y-4 overflow-y-auto">
        {messages.map((msg, index) => (
          <Message key={index} role={msg.role} text={msg.text} />
        ))}
      </ScrollArea>

      {/* Input Box */}
      <div className="sticky bottom-0 bg-white dark:bg-black z-50">
        <InputBox onSendMessage={onSendMessage} />
      </div>
    </div>
  );
};

export default ChatBox;