from alpine:edge
run apk add --no-cache py3-pip imagemagick ttf-liberation && \
        pip install --no-cache requests bottle eventlet
expose 8080
ADD main.py /
CMD ["/main.py"]
ENTRYPOINT ["python3"]
