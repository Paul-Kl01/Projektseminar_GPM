FROM python:3.11.6

RUN apt-get update && apt-get install -y git
RUN pip install gradio
RUN pip install matplotlib


RUN git clone https://github.com/MaxGit32/Projektseminar_GPM_Huggingface.git
CMD ["mkdir","Mathplot"]

WORKDIR ./Projektseminar_GPM_Huggingface


CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "7860"]
