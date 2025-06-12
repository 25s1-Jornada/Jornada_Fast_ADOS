import styled from "styled-components";

export const SmallVallueCard = styled.section`
        background: white;
        padding: 25px !important;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);


    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }

    .card-title {
        font-size: 14px;
        color: #666;
        font-weight: 500;
    }

    .card-trend {
        font-size: 12px;
        padding: 4px 8px;
        border-radius: 12px;
        font-weight: 500;
    }

    .trend-positive {
        background-color: #d4edda;
        color: #155724;
    }

    .trend-negative {
        background-color: #f8d7da;
        color: #721c24;
    }
`;