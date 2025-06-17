import styled from "styled-components";

export const TableSection = styled.section`
    background: white;
    padding: 25px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);

      .table-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .table-title {
            font-size: 18px;
            font-weight: 600;
            color: #333;
        }

        .table-filter {
            display: flex;
            gap: 10px;
            align-items: center;
            font-size: 12px;
            color: #666;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
        }

        .data-table th,
        .data-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }

        .data-table th {
            font-weight: 600;
            color: #666;
            font-size: 12px;
            text-transform: uppercase;
        }

        .employee-info {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .employee-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: #ddd;
        }

        .status-badge {
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }

        .status-permanent {
            background: #d4edda;
            color: #155724;
        }

        .status-contract {
            background: #fff3cd;
            color: #856404;
        }

        .progress-bar {
            width: 60px;
            height: 6px;
            background: #eee;
            border-radius: 3px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: #28a745;
            border-radius: 3px;
        }
`;