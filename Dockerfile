# --------------------------
# Docker file
# --------------------------
FROM python:3.7

# Set system language
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV FLASK_CONFIG production

# install python requirement
COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
RUN pip3 install --no-cache-dir gunicorn
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /tmp/requirements.txt

# Create root folder docker_web_app
# COPY ./webapp /docker_web_app/iodock/
WORKDIR /small/

# ENV PORT 5000
EXPOSE 5000

CMD ["/usr/local/bin/gunicorn", "-w", "2", "-b", ":5000", "install:app"]
