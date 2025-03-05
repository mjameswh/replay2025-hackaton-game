import styled from "styled-components";

export const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
`;

export const HeaderBar = styled.header`
  background: #2c3e50;
  color: white;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
`;

export const MainContent = styled.main`
  display: flex;
  flex: 1;
  overflow: hidden;
`;

export const ChatWindowContainer = styled.div`
  flex: 7;
  padding: 1rem;
  background: #f5f5f5;
  overflow-y: auto;
`;

export const StatusPanelContainer = styled.div`
  flex: 3;
  padding: 1rem;
  background: #e0e0e0;
  border-left: 1px solid #ccc;
  overflow-y: auto;
`;

export const InputArea = styled.div`
  padding: 1rem;
  background: #f0f0f0;
  display: flex;
  gap: 1rem;
`;

export const StyledInput = styled.input`
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
`;

export const StyledButton = styled.button`
  padding: 0.5rem 1rem;
  background: #2c3e50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;

  &:hover {
    background: #34495e;
  }
`;
