# Inteligência Artificial - Trabalho Prático 1
## Jelly Field

## Instruções de compilação e execução:

1. **Criar o ambiente virtual (venv):**

```bash
python3 -m venv venv
```

2. **Iniciar o ambiente virtual:**

```bash
source venv/bin/activate
```

3. **Instalar as dependências necessárias (dentro do ambiente virtual):**

```bash
pip install pygame
```

4. **Correr o jogo no ambiente virtual:**

```bash
python main.py
```

Este comando irá abrir um menu, no qual, utilizando o rato, podemos escolher várias opções:
- "Play" se quisermos jogar o jogo, que nos leva para um menu onde podemos escolher o mapa e a dificuldade;
- "Computer" se quisermos testar as IA's implementadas no jogo;
- "How to play" para se quisermos aceder às instruções e regras do jogo.

Podemos executar um movimento selecionando uma das duas peças na parte inferior do ecrã e uma posição livre no tabuleiro do jogo (jogar a peça selecionada no local vazio). As regras e objetivos do jogo estão expostas em "How to Play".

Os resultados produzidos pela utilização das IA's são armazenados em /results.