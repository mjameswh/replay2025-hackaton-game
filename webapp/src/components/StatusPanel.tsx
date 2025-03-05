import React from "react";
import { StatusPanelContainer } from "../styles/components";

interface Character {
  stats: {
    hp: number;
    maxHp: number;
    gold: number;
    xp: number;
  };
  inventory: string[];
}

interface StatusPanelProps {
  character: Character;
}

export const StatusPanel: React.FC<StatusPanelProps> = ({ character }) => (
  <StatusPanelContainer>
    <h2>Character Stats</h2>
    <div>
      <p>
        HP: {character.stats.hp}/{character.stats.maxHp}
      </p>
      <p>Gold: {character.stats.gold}</p>
      <p>XP: {character.stats.xp}</p>
    </div>

    <h2>Inventory</h2>
    <div>
      {character.inventory.map((item, index) => (
        <p key={index}>- {item}</p>
      ))}
    </div>
  </StatusPanelContainer>
);
