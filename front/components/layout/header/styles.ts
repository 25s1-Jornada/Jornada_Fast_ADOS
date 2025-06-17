import styled from "styled-components";

export const Header = styled.section`
    
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    

    .page-title {
        font-size: 28px;
        font-weight: 600;
        color: #333;
    }

    .user-info {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #2c5aa0;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }

`;