# FROM surnet/alpine-wkhtmltopdf:3.16.2-0.12.6-full as wkhtmltopdf
FROM surnet/alpine-wkhtmltopdf:3.18.0-0.12.6-small as wkhtmltopdf
FROM alpine:3.14
# Install dependencies for wkhtmltopdf


#changed line 7
RUN apk update &&\
  apk add --no-cache \
  libstdc++ \
  libx11 \
  libxrender \
  libxext \
  libssl1.1 \
  ca-certificates \
  fontconfig \
  freetype \
  ttf-dejavu \
  ttf-droid \
  ttf-freefont \
  ttf-liberation \
  # more fonts
  && apk add --no-cache --virtual .build-deps \
  msttcorefonts-installer \
  # Install microsoft fonts
  && update-ms-fonts \
  && fc-cache -f \
  # Clean up when done
  && rm -rf /tmp/* \
  && apk del .build-deps


COPY --from=wkhtmltopdf /bin/wkhtmltopdf /bin/wkhtmltopdf


ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools


RUN pip install --no-cache-dir fastapi uvicorn pydantic jinja2


COPY images/ /app/images/
COPY templates/ /app/templates/
COPY main.py /app/




EXPOSE 8080
WORKDIR /app


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
