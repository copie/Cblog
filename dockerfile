FROM base/archlinux

VOLUME [ "/data" ]
COPY ./requirements.txt /
RUN cd /
RUN echo "Server = http://mirrors.163.com/archlinux/\$repo/os/\$arch" > /etc/pacman.d/mirrorlist
RUN pacman -Syyu&&pacman -S python --noconfirm&& \
    pacman -S python-pip --noconfirm&& \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gunicorn&& \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gevent&& \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /requirements.txt

EXPOSE 8000
RUN echo "zh_CN.UTF-8 UTF-8" > /etc/locale.gen
RUN locale-gen
ENV LANG=zh_CN.UTF-8
WORKDIR /data
CMD [ "gunicorn","manage:app","--bind=0.0.0.0:8000"]