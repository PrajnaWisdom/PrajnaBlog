FROM registry.cn-beijing.aliyuncs.com/k8s-webot/base:python36

ENV LANG=C.UTF-8 C_FORCE_ROOT=true


WORKDIR /app
ENV ANNOY_COMPILER_ARGS -mtune=native
RUN export PYTHONIOENCODING=utf8
RUN pip3 install --upgrade pip -i https://pypi.douban.com/simple
COPY requirements.txt /app
RUN pip3 install --no-cache-dir  -r requirements.txt -i https://pypi.douban.com/simple
COPY . /app
CMD uvicorn main:app --host 0.0.0.0
