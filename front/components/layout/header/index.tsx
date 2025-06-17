import * as S from "./styles";

export function Header() {
  return (
      <S.Header>
            <h1 className="page-title">Resumo Geral</h1>
            <div className="user-info">
                <div className="user-avatar">U</div>
            </div>
      </S.Header>
  );
}