import React, { useState } from "react";
import { InputArea, StyledInput, StyledButton } from "../styles/components";

interface CommandInputProps {
  onSendCommand: (command: string) => void;
}

export const CommandInput: React.FC<CommandInputProps> = ({
  onSendCommand,
}) => {
  const [command, setCommand] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (command.trim()) {
      onSendCommand(command);
      setCommand("");
    }
  };

  return (
    <InputArea as="form" onSubmit={handleSubmit}>
      <StyledInput
        type="text"
        value={command}
        onChange={(e) => setCommand(e.target.value)}
        placeholder="Enter your command..."
      />
      <StyledButton type="submit">Send</StyledButton>
    </InputArea>
  );
};
