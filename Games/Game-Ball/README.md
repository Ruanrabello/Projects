<p align="center">
  <img src="./assets/neon-depths-header.svg" width="100%" alt="Neon Depths — roguelike cyberpunk em Python e Pygame">
</p>

<p align="center">
  <strong>Roguelike de ação com geração procedural, combate, chefes, progressão e identidade visual neon.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Pygame-0B7A3B?style=for-the-badge" alt="Pygame">
  <img src="https://img.shields.io/badge/JSON-Persistência-EC4899?style=for-the-badge" alt="JSON">
  <img src="https://img.shields.io/badge/Status-Funcional-16A34A?style=for-the-badge" alt="Status funcional">
</p>

<p align="center">
  <a href="../../README.md">← Voltar ao catálogo de projetos</a>
</p>

## Visão geral

**Neon Depths** é um jogo de ação em perspectiva superior inspirado em roguelikes e shooters arcade. O jogador explora masmorras geradas proceduralmente, enfrenta inimigos com comportamentos diferentes, coleta power-ups e avança por andares cada vez mais difíceis.

O projeto divide gameplay, apresentação e infraestrutura em sistemas independentes. O suporte a áudio e gamepad é defensivo: a ausência de dispositivo de som ou um controle com menos eixos não impede o jogo de iniciar.

## Principais funcionalidades

| Sistema | Descrição |
|---|---|
| Combate | Mira, disparos, dano, dash e invencibilidade temporária |
| Geração procedural | Cria salas, corredores, spawns e saídas de andar |
| Inimigos e chefes | Comportamentos, escalonamento de dificuldade e bosses periódicos |
| Progressão | Experiência, níveis, pontuação e power-ups |
| Interface | HUD, menus, notificações e números de dano |
| Persistência | Save, leaderboard e conquistas em JSON |
| Apresentação | Partículas, iluminação, screen shake e áudio procedural |
| Display | Janela redimensionável, tela cheia e ultrawide com letterbox |
| Entrada | Teclado, mouse e gamepad com dead zone |

## Arquitetura

```text
Entrada e estados
      │
      ▼
main.py ─────────────── menu.py
  │                         │
  ├── player.py             ├── configurações
  ├── enemy.py              ├── leaderboard
  ├── bullet.py             └── conquistas
  ├── map.py
  ├── ui.py
  │
  ├── effects/  → partículas e iluminação
  └── utils/    → câmera, áudio, colisão, display, input e persistência
```

## Estrutura

```text
Game-Ball/
├── assets/
│   └── neon-depths-header.svg
├── effects/
├── utils/
│   ├── achievements.py
│   ├── audio.py
│   ├── camera.py
│   ├── collision.py
│   ├── display.py
│   ├── input_handler.py
│   ├── leaderboard.py
│   ├── save_system.py
│   └── sprites.py
├── main.py
├── settings.py
├── player.py
├── enemy.py
├── bullet.py
├── map.py
├── ui.py
├── menu.py
├── requirements.txt
└── README.md
```

## Controles

| Ação | Controle |
|---|---|
| Movimentação | `WASD`, setas ou analógico esquerdo |
| Mira | Mouse ou analógico direito |
| Disparo | Mouse |
| Dash | Espaço ou botão principal do gamepad |
| Pausa | `Esc`, `P` ou Start |
| Tela cheia | `F11` |

## Como executar localmente

```bash
git clone https://github.com/Ruanrabello/Projects.git
cd Projects/Games/Game-Ball
python -m venv .venv
```

No Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

No Linux ou macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Caso nenhum dispositivo de áudio esteja disponível, o jogo continua sem som.

## Dados locais

Os arquivos de save, leaderboard e conquistas são criados em `saves/` e permanecem fora do Git. O save combina configurações antigas com novos valores padrão e é gravado de forma atômica para reduzir risco de corrupção.

## Roadmap

- [x] Implementar combate, dash, progressão, chefes e mapas procedurais.
- [x] Adicionar save, leaderboard e conquistas.
- [x] Tornar áudio, gamepad e persistência mais resilientes.
- [ ] Adicionar screenshot ou GIF real da jogabilidade.
- [ ] Criar testes para colisões e geração de mapas.
- [ ] Adicionar novos inimigos, armas e biomas.
- [ ] Empacotar uma versão executável para Windows.

## Licença

Distribuído sob a [licença MIT](../../LICENSE).

## Autor

**Ruan Rabello** — estudante de Engenharia da Computação com foco em Back-end, Dados, IA e Automação.

[LinkedIn](https://www.linkedin.com/in/ruan-rabello-da-silva-9032b5274/) · [Portfólio](https://ruanportifolio.lovable.app) · [GitHub](https://github.com/Ruanrabello)
