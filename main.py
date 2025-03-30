import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading
import os

# Tema escuro
BACKGROUND_COLOR = "#2e2e2e"
FOREGROUND_COLOR = "#ffffff"
BUTTON_COLOR = "#4CAF50"

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader Avançado (yt-dlp GUI)")
        self.root.geometry("700x650")
        self.root.resizable(False, False)
        self.root.configure(bg=BACKGROUND_COLOR)

        self.pause_flag = threading.Event()
        self.pause_flag.set()  # Inicia sem estar pausado

        self.pasta_destino = tk.StringVar()
        self.var_playlist = tk.BooleanVar()

        self.build_ui()

    def build_ui(self):
        # Links
        tk.Label(self.root, text="Cole os links dos vídeos (um por linha):", bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR).pack(anchor='w', padx=10, pady=(10, 0))
        self.entrada_links = scrolledtext.ScrolledText(self.root, height=8, wrap=tk.WORD, bg="#3c3f41", fg=FOREGROUND_COLOR, insertbackground=FOREGROUND_COLOR)
        self.entrada_links.pack(padx=10, fill='x')

        # Pasta destino
        tk.Label(self.root, text="Pasta de destino:", bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR).pack(anchor='w', padx=10, pady=(10, 0))
        frame_pasta = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        frame_pasta.pack(padx=10, fill='x')
        tk.Entry(frame_pasta, textvariable=self.pasta_destino, bg="#3c3f41", fg=FOREGROUND_COLOR, insertbackground=FOREGROUND_COLOR).pack(side='left', fill='x', expand=True)
        tk.Button(frame_pasta, text="Escolher...", command=self.escolher_pasta, bg=BUTTON_COLOR, fg="white").pack(side='left', padx=5)

        # Qualidade
        tk.Label(self.root, text="Qualidade desejada:", bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR).pack(anchor='w', padx=10, pady=(10, 0))
        self.combo_qualidade = ttk.Combobox(self.root, values=["Melhor (MP4)", "720p", "1080p", "Somente Áudio (MP3)"])
        self.combo_qualidade.current(0)
        self.combo_qualidade.pack(padx=10, fill='x')

        # Playlist
        check_playlist = tk.Checkbutton(self.root, text="Baixar playlist completa (se aplicável)", variable=self.var_playlist, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, selectcolor=BACKGROUND_COLOR)
        check_playlist.pack(anchor='w', padx=10, pady=(5, 10))

        # Botões
        frame_botoes = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        frame_botoes.pack(padx=10, fill='x')
        tk.Button(frame_botoes, text="Baixar Vídeos", command=self.iniciar_download, bg=BUTTON_COLOR, fg="white", height=2).pack(side='left', fill='x', expand=True)
        tk.Button(frame_botoes, text="Pausar", command=self.pausar_downloads, bg="#f39c12", fg="white", height=2).pack(side='left', padx=5)
        tk.Button(frame_botoes, text="Retomar", command=self.retornar_downloads, bg="#3498db", fg="white", height=2).pack(side='left')

        # Barra de progresso
        tk.Label(self.root, text="Progresso:", bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR).pack(anchor='w', padx=10, pady=(10, 0))
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(padx=10, fill='x')

        # Caixa de status
        tk.Label(self.root, text="Status:", bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR).pack(anchor='w', padx=10)
        self.caixa_status = scrolledtext.ScrolledText(self.root, height=12, state='disabled', wrap=tk.WORD, bg="#3c3f41", fg=FOREGROUND_COLOR, insertbackground=FOREGROUND_COLOR)
        self.caixa_status.pack(padx=10, fill='both', expand=True, pady=(0, 10))

    def escolher_pasta(self):
        caminho = filedialog.askdirectory()
        if caminho:
            self.pasta_destino.set(caminho)

    def atualizar_status(self, mensagem):
        self.caixa_status.config(state='normal')
        self.caixa_status.insert(tk.END, mensagem + "\n")
        self.caixa_status.see(tk.END)
        self.caixa_status.config(state='disabled')

    def iniciar_download(self):
        raw_links = self.entrada_links.get("1.0", tk.END).strip()
        links = [l for l in raw_links.splitlines() if l.strip() != ""]

        if not links:
            messagebox.showwarning("Aviso", "Por favor, cole ao menos um link.")
            return

        destino = self.pasta_destino.get()
        if not destino:
            messagebox.showwarning("Aviso", "Por favor, selecione uma pasta de destino.")
            return

        qualidade = self.combo_qualidade.get()
        incluir_playlist = self.var_playlist.get()

        # Limpar status e progresso
        self.caixa_status.config(state='normal')
        self.caixa_status.delete(1.0, tk.END)
        self.caixa_status.config(state='disabled')
        self.progress_var.set(0)

        thread = threading.Thread(target=self.baixar_videos, args=(links, destino, qualidade, incluir_playlist))
        thread.start()

    def baixar_videos(self, links, destino, qualidade, incluir_playlist):
        if qualidade == "Melhor (MP4)":
            formato = 'best[ext=mp4][vcodec^=avc1][acodec^=mp4a]/best[ext=mp4]'
            merge_format = 'mp4'
            postprocessors = []
        elif qualidade == "720p":
            formato = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]'
            merge_format = 'mp4'
            postprocessors = []
        elif qualidade == "1080p":
            formato = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]'
            merge_format = 'mp4'
            postprocessors = []
        elif qualidade == "Somente Áudio (MP3)":
            formato = 'bestaudio/best'
            merge_format = 'mp3'
            postprocessors = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            formato = 'best'
            merge_format = 'mp4'
            postprocessors = []

        total = len(links)
        opcoes = {
            'format': formato,
            'outtmpl': os.path.join(destino, '%(title)s.%(ext)s'),
            'merge_output_format': merge_format,
            'ffmpeg_location': 'ffmpeg',
            'noplaylist': not incluir_playlist,
            'quiet': True,
            'postprocessors': postprocessors,
            'progress_hooks': [self.progresso_hook],
        }

        with yt_dlp.YoutubeDL(opcoes) as ydl:
            for i, link in enumerate(links, 1):
                self.pause_flag.wait()  # Aguarda se pausado
                try:
                    self.atualizar_status(f'⬇️ Baixando ({i}/{total}): {link.strip()}')
                    ydl.download([link.strip()])
                    self.atualizar_status(f'✅ Concluído ({i}/{total}): {link.strip()}')
                except Exception as e:
                    self.atualizar_status(f'❌ Erro com {link.strip()}: {e}')

        self.atualizar_status("🚀 Todos os downloads foram concluídos.")
        self.progress_var.set(100)

    def progresso_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0.0%').strip().replace('%', '')
            try:
                self.progress_var.set(float(percent))
            except:
                pass

    def pausar_downloads(self):
        self.pause_flag.clear()
        self.atualizar_status("⏸️ Download pausado.")

    def retornar_downloads(self):
        self.pause_flag.set()
        self.atualizar_status("▶️ Download retomado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
