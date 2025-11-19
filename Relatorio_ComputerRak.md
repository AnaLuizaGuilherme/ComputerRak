# 📘 Relatório Pedagógico – *ComputerRak: Tabuleiro de Computabilidade*

## 1. Identificação do Plugin
**Nome:** ComputerRak — Tabuleiro Gamificado de Computabilidade  
**Área:** Modelos Computacionais / Computabilidade  
**Grupo:**  
- Ana Luiza Guilherme — 33911410  
- Kayky Mourão de Oliveira — 33579016  
- Rafael de Albuquerque Tavares — 34225013  

## 2. Objetivo Pedagógico
O objetivo do ComputerRak é facilitar a compreensão dos principais tópicos de computabilidade por meio de um jogo gamificado que simula um tabuleiro ao estilo Monopoly Go. O aluno aprende conceitos de forma dinâmica, por meio de desafios interativos.

## 3. Descrição do Jogo
O jogo consiste em um tabuleiro circular com 16 casas. A cada jogada:
- Dois dados são lançados.
- O jogador avança casas.
- A casa determina o desafio:
  - Quiz
  - Prova guiada
  - Probabilidade (casas "?")
  - Ferroviária (quiz ou prova aleatória)

Tudo é processado pelo backend FastAPI.

## 4. Conteúdo Relacionado à Disciplina
O jogo aborda:
- Máquinas de Turing  
- Decidibilidade e indecidibilidade  
- Funções computáveis  
- Reduções ≤m  
- Teorema de Rice  
- Problema da Parada  
- Linguagens Regulares / RE / co-RE  
- Diagonalização  
- Probabilidade Básica (casas "?")

## 5. Critérios de Pontuação
- Quiz → +10 pontos  
- Prova Guiada → +15 pontos  
- Dica ativada → redução para +5  
- Sem penalidade de erros

## 6. Testes Realizados
- Lançamento de sessão (/launch)  
- Score correto e incorreto (/score)  
- Simulações no endpoint "/"  
- Testes de posição, dados e integridade do tabuleiro  
- Tratamento de erros com session_id inválido  

## 7. Roteiro de Demonstração
### Cenário Feliz
1. Iniciar API  
2. Abrir Streamlit  
3. Criar sessão  
4. Jogar dados  
5. Mostrar desafios  
6. Responder um quiz  
7. Mostrar banco SQLite

### Cenário de Erro
- session_id inválido  
- payload errado  
- API offline (tratamento no frontend)

## 8. Conclusão
O ComputerRak torna computabilidade mais acessível, visual e interativa.  
A gamificação reforça o aprendizado através de repetição, erros controlados e desafios progressivos.
