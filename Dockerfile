FROM python:3.11-bookworm AS build

WORKDIR /src

RUN pip install --no-cache-dir pygame==2.5.2 numpy==1.26.1 pygbag==0.9.3

COPY . .

RUN python -m pygbag --build --no_opt \
        --cdn https://pygame-web.github.io/archives/0.8/ \
        --PYBUILD 3.11 \
        --width 960 \
        --height 960 \
        --ume_block 0 \
        --title "Slide Quest!" \
        --icon favicon.png \
        . \
    && python deploy/patch_index.py

FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /src/build/web /usr/share/nginx/html

EXPOSE 80
