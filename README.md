# Chamada Digital - Instituto Saber Social

> Plataforma inteligente de gestão de frequência, cadastros e apoio socioeducativo para substituição de processos manuais em nuvem.

---

## 📝 Sobre o Projeto e o Instituto

### O Instituto
O **Instituto Saber Social** é uma Organização da Sociedade Civil (OSC) que atende crianças e adolescentes na faixa etária de 6 a 14 anos, divididos em grupos internos de atendimento socioeducativo. A instituição oferece oficinas semanais de esportes, artes, hip-hop, artes marciais e música, com o objetivo de promover o acolhimento, desenvolvimento social e cidadania.

### O Projeto
A plataforma **Chamada Digital** foi idealizada para substituir o atual controle de frequência do instituto — que hoje opera de forma manual através de cadernos físicos e planilhas descentralizadas no OneDrive. O sistema automatiza o cálculo de assiduidade para garantir o cumprimento da meta mínima de **70% de frequência exigida por lei**, mitigando o retrabalho técnico, eliminando falhas humanas e auxiliando diretamente as equipes de referência (assistentes sociais e psicólogas) na execução de relatórios periódicos para a Secretaria de Assistência Social.

---

## 🚀 Funcionalidades Planejadas

O desenvolvimento foi estruturado em ciclos incrementais (Scrum/Metodologia Ágil) para garantir entregas rápidas de valor e adaptação contínua ao nível de maturidade digital dos usuários.

### 📌 Escopo Inicial (Fase 1 - MVP / Sprints 1 e 2)
* **Controle de Frequência Básica (Espinha Dorsal):** Substituição da chamada física por listagens automatizadas de presença e falta por turma/data.
* **Módulo de Justificativas:** Campo obrigatório para registrar justificativas de ausência sempre que o atendido estiver abaixo de 70% de assiduidade.
* **Gestão de Perfis de Acesso (RBAC):** Controle restrito onde professores/oficineiros gerenciam apenas suas respectivas turmas e administradores possuem visão global.
* **Cadastros Estruturais:** Módulo de registros contendo dados socioeconômicos dos atendidos (NIS, CPF, escola, período e benefícios como Bolsa Família).
* **Observações e Notas Qualitativas:** Diário de classe digital para registro rápido de atividades diárias desenvolvidas e intercorrências pontuais.

### 🔮 Escopo Futuro (Fase 2+ / Sprints 3+)
* **Inteligência de Dados (Alertas Críticos):** Identificação visual imediata e automatizada de alunos com frequência crítica (< 75%) para prevenção ativa de evasão escolar.
* **Filtros e Relatórios Customizados:** Mecanismos de busca para exportação de recortes de faixas etárias específicas sob demanda, facilitando o preenchimento do sistema municipal (CISC/Cadastro Único).
* **Módulo de Gestão de Estoque Centralizado:** Ferramenta compartilhada e dinâmica para controle e remanejamento de materiais pedagógicos entre as três unidades do instituto.
* **Prontuário Eletrônico de Colaboradores e Fluxo de Caixa:** Expansão administrativa para gestão de RH interno e unificação de rotas de veículos.

---

## 📐 Modelagem do Banco de Dados (DER)

A modelagem lógica do banco de dados (que engloba entidades como *Atendidos, Responsáveis, Oficineiros, Oficinas, Presenças, Unidades e Turmas*) foi estruturada de forma relacional.

> 🌐 **Acesse o modelo interativo aqui:** [Link para o Diagrama no dbdiagram.io](https://dbdiagram.io/d/6a0cc6239f1f8ec47b56be1e)

---

## 🛠️ Stack Tecnológica

O ecossistema do projeto foi planejado com uma arquitetura moderna, focada em alta performance (tempo de carregamento de chamadas inferior a 2 segundos) e portabilidade para dispositivos móveis (*Mobile-First*).

### Front-end (Interface Mobile & Web)
* **Framework Principal:** **React Native** (com Expo) ou **React.js** (configurado como PWA - *Progressive Web App*). 
  > *Justificativa:* Garante que os oficineiros e professores consigam fazer a chamada direto pelo celular na sala de aula, mesmo com redes móveis instáveis.
* **Estilização e UI:** **Tailwind CSS** (ou NativeWind para mobile), garantindo uma interface limpa, leve e de alta legibilidade (*learnability*).

### Back-end (API e Regras de Negócio)
* **Ambiente de Execução:** **Node.js** (com TypeScript e Express) ou **Python** (com FastAPI).
  > *Justificativa:* Perfeito para a construção de uma API REST escalável, lidando de forma ágil com as rotinas de checagem de frequência e autenticação de usuários.
* **Segurança e Criptografia:** **BCrypt** para encriptação de senhas com *salted hashing* e **JWT** (*JSON Web Tokens*) para controle de sessões e perfis de acesso (RBAC).

### Banco de Dados (Persistência e Relacionamentos)
* **Tipo:** **Relacional (SQL)**.
  > *Justificativa:* Indispensável para o projeto devido à necessidade estrita de integridade referencial (garantir que uma presença esteja obrigatoriamente amarrada a um aluno válido e a uma turma existente).
* **SGBD:** **PostgreSQL** ou **MySQL**.

### Infraestrutura, DevOps e Segurança
* **Controle de Versão:** **Git** e **GitHub** para gerenciamento de branches e integração do grupo.
* **Conformidade com a LGPD:** Camada de segurança dedicada para a proteção e mascaramento de dados sensíveis de menores de idade (como CPF, NIS e relatórios psicossociais).
* **Hospedagem da API:** Sob análise (**Render** ou **Vercel** para o deploy inicial gratuito do MVP).
