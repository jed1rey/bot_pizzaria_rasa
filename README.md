# Bot Pizzaria com Rasa 🍕

Chatbot desenvolvido em **Rasa** para uma pizzaria fictícia, com funcionalidades de atendimento automatizado.

## Funcionalidades

* **Saudação inicial**: dá boas-vindas ao cliente.
* **Fazer pedido**: guia o usuário na escolha de sabor, tamanho e borda da pizza.
* **Validação de sabor**: confere se o sabor informado está disponível.
* **Validação de tamanho**: confirma se o tamanho informado é válido (pequena, média ou grande).
* **Confirmação do pedido**: revisa e confirma o pedido antes da finalização.
* **Cancelamento/Despedida**: finaliza a conversa educadamente.

### Funcionalidades extras adicionadas

* **Horário de funcionamento**: informa os horários de atendimento da pizzaria.
* **Ingrediente extra**: permite adicionar ou recusar ingredientes adicionais.

## Estrutura do Projeto

* `domain.yml`: definição de intents, slots, entidades, ações e respostas.
* `rules.yml` e `stories.yml`: definem o fluxo de conversas.
* `actions.py`: contém as ações personalizadas (incluindo as funcionalidades extras adicionadas).
* `nlu.yml`: exemplos de treinamento para reconhecimento de intenções.

## Tecnologias

* **Rasa Open Source** (NLU + Core)
* **Python**

## Como executar

1. Criar e ativar o ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```
2. Instalar dependências:

   ```bash
   pip install -r requirements.txt
   ```
3. Treinar o modelo:

   ```bash
   rasa train
   ```
4. Iniciar o servidor de ações:

   ```bash
   rasa run actions
   ```
5. Iniciar o bot em modo shell:

   ```bash
   rasa shell
   ```

## Autor

**Paula Cristina Abib Teixeira**
Matéria: *Processamento de Linguagem Natural*
Fatec Franca
