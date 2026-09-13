# Sprint_3_Simulador_ChargeGrid

ChargeGrid Intelligence — Sprint 3

1. Sobre o projeto

O ChargeGrid Intelligence é uma proposta de gerenciamento inteligente de recarga de veículos elétricos, integrando aplicativo, Supabase, estações, carregadores, dados energéticos, tarifação e automação.

2. Arquitetura

Aplicativo (Thunkable) → API REST → Supabase/PostgreSQL → dados de usuários, veículos, estações, carregadores, tarifas, sessões e energia.

Os dados energéticos alimentam regras de gerenciamento de demanda, que podem registrar comandos de automação.

3. Fluxo funcional

Usuário consulta uma estação.

Seleciona veículo e carregador.

Uma sessão de carregamento é criada.

O carregador passa para ocupado.

O sistema monitora energia/demanda.

Regras podem manter, reduzir ou ampliar a potência.

O comando de automação é registrado.

Ao finalizar, energia e custo são registrados.

O carregador volta a livre e a sessão aparece no histórico.

4. Tecnologias

Thunkable

Supabase

PostgreSQL

REST API

Regras de automação

Dados simulados de energia

5. Estrutura do banco

As sessões relacionam:

usuario_id → usuários

veiculo_id → veículos

estacao_id → estações

carregador_id → carregadores

tarifa_id → tarifas

carregadores.id_estacao relaciona cada carregador à sua estação.

6. Gerenciamento energético

Regra principal:

se a demanda ultrapassar a potência disponível, reduzir potência e registrar comando;

se houver margem energética, manter ou ampliar conforme as regras;

em horário de pico, recomendar recarga em período de menor tarifa.

7. Resultados

Os resultados devem ser apresentados com evidências do banco e do aplicativo. Valores simulados precisam ser identificados como cenários de teste.

8. Conteúdos da disciplina

O projeto aplica banco de dados relacional, APIs, programação, automação, lógica de decisão, tarifação, eficiência energética, sustentabilidade e conceitos de inteligência artificial.

9. Equipe

[Guilherme Miranda — 573107]

[Carlos Eduardo — 572949]

[Rafael Gandolfi — 569036]

[Jõao Soler — 569725]

[Rafael Lins — 570588]

[Cauã Paes — 569906]
