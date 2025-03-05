import React, { useState, useEffect } from "react";
import { Header } from "./components/Header";
import { ChatWindow } from "./components/ChatWindow";
import { StatusPanel } from "./components/StatusPanel";
import { CommandInput } from "./components/CommandInput";
import { AppContainer, MainContent } from "./styles/components";
import { useWebSocket } from "./contexts/WebSocketContext";

const initialCharacter = {
  name: "Adventurer",
  stats: {
    hp: 100,
    maxHp: 100,
    gold: 50,
    xp: 0,
  },
  inventory: ["Sword", "Health Potion", "Torch"],
};

const App: React.FC = () => {
  const { sendMessage, lastMessage } = useWebSocket();
  const [messages, setMessages] = useState([
    { id: 1, text: "Welcome to your adventure...", type: "system" as const },
  ]);
  const [character, setCharacter] = useState(initialCharacter);

  useEffect(() => {
    if (lastMessage) {
      try {
        const data = JSON.parse(lastMessage);
        if (data.type === "gameState") {
          setCharacter(data.character);
        } else if (data.type === "message") {
          setMessages((prev) => [
            ...prev,
            { id: Date.now(), text: data.text, type: data.messageType },
          ]);
        }
      } catch (error) {
        console.error("Error parsing message:", error);
      }
    }
  }, [lastMessage]);

  const handleCommand = (command: string) => {
    sendMessage(JSON.stringify({ type: "command", command }));
    // setMessages((prev) => [
    //   ...prev,
    //   { id: Date.now(), text: `> ${command}`, type: "player" as const },
    // ]);
  };

  return (
    <AppContainer>
      <Header
        characterName={character.name}
        health={character.stats.hp}
        maxHealth={character.stats.maxHp}
      />
      <MainContent>
        <ChatWindow messages={messages} />
        <StatusPanel character={character} />
      </MainContent>
      <CommandInput onSendCommand={handleCommand} />
    </AppContainer>
  );
};

export default App;
