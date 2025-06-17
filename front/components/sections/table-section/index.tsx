import * as S from "./styles";

export function TableSection() {
  return (
      <S.TableSection>
            <div className="table-header">
                <h3 className="table-title">O.S por Técnico</h3>
                <div className="table-filter">
                    <span>Filtro & Buscar</span>
                    <span>⚙️</span>
                </div>    
            </div>

            <table className="data-table">
                <thead>
                    <tr>
                        <th>Técnico</th>
                        <th>Departamento</th>
                        <th>Área</th>
                        <th>Conclusão</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <div className="employee-info">
                                <div className="employee-avatar"></div>
                                <span>Justin Lipshutz</span>
                            </div>
                        </td>
                        <td>Marketing</td>
                        <td>22</td>
                        <td>
                            <div style={{display: "flex", alignItems: "center", gap: "8px"}}>
                                <div className="progress-bar">
                                    <div className="progress-fill" style={{width: "100%"}}></div>
                                </div>
                                <span>100%</span>
                            </div>
                        </td>
                        <td><span className="status-badge status-permanent">Permanent</span></td>
                    </tr>
                    <tr>
                        <td>
                            <div className="employee-info">
                                <div className="employee-avatar"></div>
                                <span>Marcus Culhane</span>
                            </div>
                        </td>
                        <td>Finance</td>
                        <td>24</td>
                        <td>
                            <div style={{display: "flex", alignItems: "center", gap: "8px"}}>
                                <div className="progress-bar">
                                    <div className="progress-fill" style={{width: "95%"}}></div>
                                </div>
                                <span>95%</span>
                            </div>
                        </td>
                        <td><span className="status-badge status-contract">Contract</span></td>
                    </tr>
                    <tr>
                        <td>
                            <div className="employee-info">
                                <div className="employee-avatar"></div>
                                <span>Leo Stanton</span>
                            </div>
                        </td>
                        <td>R&D</td>
                        <td>28</td>
                        <td>
                            <div style={{display: "flex", alignItems: "center", gap: "8px"}}>
                                <div className="progress-bar">
                                    <div className="progress-fill" style={{width: "89%"}}></div>
                                </div>
                                <span>89%</span>
                            </div>
                        </td>
                        <td><span className="status-badge status-permanent">Permanent</span></td>
                    </tr>
                </tbody>
            </table>
            
      </S.TableSection>
  );
}