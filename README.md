<div align="center">

<img src="https://img.shields.io/badge/macOS-Sequoia-black?style=for-the-badge&logo=apple&logoColor=white" />
<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/yt--dlp-powered-FF0000?style=for-the-badge&logo=youtube&logoColor=white" />
<img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" />

<br />
<br />

```
██╗   ██╗██╗██████╗ ███████╗ ██████╗
██║   ██║██║██╔══██╗██╔════╝██╔═══██╗
██║   ██║██║██║  ██║█████╗  ██║   ██║
╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║
 ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝
  ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝
██████╗ ██████╗  ██████╗ ██████╗ ██████╗ ███████╗██████╗
██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║  ██║██████╔╝██║   ██║██████╔╝██████╔╝█████╗  ██████╔╝
██║  ██║██╔══██╗██║   ██║██╔═══╝ ██╔═══╝ ██╔══╝  ██╔══██╗
██████╔╝██║  ██║╚██████╔╝██║     ██║     ███████╗██║  ██║
╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝
```

### 🎬 Baixador de vídeos para macOS com visual estilo Apple
**YouTube · TikTok · Instagram · Twitter/X · Facebook · Vimeo · +500 sites**

*Made with ❤️ by [Hellcath](https://github.com/Hellcath)*

<br/>

</div>

---

## ✨ O que é o VideoDropper?

O **VideoDropper** é um app gratuito e open source para macOS que permite baixar vídeos de qualquer site — YouTube, TikTok, Instagram e mais de 500 outros — com uma interface limpa e moderna no estilo Apple. Sem anúncios, sem cadastro, sem complicação.

Cole o link → escolha o formato → baixe. Simples assim.

<br/>

## 🚀 Instalação

### Pré-requisitos

Antes de tudo, você precisa ter o **Python 3** no seu Mac.

**Verificar se já tem:**
```bash
python3 --version
```
Se aparecer `Python 3.x.x` você já tem. Se não aparecer, [baixe aqui](https://www.python.org/downloads/).

---

### Passo 1 — Baixe o VideoDropper

Clique em **Releases** no canto direito desta página e baixe o arquivo `VideoDropper.zip` mais recente.

Depois de baixar, **clique duas vezes** no `.zip` para descompactar.

---

### Passo 2 — Abra o Terminal

Pressione **⌘ Espaço**, digite `Terminal` e pressione **Enter**.

---

### Passo 3 — Rode o instalador

Cole o comando abaixo no Terminal e pressione **Enter**:

```bash
cd ~/Downloads/VideoDropper && bash instalar.sh
```

O instalador vai fazer tudo automaticamente:
- ✅ Verificar o Python
- ✅ Instalar o `yt-dlp` (motor de download)
- ✅ Instalar o `ffmpeg` (necessário para alta qualidade)
- ✅ Criar o `VideoDropper.app` em `~/Applications`
- ✅ Criar um atalho na sua Área de Trabalho

---

### Passo 4 — Abrir o app

Clique duas vezes no **VideoDropper** na sua Área de Trabalho ou em `~/Applications`.

> ⚠️ **Apareceu um aviso de segurança?** Isso é normal para apps fora da App Store.
> Clique com o botão **direito** → **"Abrir"** → **"Abrir assim mesmo"**.
> Você só precisa fazer isso uma única vez.

<br/>

## 🎯 Como usar

```
1. Abra o VideoDropper
2. Cole o link do vídeo no campo (⌘V)
3. Escolha o formato:
      🎬 MP4  →  baixa o vídeo completo
      🎵 MP3  →  extrai só o áudio
4. Selecione a qualidade: Melhor / 1080p / 720p / 480p
5. Clique em  ⬇ Baixar Vídeo
6. Aguarde — a pasta de Downloads abre sozinha ao terminar!
```

<br/>

## 🌐 Sites suportados

| Plataforma | Suporte |
|---|---|
| YouTube | ✅ Vídeos, Shorts e Playlists |
| TikTok | ✅ Completo |
| Instagram | ✅ Reels, Posts e Stories públicos |
| Twitter / X | ✅ Completo |
| Facebook | ✅ Vídeos públicos |
| Vimeo | ✅ Completo |
| Twitch | ✅ Clips e VODs |
| Reddit | ✅ Completo |
| SoundCloud | ✅ Áudio |
| **+500 outros** | ✅ Via yt-dlp |

Veja a lista completa em [yt-dlp/supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

<br/>

## ❓ Problemas comuns

<details>
<summary><b>🔴 "App não abre" ou aviso de segurança do macOS</b></summary>
<br>

O macOS bloqueia apps que não vieram da App Store por padrão. Para resolver:

1. Clique com o botão **direito** no `VideoDropper.app`
2. Selecione **"Abrir"**
3. Clique em **"Abrir assim mesmo"**

Você só precisa fazer isso **uma vez**.
</details>

<details>
<summary><b>🔴 "yt-dlp não encontrado" ao abrir o app</b></summary>
<br>

Abra o Terminal e rode:
```bash
pip3 install --upgrade yt-dlp
```
Depois feche e abra o VideoDropper novamente.
</details>

<details>
<summary><b>🔴 Vídeo baixa sem áudio ou com qualidade ruim</b></summary>
<br>

O `ffmpeg` é necessário para juntar vídeo e áudio em alta qualidade. Instale assim:

```bash
# 1. Instalar o Homebrew (gerenciador de pacotes do macOS):
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Instalar o ffmpeg:
brew install ffmpeg
```
</details>

<details>
<summary><b>🔴 Erro ao baixar vídeo privado ou com restrição de idade</b></summary>
<br>

Vídeos privados ou com restrição de idade exigem autenticação. O VideoDropper funciona apenas com **vídeos públicos**.
</details>

<details>
<summary><b>🔴 O download está muito lento</b></summary>
<br>

Vídeos em 4K são muito pesados. Tente selecionar **720p** ou **480p** para downloads mais rápidos. A velocidade também depende da sua conexão com a internet.
</details>

<br/>

## 🛠️ Tecnologias

| Tecnologia | O que faz |
|---|---|
| [Python 3](https://python.org) | Linguagem principal do app |
| [Tkinter](https://docs.python.org/3/library/tkinter.html) | Interface gráfica |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Motor de download (suporta 500+ sites) |
| [ffmpeg](https://ffmpeg.org) | Merge e conversão de vídeo/áudio |

<br/>

## 📁 Estrutura do projeto

```
VideoDropper/
├── VideoDropper.py    # App principal — interface e toda a lógica
├── instalar.sh        # Script de instalação automática para macOS
└── README.md          # Este arquivo
```

<br/>

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Se quiser melhorar o VideoDropper:

1. Faça um **Fork** deste repositório
2. Crie uma nova branch: `git checkout -b minha-melhoria`
3. Faça suas alterações e commite: `git commit -m 'Adiciona funcionalidade X'`
4. Envie: `git push origin minha-melhoria`
5. Abra um **Pull Request** e descreva o que você fez

Tem uma ideia mas não sabe programar? Sem problema — abre uma [Issue](../../issues) descrevendo o que você quer!

<br/>

## 📄 Licença

Este projeto está sob a licença **MIT** — pode usar, modificar e distribuir à vontade, desde que mantenha os créditos ao autor original.

```
MIT License — Copyright (c) 2026 Hellcath
```

<br/>

---

<div align="center">

**Se o projeto te ajudou, deixa uma ⭐ — significa muito!**

*Feito com ❤️ por [Hellcath](https://github.com/Hellcath)*

</div>
