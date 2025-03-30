# Baixador de Vídeos em Python

Este é um simples baixador de vídeos desenvolvido em Python utilizando a biblioteca `yt_dlp` para baixar vídeos, `tkinter` para a interface gráfica do usuário (GUI), `threading` para processar os downloads em segundo plano, e `os` para gerenciar o sistema de arquivos.

## Tecnologias Utilizadas

- **yt_dlp**: Biblioteca Python para baixar vídeos de diversos sites de streaming (como YouTube, Vimeo, etc.).
- **tkinter**: Framework de interface gráfica do Python utilizado para criar a GUI.
- **threading**: Módulo para gerenciar o download de vídeos de forma assíncrona, permitindo que o usuário interaja com a interface enquanto o vídeo está sendo baixado.
- **os**: Módulo utilizado para realizar operações no sistema de arquivos, como salvar o vídeo em um diretório específico.

## Funcionalidades

- Baixar vídeos de várias plataformas de streaming.
- Interface gráfica simples e intuitiva para o usuário.
- Suporte a downloads simultâneos com a ajuda de threads.
- Exibição de progresso durante o download.

### Requisitos

- Python 3.x
- Bibliotecas Python: `yt_dlp`, `tkinter`, `threading`, `os`

### Instalação

1. Clone o repositório ou baixe os arquivos do projeto.
2. Instale as dependências necessárias com o seguinte comando:

```bash
pip install yt-dlp
```
3. Caso o tkinter não esteja instalado (ele é geralmente instalado com o Python), execute:

```bash
pip install tk
```
### Executando o Baixador

Para rodar o programa, basta executar o script Python principal. Abra o terminal ou prompt de comando, navegue até o diretório onde o arquivo está localizado e execute:

```bash
python baixador_videos.py
```

A interface gráfica será exibida, permitindo que você insira o link do vídeo que deseja baixar. Após inserir o link, clique no botão para iniciar o download. O progresso será mostrado e o vídeo será salvo no diretório padrão ou em um local especificado.
<br/>

### Exemplo de Uso
1. Insira o link do vídeo na caixa de texto.

2. Selecione o diretório de destino (opcional).

3. Clique no botão "Baixar Vídeo".

O vídeo será baixado em segundo plano, e o progresso será exibido na interface.
<br/>

### Como Funciona
O programa usa a biblioteca yt_dlp para baixar o vídeo. Quando o usuário fornece o link, o script cria uma thread para o download para que a interface gráfica não congele. O progresso do download é atualizado em tempo real na interface, permitindo uma experiência de usuário suave.
<br/>

### Contribuições
Sinta-se à vontade para contribuir com melhorias ou sugestões! Você pode abrir um pull request ou issue.
<br/>

### Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.