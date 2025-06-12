import styled from "styled-components";

export const SummarySharts = styled.section`
    
    margin-top: 30px;

    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 30px;
    margin-bottom: 30px;
    

    .chart-container {
        background: white;
        padding: 25px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    .chart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    .chart-title {
        font-size: 18px;
        font-weight: 600;
        color: #333;
    }

    .chart-filter {
        display: flex;
        gap: 10px;
        align-items: center;
    }

    .filter-btn {
        padding: 6px 12px;
        border: 1px solid #ddd;
        background: white;
        border-radius: 4px;
        cursor: pointer;
        font-size: 12px;
    }

    .filter-btn.active {
        background: #2c5aa0;
        color: white;
        border-color: #2c5aa0;
    }
`;