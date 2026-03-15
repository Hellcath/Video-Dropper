#!/usr/bin/env python3
"""
VideoDropper — Baixador de vídeos estilo Apple para macOS
Suporta YouTube, TikTok e muito mais via yt-dlp
"""

import tkinter as tk
from tkinter import ttk, filedialog
import threading
import subprocess
import sys
import os
import re
from pathlib import Path

# ──────────────────────────────────────────
#  Paleta Apple / macOS Sequoia
# ──────────────────────────────────────────
BG           = "#1C1C1E"      # systemBackground (dark)
SURFACE      = "#2C2C2E"      # secondarySystemBackground
SURFACE2     = "#3A3A3C"      # tertiarySystemBackground
ACCENT       = "#0A84FF"      # systemBlue
ACCENT_HOVER = "#409CFF"
SUCCESS      = "#30D158"      # systemGreen
WARNING      = "#FF9F0A"      # systemOrange
ERROR        = "#FF453A"      # systemRed
TEXT_PRI     = "#FFFFFF"
TEXT_SEC     = "#8E8E93"
TEXT_TER     = "#48484A"
BORDER       = "#38383A"

FONT_TITLE   = ("SF Pro Display", 22, "bold")
FONT_BODY    = ("SF Pro Text", 13)
FONT_SMALL   = ("SF Pro Text", 11)
FONT_TINY    = ("SF Pro Text", 10)
FONT_MONO    = ("SF Mono", 11)

