from alpine:edge
run apk add --no-cache py3-bottle py3-requests imagemagick
expose 8080
ADD main.py /
CMD ["/main.py"]
ENTRYPOINT ["python"]
