# Wandi IDE - IDE de Microcontroladores e Simulação 3D Avançada

## 🌟 Visão Geral

O **Wandi IDE** é uma plataforma de desenvolvimento avançada, criada em **Python (PyQt6)**, projetada para programação de microcontroladores e integração com **simulação 3D em tempo real**.

Ele combina:

* Editor de código completo
* Consola de execução
* Dock de simulação 3D
* Barra de ferramentas e menus altamente configuráveis

O foco principal é **educacional e profissional**, permitindo que desenvolvedores programem microcontroladores e vejam o comportamento de seus projetos em uma simulação 3D realista antes de testar no hardware físico.

---

## 🛠 Funcionalidades Principais

### 1️⃣ Editor de Código

* Suporte a múltiplas abas
* Destaque de sintaxe para Python e futuras linguagens de microcontrolador
* Integração com execução direta
* Undo/redo, copiar, colar e navegação rápida

### 2️⃣ Consola de Saída e Monitor Serial

* Execução de scripts Python localmente
* Monitoramento de portas seriais conectadas ao microcontrolador
* Exibição de logs de execução e mensagens do hardware

### 3️⃣ Docks Modulares

* Consola de saída
* Simulador 3D
* Informações do sistema e debug
* Permite layout personalizável e redimensionável pelo usuário

### 4️⃣ Simulação 3D Avançada

* Visualização em tempo real do comportamento do microcontrolador e sensores
* Simulação física para testar movimentos, colisões e interações
* Preparado para futuras integrações com motores robóticos reais

### 5️⃣ Barra de Ferramentas e Menu

* Botões Run / Stop / Upload / Compile
* Acesso rápido a configurações e estilos
* Possibilidade de personalização total via arquivo de estilo (`.qss`)

### 6️⃣ Integração Modular

* Backend, UI e runtime separados
* Facilidade para adicionar novos tipos de docks ou simulações
* Suporte à comunicação futura com motores 3D, firmwares e hardware real

---

## 🎨 Personalização e Estilo

* Tema escuro padrão via `dark.qss`
* Cada elemento mapeado para customização completa
* Separação de estilo e lógica para manter o código principal limpo

---

## ⚡ Tecnologias

* Python 3.12
* PyQt6 (QMainWindow, QDockWidget, QPlainTextEdit, QWebEngineView, QLabel)
* Estrutura modular de docks e overlays
* Preparado para integração com motores de simulação 3D externos (Three.js, PyBullet)

---

## 📂 Estrutura do Projeto

```
WANDI/
├── ide.py                # IDE principal
├── style/
│   └── dark.qss          # Tema escuro completo
├── wandi3d/              # Motor 3D independente
│   ├── index.html
│   ├── main.js
│   └── package.json
├── wandi.png             # Ícone da IDE
└── README.md
```

---

## 🚀 Próximos Passos

* Integração de novos microcontroladores
* Simulação 3D interativa com física realista
* Sistema de plugins para extensões de IDE
* Monitoramento em tempo real entre hardware físico e simulação 3D

# Wandi IDE

Aqui está uma captura de tela da interface do Wandi IDE:

![Captura de tela do Wandi IDE](https://github.com/eliMassaqui/Wandi/raw/master/Captura%20de%20ecr%C3%A3%202026-01-12%20171653.png)

