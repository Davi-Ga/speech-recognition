# Projeto de Reconhecimento de Fala com a API do Azure

Este projeto utiliza a API de Reconhecimento de Fala do Azure para transcrever áudio em texto. Ele é desenvolvido em Python e faz uso da biblioteca `azure-cognitiveservices-speech` para interagir com os serviços de fala do Azure.

## Pré-requisitos

Antes de começar, certifique-se de ter:

1. Uma conta no Azure.
2. Uma chave de API do Azure Speech Service.
3. O SDK do Azure Speech instalado em seu ambiente Python.

## Instalação

1. Clone este repositório para o seu ambiente local:

    ```sh
    git clone https://github.com/Davi-Ga/speech-recognition.git
    cd speech-recognition
    ```

2. Crie um ambiente virtual (opcional, mas recomendado):

    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows use: venv\Scripts\activate
    ```

3. Instale as dependências necessárias:

    ```sh
    pip install -r requirements.txt
    ```

## Configuração

1. Obtenha a chave de API do Azure Speech e a região do seu serviço. Você pode encontrar essas informações no portal do Azure, na seção de recursos de Speech.

2. Crie um arquivo `.env` na raiz do projeto e adicione suas credenciais da seguinte forma:

    ```env
    SUBSCRIPTION_KEY=your_speech_key
    SERVICE_REGION=your_service_region
    ```

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para obter mais detalhes.

## Referências

- [Documentação do Azure Speech Service](https://docs.microsoft.com/azure/cognitive-services/speech-service/)
- [SDK do Azure para Python](https://pypi.org/project/azure-cognitiveservices-speech/)

