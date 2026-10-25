<div align="center">

<img src="docs/assets/icon-512.png" width="108" alt="Free My TV Logo">

# Free My TV (for LG webOS)

**A fast, ad-free 60fps home screen for LG Smart TVs.**

The streaming apps you actually use on a frosted glass shelf, live weather that follows the sunset, and trending cinema picks.<br>
Open source. Zero ads. 100% Onboard. No root required.

[![License: MIT](https://img.shields.io/badge/License-MIT-0a84ff.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/LG_webOS-3.0_to_24+-30d158.svg)](#)
[![Performance](https://img.shields.io/badge/Render-60_FPS_Native-ff9f0a.svg)](#)
[![No Root](https://img.shields.io/badge/Root-Not_Required-brightgreen.svg)](#)

[**Install**](#-quick-install-2-minutes) · [**Features**](#-what-you-get) · [**Customize**](#%EF%B8%8F-make-it-yours-on-tv-customization) · [**Roadmap**](ROADMAP.md) · [**How It Works**](#%EF%B8%8F-how-it-works)

**🇺🇸 English** · [**🇧🇷 Português**](#free-my-tv-para-lg-webos)

<br>

<img src="docs/assets/preview.png" width="900" alt="Free My TV on LG webOS: Frosted glass app shelf, dynamic hero preview, live weather, and trending movies">

</div>

---

## ⚡ Why This Exists

Modern LG webOS (especially webOS 6, 22, 23, and 24) replaced the classic, snappy bottom card bar with a sluggish full-screen portal packed with:
- Auto-playing banner ads, shopping promotions, and "Trending Now" bloatware.
- 3 to 5 second lag spikes every time you press the Home button.
- Background telemetry and Automatic Content Recognition (ACR).

**Free My TV for webOS** brings the philosophy of [simbasjungles/free-my-tv](https://github.com/simbasjungles/free-my-tv) and Apple tvOS natively to LG televisions—giving you an instantaneous, clean glass dashboard that lives right on your TV's internal flash memory.

---

## ✨ What You Get

- **🚫 Zero Ads. Ever.** No sponsored rows, no banner promos, no shopping widgets.
- **🧊 Frosted Glass App Shelf.** Your favorite streaming apps and HDMI inputs front-and-center, launching natively in ~100ms via the webOS Luna bus.
- **⚙️ On-Screen Shelf Customizer.** Automatically detects installed apps on your LG TV so you can toggle which ones appear on your shelf using your remote.
- **🌅 Dynamic Sunset & OLED Themes.** Connects to Open-Meteo to show live local weather and automatically shifts your background from *Daylight Blue* to *Sunset Amber* to *Deep Midnight* (plus a *Pure OLED Black* mode).
- **🎬 Movies & Shows Trending Tabs.** Separate tabs for trending movies and TV shows—TMDB-ranked with your optional key, or our built-in zero-key live feed (TVMaze for Shows, curated picks for Movies).
- **🌤️ Weather & Sun Drawer.** Click the weather widget for an hourly forecast and exact sunrise/sunset times, powered by Open-Meteo.
- **🌑 OLED-Safe Idle Screensaver.** A pure-black floating clock kicks in after a few minutes idle and gently shifts position to avoid burn-in—dismissed by any key or remote movement.
- **🎮 Full Magic Remote & D-Pad Support.** Point and click with the LG Magic Remote cursor, or fly across tiles with the directional arrow keys and scroll wheel.
- **💻 100% Onboard & Independent.** Installed as a native `.ipk` package on your TV. Your computer does **not** need to stay on.
- **🛡️ Safe & Reversible.** Works on stock unrooted TVs via official LG Developer Mode (or Homebrew Channel). Your factory home screen is untouched.

---

## 📊 Stock LG webOS Home vs. Free My TV

| Metric / Feature | Stock LG webOS 24 Home | Free My TV (webOS) |
|---|---|---|
| **Sponsored Ads & Banners** | ❌ 70%+ of screen real estate | ✅ **0% (Completely Ad-Free)** |
| **Cold Load Time** | ❌ 3.5 – 5.0 seconds | ✅ **< 0.2 seconds** |
| **Frame Rate** | ❌ Frequent UI frame drops | ✅ **Locked 60 FPS** |
| **OLED Burn-in Friendly** | ❌ Bright static ad banners | ✅ **Dark Glass & Pure OLED Mode** |
| **PC Required After Install** | N/A | ✅ **No (Runs 100% Onboard)** |
| **Root Required** | N/A | ✅ **No (Official Dev Mode)** |

---

## 🚀 Quick Install (2 Minutes)

All you need is an LG Smart TV (webOS 3.0+) and a computer on the same Wi-Fi for the initial 2-minute install.

### Step 1: Enable Developer Mode on the TV
1. Open the **Apps / LG Content Store** on your TV, search for **`Developer Mode`**, and install it.
2. Open **Developer Mode**, sign in with your free LG Developer account ([webostv.developer.lge.com](https://webostv.developer.lge.com)), and switch **Dev Mode Status** to **ON**.
3. After the TV restarts, open **Developer Mode** again and toggle **Key Server** to **ON**. Note the **IP Address** and 6-character **Passphrase** on screen.

### Step 2A: Automated One-Command Install (Recommended)
Run our automated Python installer—it discovers your TV on the network, pairs the SSH key, packages the app, and installs it:

```bash
git clone https://github.com/danielthejoker18/FreeMyTvWebOS.git
cd FreeMyTvWebOS
python scripts/install.py
```

### Step 2B: GUI Install via webOS Dev Manager
1. Install [webOS Dev Manager](https://github.com/webosbrew/dev-manager-desktop/releases) (`winget install webosbrew.webOSDevManager` on Windows).
2. Connect your TV using the IP and Passphrase.
3. Download [`dist/org.webos.freemytv_1.2.5_all.ipk`](dist/org.webos.freemytv_1.2.5_all.ipk) and click **Install .ipk**.

> [!TIP]
> **Make It Your 1-Second Home Key (Quick Access):**
> While inside **Free My TV** on your TV, **press and hold number `1`** (or hold `0` to open Quick Access) on your Magic Remote and assign **Free My TV** to key **`1`**. Now, holding **`1`** from anywhere on your TV jumps straight into your clean glass hub in half a second!

---

## ⚙️ Make It Yours (On-TV Customization)

Click the **⚙️ Customize** button in the top-right corner of the dashboard using your remote:

Choose **Reorder** on the main shelf. Select a tile and press OK to pick it up, use Left/Right to move it, then OK to place it. Choose **Done** to save. Back or Cancel discards changes.

Launch messages use the app or console name and report unavailable apps, failures, or no response after eight seconds. Repeated presses are ignored while a launch is pending; browser previews explain that launching requires an LG TV.

Under **HDMI Devices**, press a port to cycle through HDMI, PS5, PS4, Xbox, Nintendo Switch, and Gaming PC, then choose **Save & Apply**. These are manual, per-port choices; connected consoles are not automatically detected. The tile keeps launching the same HDMI input. Cancel discards pending changes, and Reset Defaults clears device choices when saved.

The shelf displays larger artwork with bundled brand logos for PS5, PS4, Xbox, Nintendo Switch, and the streaming apps in the default catalog (including Netflix). These logos work offline. Other installed apps use icons supplied by webOS when accessible; missing or unreadable icons fall back to a readable app name.

Some newer webOS releases block Developer Mode apps from listing installed apps. On those TVs, a one-time on-screen prompt asks to allow Free My TV; accept it so your installed apps appear in Customize.

| Setting | What It Does |
|---|---|
| **App Shelf Selector** | Auto-discovers apps installed on your TV (`listLaunchPoints`) so you can pick up to 8 favorites for your glass dock. |
| **City Name** | Type any city (e.g., `São Paulo`, `Lisbon`, `New York`) for live Open-Meteo weather and accurate local sunset times, or leave blank for automatic IP geolocation. |
| **Theme Mode** | Choose `Auto (Follows Sunset)`, `Deep Midnight`, `Pure OLED Black`, or `Daylight Blue`. |
| **Clock Format** | Toggle between `24-Hour (20:30)` and `12-Hour (8:30 PM)` display. |
| **Performance Mode** | Choose between `Standard (Glass & Glow)` and `High Performance (60 FPS Boost)` to disable heavy backdrop filters on resource-constrained TVs. |
| **TMDB API Key** | Paste a free [TMDB API Key](https://www.themoviedb.org/settings/api) for live weekly trending movies & shows, or leave empty to use the built-in zero-key live popular feed. |

---

## 🗺️ Roadmap & Things to Come

See the full [ROADMAP.md](ROADMAP.md) for detailed technical specifications.

- [x] **v1.0 — Core 60fps Glass Engine:** Native Luna app launching, Magic Remote + D-Pad spatial nav, 1-command installer.
- [x] **v1.1 — Live Weather, Sunset Themes & On-TV Customizer:** Open-Meteo integration, TMDB + zero-key live trending feed, and interactive app shelf editor.
- [ ] **v1.2 — Deep-Linking & Quick Drawer (Next Up 🚧):** Direct movie/episode deep-linking into Netflix/YouTube/Plex, D-Pad tile reordering, native TV icon extraction, and multi-language support (`EN`, `PT-BR`, `ES`, `DE`, `FR`).
- [ ] **v1.3 — OLED Care Screensaver & Wake-on-LAN 📅:** Built-in pixel-shifting 4K ambient screensaver and automatic Wake-on-LAN packet sender to wake your gaming PC when selecting HDMI.
- [ ] **v1.4 — Official Homebrew Repo & Home Button Hook 🚀:** One-click installation from the `webosbrew.org` on-TV store and optional physical Home button binding for rooted TVs.
- [ ] **v2.0 — Smartphone QR Companion & Smart Home Hub 🌟:** Scan a QR code to configure settings from your phone and trigger Home Assistant lighting webhooks.

---

## 🛠️ How It Works

```
free-my-webos/
├── app/
│   ├── appinfo.json       # webOS package manifest & permissions
│   ├── index.html         # Self-contained 60fps Glass UI, Weather, TMDB & Luna bridge
│   ├── webOSTV.js         # Official LG webOS JavaScript service library
│   └── assets/            # App icons & splash screens
├── dist/
│   └── org.webos.freemytv_1.2.5_all.ipk
├── docs/                  # Live preview & visual assets
└── scripts/
    ├── build.py           # Cross-platform .ipk compiler (ares-package + pure Python fallback)
    └── install.py         # Automated SSDP TV discovery, SSH key pairing & Luna installer
```

- **Zero Framework Bloat:** Written in pure, hardware-accelerated HTML5, CSS3, and vanilla JavaScript. The entire `.ipk` package is under **80 KB**.
- **Direct Luna Bus IPC:** Calls `luna://com.webos.applicationManager/launch` directly from the TV's local web engine (with automatic fallback to `luna://org.webosbrew.hbchannel.service/exec`).

---

## 🤝 Credits & License

- Inspired by [simbasjungles/free-my-tv](https://github.com/simbasjungles/free-my-tv) (for Google TV).
- Built for the [webOS Homebrew](https://webosbrew.org/) and LG TV community.
- Weather data by [Open-Meteo](https://open-meteo.com/) · Movie metadata by [TMDB](https://www.themoviedb.org/) & [TVMaze](https://www.tvmaze.com/).

Released under the [MIT License](LICENSE). Fork it, vibe code it, make your TV yours.

---
---

<div align="center">

<img src="docs/assets/icon-512.png" width="108" alt="Logo do Free My TV">

# Free My TV (para LG webOS)

**Uma home screen rápida, sem anúncios e a 60fps para Smart TVs LG.**

Os apps de streaming que você realmente usa em uma prateleira de vidro fosco, previsão do tempo ao vivo que acompanha o pôr do sol, e sugestões de filmes e séries em alta.<br>
Código aberto. Zero anúncios. 100% independente na TV. Sem necessidade de root.

[![License: MIT](https://img.shields.io/badge/License-MIT-0a84ff.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/LG_webOS-3.0_to_24+-30d158.svg)](#)
[![Performance](https://img.shields.io/badge/Render-60_FPS_Native-ff9f0a.svg)](#)
[![No Root](https://img.shields.io/badge/Root-Not_Required-brightgreen.svg)](#)

[**Instalar**](#-instalação-rápida-2-minutos) · [**Recursos**](#-o-que-você-ganha) · [**Personalizar**](#%EF%B8%8F-deixe-do-seu-jeito-personalização-na-tv) · [**Roadmap**](ROADMAP.md) · [**Como Funciona**](#%EF%B8%8F-como-funciona)

[**🇺🇸 English**](#free-my-tv-for-lg-webos) · **🇧🇷 Português**

<br>

<img src="docs/assets/preview.png" width="900" alt="Free My TV no LG webOS: prateleira de apps em vidro fosco, preview dinâmico, clima ao vivo e filmes em alta">

</div>

---

## ⚡ Por Que Isso Existe

O webOS moderno da LG (especialmente webOS 6, 22, 23 e 24) substituiu a clássica barra de cards rápida por um portal de tela cheia lento e cheio de:
- Banners de anúncios automáticos, promoções de compras e lixo de "Em Alta".
- Travamentos de 3 a 5 segundos toda vez que você aperta o botão Home.
- Telemetria em segundo plano e Reconhecimento Automático de Conteúdo (ACR).

**Free My TV para webOS** traz a filosofia do [simbasjungles/free-my-tv](https://github.com/simbasjungles/free-my-tv) e da Apple tvOS nativamente para as TVs LG — te dando um painel de vidro instantâneo e limpo que roda direto na memória flash interna da sua TV.

---

## ✨ O Que Você Ganha

- **🚫 Zero Anúncios. Nunca.** Sem linhas patrocinadas, sem banners promocionais, sem widgets de compras.
- **🧊 Prateleira de Apps em Vidro Fosco.** Seus apps de streaming e entradas HDMI favoritos em destaque, abrindo nativamente em ~100ms via o barramento Luna do webOS.
- **⚙️ Personalizador de Prateleira na Tela.** Detecta automaticamente os apps instalados na sua TV LG para você escolher quais aparecem na prateleira usando o controle remoto.
- **🌅 Temas Dinâmicos de Pôr do Sol e OLED.** Conecta ao Open-Meteo para mostrar o clima local ao vivo e muda automaticamente o fundo de *Azul Diurno* para *Âmbar do Pôr do Sol* até *Meia-Noite Profunda* (além de um modo *Preto OLED Puro*).
- **🎬 Abas de Filmes e Séries em Alta.** Abas separadas para filmes e séries em alta — ranqueadas pelo TMDB com sua chave opcional, ou nosso feed ao vivo sem chave (TVMaze para séries, curadoria para filmes).
- **🌤️ Gaveta de Clima e Sol.** Clique no widget de clima para ver a previsão hora a hora e os horários exatos de nascer/pôr do sol, via Open-Meteo.
- **🌑 Screensaver Seguro para OLED.** Um relógio flutuante em tela totalmente preta aparece após alguns minutos parado e muda de posição aos poucos para evitar marcação de imagem — some com qualquer tecla ou movimento do controle.
- **🎮 Suporte Completo ao Magic Remote e D-Pad.** Aponte e clique com o cursor do Magic Remote da LG, ou navegue pelos cards com as setas direcionais e a roda de rolagem.
- **💻 100% Independente na TV.** Instalado como um pacote `.ipk` nativo na sua TV. Seu computador **não** precisa ficar ligado.
- **🛡️ Seguro e Reversível.** Funciona em TVs de fábrica sem root via o Developer Mode oficial da LG (ou Homebrew Channel). Sua home screen de fábrica fica intocada.

---

## 📊 LG webOS de Fábrica vs. Free My TV

| Métrica / Recurso | LG webOS 24 de Fábrica | Free My TV (webOS) |
|---|---|---|
| **Anúncios e Banners Patrocinados** | ❌ Mais de 70% da tela | ✅ **0% (Totalmente Sem Anúncios)** |
| **Tempo de Carregamento Frio** | ❌ 3,5 a 5,0 segundos | ✅ **< 0,2 segundos** |
| **Taxa de Quadros** | ❌ Quedas de frame frequentes | ✅ **60 FPS Travados** |
| **Amigável contra Burn-in de OLED** | ❌ Banners de anúncio estáticos e claros | ✅ **Vidro Escuro e Modo OLED Puro** |
| **PC Necessário Após a Instalação** | N/A | ✅ **Não (Roda 100% na TV)** |
| **Root Necessário** | N/A | ✅ **Não (Dev Mode Oficial)** |

---

## 🚀 Instalação Rápida (2 Minutos)

Tudo que você precisa é de uma Smart TV LG (webOS 3.0+) e um computador na mesma rede Wi-Fi para a instalação inicial de 2 minutos.

### Passo 1: Ativar o Developer Mode na TV
1. Abra a **LG Content Store** na sua TV, procure por **`Developer Mode`** e instale.
2. Abra o **Developer Mode**, entre com sua conta gratuita de desenvolvedor LG ([webostv.developer.lge.com](https://webostv.developer.lge.com)) e mude o **Dev Mode Status** para **ON**.
3. Depois da TV reiniciar, abra o **Developer Mode** de novo e ative o **Key Server**. Anote o **Endereço IP** e a **Senha** de 6 caracteres mostrados na tela.

### Passo 2A: Instalação Automática em Um Comando (Recomendado)
Rode nosso instalador Python automatizado — ele descobre sua TV na rede, pareia a chave SSH, empacota o app e instala:

```bash
git clone https://github.com/danielthejoker18/FreeMyTvWebOS.git
cd FreeMyTvWebOS
python scripts/install.py
```

### Passo 2B: Instalação via Interface Gráfica (webOS Dev Manager)
1. Instale o [webOS Dev Manager](https://github.com/webosbrew/dev-manager-desktop/releases) (`winget install webosbrew.webOSDevManager` no Windows).
2. Conecte sua TV usando o IP e a Senha.
3. Baixe o [`dist/org.webos.freemytv_1.2.5_all.ipk`](dist/org.webos.freemytv_1.2.5_all.ipk) e clique em **Install .ipk**.

> [!TIP]
> **Transforme em Sua Tecla de Acesso Rápido (1 Segundo):**
> Dentro do **Free My TV** na sua TV, **segure o número `1`** (ou segure `0` para abrir o Acesso Rápido) no Magic Remote e atribua o **Free My TV** à tecla **`1`**. Agora, segurar **`1`** de qualquer lugar da TV te leva direto para o seu painel de vidro limpo em meio segundo!

---

## ⚙️ Deixe do Seu Jeito (Personalização na TV)

Clique no botão **⚙️ Customize** no canto superior direito do painel usando o controle remoto:

| Configuração | O Que Faz |
|---|---|
| **Seletor de Prateleira de Apps** | Descobre automaticamente os apps instalados na sua TV (`listLaunchPoints`) para você escolher até 8 favoritos para sua prateleira de vidro. |
| **Nome da Cidade** | Digite qualquer cidade (ex.: `São Paulo`, `Lisboa`, `Nova York`) para clima ao vivo via Open-Meteo e horários precisos de pôr do sol, ou deixe em branco para geolocalização automática por IP. |
| **Modo de Tema** | Escolha entre `Automático (Segue o Pôr do Sol)`, `Meia-Noite Profunda`, `Preto OLED Puro`, ou `Azul Diurno`. |
| **Formato do Relógio** | Alterne entre exibição em `24 Horas (20:30)` ou `12 Horas (8:30 PM)`. |
| **Modo de Performance** | Escolha entre `Padrão (Vidro & Brilho)` ou `Alta Performance (60 FPS Boost)` para desativar filtros pesados de desfoque em TVs mais modestas. |
| **Chave da API do TMDB** | Cole uma [chave gratuita da API do TMDB](https://www.themoviedb.org/settings/api) para ver filmes e séries em alta da semana ao vivo, ou deixe em branco para usar o feed ao vivo popular embutido (sem necessidade de chave). |

---

## 🗺️ Roadmap e Próximos Passos

Veja o [ROADMAP.md](ROADMAP.md) completo para as especificações técnicas detalhadas.

- [x] **v1.0 — Motor de Vidro 60fps:** Abertura nativa de apps via Luna, navegação espacial com Magic Remote + D-Pad, instalador em 1 comando.
- [x] **v1.1 — Clima ao Vivo, Temas de Pôr do Sol e Personalizador na TV:** Integração com Open-Meteo, TMDB + feed de tendências sem chave, e editor interativo da prateleira de apps.
- [ ] **v1.2 — Deep-Linking e Gaveta Rápida (Em Breve 🚧):** Deep-linking direto para filmes/episódios no Netflix/YouTube/Plex, reordenação de cards via D-Pad, extração nativa de ícones de TV, e suporte a múltiplos idiomas (`EN`, `PT-BR`, `ES`, `DE`, `FR`).
- [ ] **v1.3 — Proteção de Tela OLED e Wake-on-LAN 📅:** Protetor de tela ambiente 4K com deslocamento de pixels embutido e envio automático de pacotes Wake-on-LAN para acordar seu PC gamer ao selecionar o HDMI.
- [ ] **v1.4 — Repositório Oficial no Homebrew e Atalho do Botão Home 🚀:** Instalação em um clique pela loja na TV do `webosbrew.org` e vínculo opcional do botão físico Home para TVs com root.
- [ ] **v2.0 — Companheiro QR no Celular e Hub Smart Home 🌟:** Escaneie um QR code para configurar pelo celular e disparar webhooks de iluminação do Home Assistant.

---

## 🛠️ Como Funciona

```
free-my-webos/
├── app/
│   ├── appinfo.json       # Manifesto do pacote webOS e permissões
│   ├── index.html         # UI de vidro 60fps autocontida, clima, TMDB e ponte com o Luna
│   ├── webOSTV.js         # Biblioteca oficial de serviços JavaScript do LG webOS
│   └── assets/            # Ícones e telas de splash do app
├── dist/
│   └── org.webos.freemytv_1.2.5_all.ipk
├── docs/                  # Preview ao vivo e recursos visuais
└── scripts/
    ├── build.py           # Compilador .ipk multiplataforma (ares-package + fallback em Python puro)
    └── install.py         # Descoberta de TV via SSDP, pareamento de chave SSH e instalador via Luna
```

- **Zero Dependência de Frameworks:** Escrito em HTML5, CSS3 e JavaScript puro acelerado por hardware. O pacote `.ipk` inteiro tem menos de **80 KB**.
- **IPC Direto pelo Barramento Luna:** Chama `luna://com.webos.applicationManager/launch` diretamente do motor web local da TV (com fallback automático para `luna://org.webosbrew.hbchannel.service/exec`).

---

## 🤝 Créditos e Licença

- Inspirado por [simbasjungles/free-my-tv](https://github.com/simbasjungles/free-my-tv) (para Google TV).
- Feito para a comunidade [webOS Homebrew](https://webosbrew.org/) e de TVs LG.
- Dados de clima por [Open-Meteo](https://open-meteo.com/) · Metadados de filmes por [TMDB](https://www.themoviedb.org/) & [TVMaze](https://www.tvmaze.com/).

Lançado sob a [Licença MIT](LICENSE). Faça um fork, modifique como quiser, deixe a TV do seu jeito.
