import styled from "styled-components";

export const BigVallueCard = styled.section`
        .donut-chart {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }

        .donut-container {
            position: relative;
            width: 150px;
            height: 150px;
        }

        .donut {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: conic-gradient(#2c5aa0 0deg 198deg, #17a2b8 198deg 360deg);
            position: relative;
        }

        .donut::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80px;
            height: 80px;
            background: white;
            border-radius: 50%;
        }

        .donut-legend {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
        }

        .legend-color1 {
            width: 12px;
            height: 12px;
            border-radius: 2px;
            background: #2c5aa0;
        }

        .legend-color2 {
            width: 12px;
            height: 12px;
            border-radius: 2px;
            background: #17a2b8;
        }
    
    .textinho {
        font-size: 12px; color: #999; margin-top: 10px;
    }
`;