def check_yt_dlp():
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_yt_dlp():
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "--upgrade", "yt-dlp"],
            check=True, capture_output=True
        )
        return True
    except Exception:
        try:
            subprocess.run(
                ["brew", "install", "yt-dlp"],
                check=True, capture_output=True
            )
            return True
        except Exception:
            return False

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=160, height=38,
                 bg=ACCENT, fg=TEXT_PRI, hover_bg=ACCENT_HOVER,
                 font=FONT_BODY, radius=12, **kwargs):
        super().__init__(parent, width=width, height=height,
                         bg=parent["bg"], highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg
        self.hover_color = hover_bg
        self.fg = fg
        self.radius = radius
        self.text = text
        self.font = font
        self._draw(bg)
        self.bind("<Enter>", lambda e: self._draw(hover_bg))
        self.bind("<Leave>", lambda e: self._draw(bg))
        self.bind("<Button-1>", lambda e: self._click())

    def _round_rect(self, x1, y1, x2, y2, r, **kw):
        pts = [
            x1+r, y1,  x2-r, y1,
            x2, y1,    x2, y1+r,
            x2, y2-r,  x2, y2,
            x2-r, y2,  x1+r, y2,
            x1, y2,    x1, y2-r,
            x1, y1+r,  x1, y1,
            x1+r, y1,
        ]
        return self.create_polygon(pts, smooth=True, **kw)

    def _draw(self, color):
        self.delete("all")
        w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        self._round_rect(1, 1, w-1, h-1, self.radius, fill=color, outline="")
        self.create_text(w//2, h//2, text=self.text,
                         fill=self.fg, font=self.font)

    def _click(self):
        if self.command:
            self.command()

    def configure_text(self, text):
        self.text = text
        self._draw(self.bg_color)

class ProgressBar(tk.Canvas):
    def __init__(self, parent, width=400, height=4, **kwargs):
        super().__init__(parent, width=width, height=height,
                         bg=SURFACE2, highlightthickness=0, **kwargs)
        self._value = 0
        self._width = width
        self._draw()

    def _round_rect(self, x1, y1, x2, y2, r, **kw):
        r = min(r, (y2-y1)//2)
        pts = [
            x1+r, y1,  x2-r, y1,
            x2, y1,    x2, y1+r,
            x2, y2-r,  x2, y2,
            x2-r, y2,  x1+r, y2,
            x1, y2,    x1, y2-r,
            x1, y1+r,  x1, y1,
            x1+r, y1,
        ]
        return self.create_polygon(pts, smooth=True, **kw)

    def _draw(self):
        self.delete("all")
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        # track
        self._round_rect(0, 0, w, h, h//2, fill=SURFACE2, outline="")
        # fill
        fill_w = int(w * self._value / 100)
        if fill_w > 2:
            self._round_rect(0, 0, fill_w, h, h//2, fill=ACCENT, outline="")

    def set(self, value):
        self._value = max(0, min(100, value))
        self._draw()

class VideoDropperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VideoDropper")
        self.resizable(False, False)
        self.configure(bg=BG)

        # Estado
        self.download_dir = str(Path.home() / "Downloads")
        self.is_downloading = False
        self.process = None

        # Centralizar janela
        w, h = 520, 580
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        self._build_ui()
        self._check_deps()

    # ── UI ──────────────────────────────────
    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=28, pady=(32, 0))

        # Ícone
        icon_canvas = tk.Canvas(header, width=52, height=52,
                                bg=BG, highlightthickness=0)
        icon_canvas.pack(side="left")
        self._draw_icon(icon_canvas)

        title_frame = tk.Frame(header, bg=BG)
        title_frame.pack(side="left", padx=14)
        tk.Label(title_frame, text="VideoDropper",
                 font=FONT_TITLE, bg=BG, fg=TEXT_PRI).pack(anchor="w")
        tk.Label(title_frame, text="YouTube · TikTok · Instagram · e mais",
                 font=FONT_SMALL, bg=BG, fg=TEXT_SEC).pack(anchor="w")

        # Separador
        sep = tk.Frame(self, height=1, bg=BORDER)
        sep.pack(fill="x", padx=28, pady=20)

        # Card principal
        card = tk.Frame(self, bg=SURFACE, highlightbackground=BORDER,
                        highlightthickness=1)
        card.pack(fill="x", padx=28)
        self._add_rounded_border(card)

        inner = tk.Frame(card, bg=SURFACE)
        inner.pack(fill="x", padx=20, pady=20)

        # Label URL
        tk.Label(inner, text="Link do vídeo",
                 font=("SF Pro Text", 12, "bold"),
                 bg=SURFACE, fg=TEXT_SEC).pack(anchor="w", pady=(0, 8))

        # Entry URL
        entry_frame = tk.Frame(inner, bg=SURFACE2,
                               highlightbackground=BORDER, highlightthickness=1)
        entry_frame.pack(fill="x")

        self.url_var = tk.StringVar()
        self.url_var.trace_add("write", self._on_url_change)
        self.url_entry = tk.Entry(
            entry_frame, textvariable=self.url_var,
            font=FONT_BODY, bg=SURFACE2, fg=TEXT_PRI,
            insertbackground=ACCENT, relief="flat",
            bd=0
        )
        self.url_entry.pack(side="left", fill="x", expand=True,
                            padx=14, pady=10)

        self.clear_btn = tk.Label(entry_frame, text="✕",
                                  font=FONT_SMALL, bg=SURFACE2,
                                  fg=TEXT_SEC, cursor="hand2")
        self.clear_btn.pack(side="right", padx=10)
        self.clear_btn.bind("<Button-1>", lambda e: self._clear_url())
        self.clear_btn.pack_forget()

        # Formato
        fmt_frame = tk.Frame(inner, bg=SURFACE)
        fmt_frame.pack(fill="x", pady=(16, 0))

        tk.Label(fmt_frame, text="Formato",
                 font=("SF Pro Text", 12, "bold"),
                 bg=SURFACE, fg=TEXT_SEC).pack(anchor="w", pady=(0, 8))

        radio_row = tk.Frame(fmt_frame, bg=SURFACE)
        radio_row.pack(fill="x")

        self.format_var = tk.StringVar(value="mp4")
        formats = [("🎬  Vídeo MP4", "mp4"), ("🎵  Áudio MP3", "mp3")]
        for label, val in formats:
            btn = tk.Radiobutton(
                radio_row, text=label, variable=self.format_var,
                value=val, font=FONT_BODY,
                bg=SURFACE, fg=TEXT_PRI,
                selectcolor=SURFACE, activebackground=SURFACE,
                activeforeground=TEXT_PRI,
                indicatoron=True,
                command=self._on_format_change
            )
            btn.pack(side="left", padx=(0, 24))

        # Qualidade
        self.quality_frame = tk.Frame(inner, bg=SURFACE)
        self.quality_frame.pack(fill="x", pady=(12, 0))

        tk.Label(self.quality_frame, text="Qualidade",
                 font=("SF Pro Text", 12, "bold"),
                 bg=SURFACE, fg=TEXT_SEC).pack(anchor="w", pady=(0, 8))

        qual_row = tk.Frame(self.quality_frame, bg=SURFACE)
        qual_row.pack(fill="x")

        self.quality_var = tk.StringVar(value="best")
        qualities = [("Melhor", "best"), ("1080p", "1080"), ("720p", "720"), ("480p", "480")]
        for label, val in qualities:
            rb = tk.Radiobutton(
                qual_row, text=label, variable=self.quality_var,
                value=val, font=FONT_SMALL,
                bg=SURFACE, fg=TEXT_PRI,
                selectcolor=SURFACE, activebackground=SURFACE,
                activeforeground=TEXT_PRI, indicatoron=True
            )
            rb.pack(side="left", padx=(0, 16))

        # Pasta
        sep2 = tk.Frame(inner, height=1, bg=BORDER)
        sep2.pack(fill="x", pady=16)

        folder_row = tk.Frame(inner, bg=SURFACE)
        folder_row.pack(fill="x")

        tk.Label(folder_row, text="📁", font=("SF Pro Text", 14),
                 bg=SURFACE, fg=TEXT_SEC).pack(side="left")

        self.folder_label = tk.Label(
            folder_row, text=self._short_path(self.download_dir),
            font=FONT_SMALL, bg=SURFACE, fg=TEXT_SEC, anchor="w"
        )
        self.folder_label.pack(side="left", padx=8, fill="x", expand=True)

        change_btn = tk.Label(folder_row, text="Alterar",
                              font=("SF Pro Text", 11, "bold"),
                              bg=SURFACE, fg=ACCENT, cursor="hand2")
        change_btn.pack(side="right")
        change_btn.bind("<Button-1>", lambda e: self._choose_folder())

        # ── Botão Download ──
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(fill="x", padx=28, pady=20)

        self.dl_button = RoundedButton(
            btn_frame, text="⬇  Baixar Vídeo",
            command=self._start_download,
            width=464, height=46,
            bg=ACCENT, hover_bg=ACCENT_HOVER,
            font=("SF Pro Text", 15, "bold"),
            radius=14
        )
        self.dl_button.pack()

        # ── Progresso ──
        prog_frame = tk.Frame(self, bg=BG)
        prog_frame.pack(fill="x", padx=28)

        self.prog_bar = ProgressBar(prog_frame, width=464, height=5)
        self.prog_bar.pack()

        self.status_label = tk.Label(
            self, text="Cole um link acima e clique em Baixar",
            font=FONT_SMALL, bg=BG, fg=TEXT_SEC
        )
        self.status_label.pack(pady=(10, 0))

        self.detail_label = tk.Label(
            self, text="",
            font=FONT_TINY, bg=BG, fg=TEXT_TER
        )
        self.detail_label.pack()

        # ── Log ──
        log_frame = tk.Frame(self, bg=SURFACE, highlightbackground=BORDER,
                             highlightthickness=1)
        log_frame.pack(fill="both", expand=True, padx=28, pady=(12, 28))

        self.log_text = tk.Text(
            log_frame, height=6, font=FONT_MONO,
            bg=SURFACE, fg=TEXT_SEC, relief="flat",
            bd=0, wrap="word", state="disabled",
            insertbackground=ACCENT
        )
        self.log_text.pack(fill="both", expand=True, padx=12, pady=10)

        # Bind paste
        self.url_entry.bind("<Command-v>", lambda e: self.after(50, self._on_paste))
        self.bind("<Return>", lambda e: self._start_download())

    def _draw_icon(self, canvas):
        # Gradiente simulado com retângulo arredondado azul + seta
        canvas.create_oval(2, 2, 50, 50, fill=ACCENT, outline="")
        # Seta down
        canvas.create_polygon(
            26, 14,  26, 32,  20, 26,  26, 32,  32, 26,  26, 32,  26, 14,
            fill="white"
        )
        canvas.create_rectangle(22, 32, 30, 40, fill="white", outline="")
        canvas.create_rectangle(14, 38, 38, 43, fill="white", outline="")

    def _add_rounded_border(self, widget):
        pass  # visual via highlightbackground

    # ── Helpers ──────────────────────────────
    def _short_path(self, path):
        home = str(Path.home())
        if path.startswith(home):
            return "~" + path[len(home):]
        return path

    def _on_url_change(self, *_):
        url = self.url_var.get().strip()
        if url:
            self.clear_btn.pack(side="right", padx=10)
        else:
            self.clear_btn.pack_forget()

    def _clear_url(self):
        self.url_var.set("")
        self.url_entry.focus()

    def _on_paste(self):
        url = self.url_var.get().strip()
        if url:
            self._set_status("🔗 Link detectado! Clique em Baixar.", TEXT_SEC)

    def _on_format_change(self):
        pass  # quality always visible

    def _choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_dir)
        if folder:
            self.download_dir = folder
            self.folder_label.config(text=self._short_path(folder))

    def _set_status(self, msg, color=TEXT_SEC):
        self.status_label.config(text=msg, fg=color)

    def _set_detail(self, msg):
        self.detail_label.config(text=msg)

    def _log(self, text):
        self.log_text.config(state="normal")
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")

    # ── Deps ─────────────────────────────────
    def _check_deps(self):
        def check():
            if not check_yt_dlp():
                self._set_status("⚙ Instalando dependências... aguarde.", WARNING)
                ok = install_yt_dlp()
                if ok:
                    self._set_status("✅ Pronto! Cole um link e baixe.", SUCCESS)
                else:
                    self._set_status("❌ Erro ao instalar yt-dlp. Veja o README.", ERROR)
            else:
                self._set_status("✅ Pronto! Cole um link e baixe.", TEXT_SEC)
        threading.Thread(target=check, daemon=True).start()

    # ── Download ─────────────────────────────
    def _start_download(self):
        if self.is_downloading:
            self._cancel_download()
            return

        url = self.url_var.get().strip()
        if not url:
            self._set_status("⚠ Cole um link primeiro!", WARNING)
            self.url_entry.focus()
            return

        if not re.match(r"https?://", url):
            self._set_status("⚠ Link inválido. Deve começar com https://", ERROR)
            return

        self.is_downloading = True
        self.dl_button.text = "⛔  Cancelar"
        self.dl_button._draw(ERROR)
        self.dl_button.hover_color = "#FF6961"
        self._clear_log()
        self.prog_bar.set(0)
        self._set_status("⏳ Iniciando download...", TEXT_SEC)
        self._set_detail("")

        threading.Thread(target=self._run_download, args=(url,), daemon=True).start()

    def _run_download(self, url):
        fmt = self.format_var.get()
        quality = self.quality_var.get()
        out_dir = self.download_dir

        if fmt == "mp3":
            cmd = [
                "yt-dlp",
                "-x", "--audio-format", "mp3",
                "--audio-quality", "0",
                "-o", f"{out_dir}/%(title)s.%(ext)s",
                "--newline",
                url
            ]
        else:
            if quality == "best":
                fmt_str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
            else:
                fmt_str = f"bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}][ext=mp4]/best"
            cmd = [
                "yt-dlp",
                "-f", fmt_str,
                "--merge-output-format", "mp4",
                "-o", f"{out_dir}/%(title)s.%(ext)s",
                "--newline",
                url
            ]

        try:
            self.process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )

            for line in self.process.stdout:
                line = line.rstrip()
                if not line:
                    continue

                self.after(0, self._log, line)

                # Progresso
                if "[download]" in line and "%" in line:
                    m = re.search(r"(\d+\.?\d*)%", line)
                    if m:
                        pct = float(m.group(1))
                        self.after(0, self.prog_bar.set, pct)
                        self.after(0, self._set_status,
                                   f"⬇  Baixando... {pct:.0f}%", ACCENT)
                        # speed/ETA
                        speed_m = re.search(r"at\s+(\S+)\s", line)
                        eta_m = re.search(r"ETA\s+(\S+)", line)
                        detail = ""
                        if speed_m:
                            detail += f"Velocidade: {speed_m.group(1)}"
                        if eta_m:
                            detail += f"  ·  Tempo restante: {eta_m.group(1)}"
                        if detail:
                            self.after(0, self._set_detail, detail)

                elif "[Merger]" in line or "Merging" in line:
                    self.after(0, self._set_status, "🔧 Finalizando arquivo...", TEXT_SEC)
                    self.after(0, self.prog_bar.set, 95)

            self.process.wait()
            rc = self.process.returncode

            if rc == 0:
                self.after(0, self.prog_bar.set, 100)
                self.after(0, self._set_status,
                           "✅ Download concluído! Verifique sua pasta.", SUCCESS)
                self.after(0, self._set_detail,
                           f"Salvo em: {self._short_path(out_dir)}")
                self.after(0, self._open_folder)
            elif rc == -15:
                self.after(0, self._set_status, "⏹ Download cancelado.", TEXT_SEC)
                self.after(0, self.prog_bar.set, 0)
            else:
                self.after(0, self._set_status,
                           "❌ Erro no download. Veja o log abaixo.", ERROR)

        except FileNotFoundError:
            self.after(0, self._set_status,
                       "❌ yt-dlp não encontrado. Reinicie o app.", ERROR)
        except Exception as e:
            self.after(0, self._set_status, f"❌ Erro: {e}", ERROR)
        finally:
            self.is_downloading = False
            self.process = None
            self.after(0, self._reset_button)

    def _cancel_download(self):
        if self.process:
            self.process.terminate()

    def _reset_button(self):
        self.dl_button.text = "⬇  Baixar Vídeo"
        self.dl_button.bg_color = ACCENT
        self.dl_button.hover_color = ACCENT_HOVER
        self.dl_button._draw(ACCENT)

    def _open_folder(self):
        try:
            subprocess.Popen(["open", self.download_dir])
        except Exception:
            pass

if __name__ == "__main__":
    app = VideoDropperApp()
    app.mainloop()
