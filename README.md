# Documentação do Sistema de Notificação

## Visão Geral do Sistema

O sistema de notificação é um microserviço projetado para lidar com o envio de mensagens e notificações através de diferentes canais, como e-mail e push. Ele foi desenvolvido para ser escalável, modular e fácil de integrar com outras aplicações, utilizando boas práticas de arquitetura e design de software. Para este projeto utilizou-se como padrão o Template Method onde processos comuns são desempenhados por mais de uma funcionalidade.

### Principais Funcionalidades

- **Envio de Notificações por E-mail:** Permite o envio de mensagens para endereços de e-mail especificados, com suporte a conteúdo dinâmico e formatos variados.
- **Envio de Notificações Push:** Envia mensagens push para dispositivos ou serviços que suportem esse formato de notificação.
- **Integração com Filas:** Escuta mensagens de filas para processar e disparar as notificações de forma eficiente.
- **Design Modular:** Componentes separados para diferentes responsabilidades, como infraestrutura, interfaces e lógica de negócio.

### Tecnologias Utilizadas

- **Python**: Linguagem principal para o desenvolvimento do sistema.
- **Docker**: Para containerização e facilitação da implantação.
- **Filas de Mensagens**: Utiliza uma solução de fila para gerenciar tarefas assíncronas (RabbitMQ).
- **SMTP e APIs Push**: Para envio de e-mails (MailHog) e mensagens push (Mercure), respectivamente.

## Descrição dos Módulos

### Diretório: `notification_service`

Este é o diretório principal contendo a implementação do serviço de notificação.

#### Submódulo: `message_listener`

Responsável por escutar mensagens em filas e acionar os mecanismos apropriados para envio de notificações.

- **Pasta `infrastructure`:** Contém a implementação dos serviços de notificação:
  - **`email_notification.py`:** Implementação para envio de e-mails utilizando protocolos SMTP ou serviços de terceiros.
  - **`push_notification.py`:** Implementação para envio de notificações push via APIs de provedores.

- **Pasta `interfaces`:** Define interfaces e abstrações utilizadas para integrar os serviços de notificação com outras partes do sistema:
  - **`notification_service.py`:** Define os métodos e contratos para enviar notificações e gerenciar comunicações entre módulos.

### Configuração e Dependências

- **`requirements.txt`:** Lista as dependências do Python necessárias para o funcionamento do sistema.
- **`.env`:** Arquivo de variáveis de ambiente que contém informações sensíveis, como credenciais de acesso e URLs de serviços externos.

### Outros Arquivos Relevantes

- **`docker-compose-services.yml`:** Arquivo de configuração para orquestração de containers, facilitando o ambiente de desenvolvimento e produção.
- **`listen_queue.py`:** Script principal que inicializa o listener de fila para processar mensagens e disparar notificações.

## Guia de Instalação e Uso

### Pré-requisitos

1. **Docker e Docker Compose:** Certifique-se de que estão instalados e configurados.
2. **Python 3.8+**: Necessário para executar scripts localmente.
3. **Ferramenta de Gerenciamento de Filas:** Como RabbitMQ ou outra solução compatível.

### Passos de Instalação

1. **Clonar o Repositório:**

   ```bash
   git clone <url-do-repositorio>
   cd notification
   ```

2. **Configurar Variáveis de Ambiente:**
   - Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

     ```env
      HUB_URL=http://localhost:80/.well-known/mercure
      MERCURE_PUBLISHER_JWT_KEY=!ChangeThisPublisherKey!
      MERCURE_SUBSCRIBER_JWT_KEY=!ChangeThisSubscriberKey!
      MERCURE_TOPIC= http://example.com/my-topic
      SMTP_SERVER=localhost
      SMTP_PORT=1025
      SENDER_MAIL=no-reply@example.com
      RABBITMQ_HOST=localhost
      RABBITMQ_USER=user
      RABBITMQ_PASS=password
      ROUTING_KEYS=notification.email,notification.status
     ```

3. **Instalar Dependências:**
   Criar um ambiente virtual:

   ```bash
   virtualenv .venv

   ```

   Ativar o ambiente virtual

   ```bash
   source .venv/bin/activate
   ```

   Caso deseje executar localmente, utilize:

   ```bash
   pip install -r python/requirements.txt
   ```

4. **Iniciar os Serviços:**
   Utilize o Docker Compose para iniciar os serviços necessários:

   ```bash
   docker-compose -f docker-compose-services.yml up --build
   ```

### Uso

Em terminais separados e com os serviços já iniciados, seguir os seguintes passos:

1. **Iniciar o Listener:**
   O listener é responsável por processar mensagens na fila:

   ```bash
   python python/listen_queue.py
   ```

2. **Consumir Push Notifications:**
   - Receber push notifications:

   ```bash
   python python/test/listen_mercure.py
   ```

3. **Verificar e-mails:**
   - Abrir o browser no seguinte endereço: <http://localhost:8025>

4. **Enviar Mensagens para a Fila:**
   - Utilizar do script `python` no diretório `test`:

   ```bash
    python python/test/send_message.py
   ```

5. **Verificar Logs (Opcional):**
   - Monitore os logs para garantir que as notificações estão sendo enviadas corretamente.

   ```bash
   docker logs -f <nome-do-container>
   ```
