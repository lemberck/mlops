# Docker

## Alguns comandos úteis

### Imagens
- `docker build -t <image> .` - Cria uma imagem a partir de um Dockerfile
- `docker build -f <dockerfile> -t <image> .` - Cria uma imagem a partir de um Dockerfile específico
- `docker images` - Lista as imagens
- `docker rmi <id_imagem>` - Remove uma imagem

### Contêineres
- `docker ps` - Lista os containers em execução
- `docker ps -a` - Lista todos os containers
- `docker run <image>` - Executa uma imagem
- `docker run -it <image> bash` - cria um container e executa o bash
- `docker run -d <image>` - Executa uma imagem em background
- `docker run -p <porta_host>:<porta_container> <image>` - Executa uma imagem e mapeia a porta do container para a porta do host
- `docker rm <id_contêiner>` - Remove um container