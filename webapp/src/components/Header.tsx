import React from "react";
import { HeaderBar } from "../styles/components";

interface HeaderProps {
  characterName: string;
  health: number;
  maxHealth: number;
}

export const Header: React.FC<HeaderProps> = ({
  characterName,
  health,
  maxHealth,
}) => (
  <HeaderBar>
    <div>{characterName}</div>
    <div>
      Health: {health}/{maxHealth}
    </div>
  </HeaderBar>
);
