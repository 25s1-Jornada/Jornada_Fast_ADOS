import styled from "styled-components";

export const BarShart = styled.section`
    .bar-chart {
            display: flex;
            align-items: end;
            gap: 8px;
            height: 200px;
            padding: 20px 0;
        }

        .bar {
            background: linear-gradient(to top, #1e4d72, #2c5aa0);
            border-radius: 4px 4px 0 0;
            min-width: 30px;
            position: relative;
            transition: all 0.3s ease;
        }

        .bar:hover {
            opacity: 0.8;
        }

        .bar.highlighted {
            background: linear-gradient(to top, #0066cc, #0080ff);
        }
`;