import React from "react";
import { ChatWindowContainer } from "../styles/components";

interface Message {
  id: number;
  text: string;
  type: "system" | "player" | "npc";
}

interface ChatWindowProps {
  messages: Message[];
}

export const ChatWindow: React.FC<ChatWindowProps> = ({ messages }) => (
  <ChatWindowContainer>
    {messages.map((message) => (
      <div key={message.id} className={`message ${message.type}`}>
        {message.text}
      </div>
    ))}
  </ChatWindowContainer>
);
