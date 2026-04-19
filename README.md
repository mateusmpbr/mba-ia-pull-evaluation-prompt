# Técnicas Aplicadas

- **Role Prompting**
  - **Justificativa para escolha**: essa técnica é fundamental para refatorar o prompt, pois permite definir uma persona específica (no caso, um product manager) que orienta o modelo na geração das histórias de usuário.
  - **Como foi aplicada**: solicitei ao modelo para ele atuar como um Product Manager sênior e redator técnico, estabelecendo desde o início o estilo e o comportamento esperados.

- **Few-shot Prompting**
  - **Justificativa para escolha**: ao usar essa técnica, forneço exemplos que calibram o comportamento do modelo e mostram exatamente como ele deve responder.
  - **Como foi aplicada**: incluí amostras de respostas ideais, demonstrando ao modelo o formato e o nível de detalhamento esperado ao converter relatos de bugs em histórias de usuário.

- **Chain of Thought**
  - **Justificativa para escolha**: essa técnica melhora o raciocínio e aumenta a precisão, incentivando o modelo a pensar de forma estruturada, “passo a passo”.
  - **Como foi aplicada**: instruí o modelo a explicitar seu raciocínio quando necessário, seguindo a lógica do Chain of Thought para chegar a respostas mais consistentes.

# Modelos de IA utilizados

- **LLM_PROVIDER**=google
- **LLM_MODEL**=gemini-2.5-flash-lite
- **EVAL_MODEL**=gemini-2.5-flash-lite

# Resultados Finais

- **Prompt no LangSmith**: https://smith.langchain.com/hub/mateusmpbr/bug_to_user_story_v2

- **Estatísticas no LangSmith**:
- ![Foto das estatísticas no LangSmith](static/langsmith-stats.png)

- **Resultado das avaliações**:
- ![Foto do resultado das avaliações](static/evaluations-result.png)
