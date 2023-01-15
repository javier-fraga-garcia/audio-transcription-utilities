# Funciones para audio y vídeo (en desarrollo) 

Repositorio con funciones para trabajar con archivos de vídeo o audio y convertirlos a texto utilizando [Whisper](https://openai.com/blog/whisper/). 

## Setup

Pasos previos para configurar el entorno:

* Instalar PyTube &rarr; `pip install pytube`
* Instalar Whisper &rarr; `pip install git+https://github.com/openai/whisper.git`
* Instanciar el modelo de Whisper deseado `model = whisper.load_model('medium')`. Consultar modelos disponibles y rendimiento en este [enlace](https://github.com/openai/whisper#available-models-and-languages)