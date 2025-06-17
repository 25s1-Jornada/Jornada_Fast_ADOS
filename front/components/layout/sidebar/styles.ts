import styled from "styled-components";

export const Sidebar = styled.section`
  width: 250px;
  background-color: #fff;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  padding: 20px 0;

  .logo {
    padding: 0 20px 30px;
    font-size: 24px;
    font-weight: bold;
    color: #2c5aa0;
  }

  .nav-menu {
    list-style: none;
  }

  .nav-item {
    padding: 12px 20px;
    cursor: pointer;
    transition: background-color 0.3s;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .nav-item:hover {
    background-color: #f0f0f0;
  }

  .nav-item.active {
    background-color: #2c5aa0;
    color: white;
  }

  .nav-icon {
    width: 16px;
    height: 16px;
    background-color: currentColor;
    border-radius: 2px;
  }
`;
