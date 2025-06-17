import * as S from "./styles";

export function Sidebar() {
  return (
      <S.Sidebar>
            <div className="logo">FAST</div>
            <ul className="nav-menu">
                <li className="nav-item">
                    <div className="nav-icon"></div>
                    <span>Início</span>
                </li>
                <li className="nav-item">
                    <div className="nav-icon"></div>
                    <span>Estoque</span>
                </li>
                <li className="nav-item">
                    <div className="nav-icon"></div>
                    <span>Ordens de Serviço</span>
                </li>
                <li className="nav-item">
                    <div className="nav-icon"></div>
                    <span>Relatórios</span>
                </li>
                <li className="nav-item active">
                    <div className="nav-icon"></div>
                    <span>Dashboard</span>
                </li>
                <li className="nav-item">
                    <div className="nav-icon"></div>
                    <span>Configurações</span>
                </li>
                <li className="nav-item">
                    <div className="nav-icon"></div>
                    <span>Deslogar</span>
                </li>
            </ul>
      </S.Sidebar>
  );
}